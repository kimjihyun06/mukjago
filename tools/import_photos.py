"""상품 사진 폴더 -> images/products/pNN/ (크기 줄이기·긴 상세페이지 자르기까지).

쓰기:
    python tools/import_photos.py <사진폴더> <상품번호>
    python tools/import_photos.py ..\자료\엑셀\5수산물\밥도둑\순살게장 28
    (상품번호는 상품번호표.txt 에서 찾습니다. 끝나면 상품갱신.bat 을 한 번 더 돌리세요)

폴더 안 파일을 이렇게 나눈다:
    대표이미지.jpg / 대표*.jpg      -> 대표사진 맨 앞
    0.jpg 1.jpg 7 (1).jpg ... (숫자) -> 대표사진 (숫자 순서)       -> 1.jpg, 2.jpg ... 로 저장 (가로 최대 1200)
    *상세*.jpg                      -> 상세페이지 이미지           -> detail-1.jpg ... (세로 2000px 씩 잘라 저장)
    아주 긴 그림 (세로 > 가로×4)     -> 이름이 달라도 상세페이지로 봄
    KakaoTalk_*, *카톡*, 그 밖 포스터·광고 그림
                                    -> **올리지 않는다** (공급업체 이름·전화가 들어 있음)
                                       → 필요한 내용은 tools/product_info.json 에 글로 옮겨
                                         상단 안내 이미지(top.jpg)에 먹자GO 디자인으로 다시 그린다.
그 밖의 파일은 건너뛰고 목록을 보여 준다. pNN 폴더의 옛 사진(top.jpg 제외)은 지우고 새로 넣는다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
EXT = (".jpg", ".jpeg", ".png", ".webp")
MAIN_W, DETAIL_W, SLICE_H, LIMIT = 1200, 860, 2000, 950_000


def save_small(im: Image.Image, out: Path, q: int = 84) -> int:
    im = im.convert("RGB")
    while True:
        im.save(out, quality=q, optimize=True, progressive=True)
        if out.stat().st_size <= LIMIT or q <= 50:
            return out.stat().st_size
        q -= 8


def _tall(f: Path) -> bool:
    """이름에 「상세」가 없어도 세로가 가로의 4배 넘게 긴 그림은 상세페이지로 본다."""
    w, h = Image.open(f).size
    return h > w * 4


def classify(files):
    main, detail, kakao, skip = [], [], [], []
    for f in files:
        s = f.stem
        if re.match(r"(?i)kakaotalk|카톡", s):
            kakao.append(f)
        elif "상세" in s or _tall(f):
            detail.append(f)
        elif s.startswith("대표"):
            main.insert(0, (-1, f))
        elif re.fullmatch(r"\d+(\s*\(\d+\))?", s):  # 7.jpg, 윈도 복사본 7 (1).jpg 도 숫자 사진
            n = re.findall(r"\d+", s)
            main.append((int(n[0]) + (int(n[1]) / 100 if len(n) > 1 else 0), f))
        else:
            kakao.append(f)  # 숫자·상세가 아닌 포스터·광고 그림 = 홍보이미지로 보고 올리지 않음
    main.sort(key=lambda x: x[0])
    nat = lambda f: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", f.stem)]
    return [f for _, f in main], sorted(detail, key=nat), kakao, skip


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, pid = Path(sys.argv[1]), int(sys.argv[2])
    files = [f for f in src.iterdir() if f.is_file() and f.suffix.lower() in EXT]
    main_f, detail_f, kakao, skip = classify(files)
    out = ROOT / "images" / "products" / f"p{pid:02d}"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.iterdir():
        if old.name != "top.jpg":
            old.unlink()

    total = 0
    for i, f in enumerate(main_f, 1):
        im = ImageOps.exif_transpose(Image.open(f))
        im.thumbnail((MAIN_W, MAIN_W))
        total += save_small(im, out / f"{i}.jpg")
    k = 0
    for f in detail_f:
        im = Image.open(f).convert("RGB")
        if im.width != DETAIL_W:
            im = im.resize((DETAIL_W, round(im.height * DETAIL_W / im.width)), Image.LANCZOS)
        for y in range(0, im.height, SLICE_H):
            k += 1
            total += save_small(im.crop((0, y, DETAIL_W, min(y + SLICE_H, im.height))), out / f"detail-{k}.jpg")
    print(f"p{pid:02d}: 대표사진 {len(main_f)}장, 상세 {len(detail_f)}장 -> {k}조각, 합계 {total / 1e6:.1f}MB")
    if kakao:
        print(f"  올리지 않음(카톡·포스터 홍보이미지): {', '.join(f.name for f in kakao)}")
        print("  -> 내용은 tools/product_info.json 에 옮겨 적으세요")
    if skip:
        print(f"  건너뜀(이름 규칙 밖): {', '.join(f.name for f in skip)}")


if __name__ == "__main__":
    main()
