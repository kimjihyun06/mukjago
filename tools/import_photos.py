"""상품 사진 폴더 -> images/products/pNN/ (크기 줄이기·긴 상세페이지 자르기까지).

쓰기:
    python tools/import_photos.py <사진폴더> <상품번호>
    python tools/import_photos.py ..\자료\엑셀\5수산물\밥도둑\순살게장 28
    (상품번호는 상품번호표.txt 에서 찾습니다. 끝나면 상품갱신.bat 을 한 번 더 돌리세요)

폴더 안 파일을 이렇게 나눈다:
    대표이미지.jpg / 대표*.jpg      -> 대표사진 맨 앞
    0.jpg 1.jpg 7 (1).jpg ... (숫자) -> 대표사진 (숫자 순서)       -> 1.jpg, 2.jpg ... 로 저장 (가로 최대 1200)
    아주 긴 그림 (세로 > 가로×4)     -> 상세페이지 (이름 순서)      -> detail-1.jpg ... (세로 2000px 씩 잘라 저장)
                                       ※ 「상세 안내.png」 처럼 이름에 상세가 있어도 포스터 모양이면 올리지 않음
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


NUMBERED = re.compile(r"\d+(\s*\(\d+\))?")   # 7.jpg, 윈도 복사본 7 (1).jpg
THUMB_DIR = ("썸네일", "대표")
DETAIL_DIR = ("상세",)


def _num(stem: str) -> float:
    n = re.findall(r"\d+", stem)
    return int(n[0]) + (int(n[1]) / 100 if len(n) > 1 else 0)


def _piece_key(f: Path):
    """상세 조각 순서: 이름 속 마지막 번호순, 번호 없는 그림은 맨 뒤."""
    n = re.findall(r"\d+", f.stem.replace("860x1100", ""))
    return (0, int(n[-1])) if n else (1, f.stem)


def classify(files, root: Path | None = None):
    """폴더 규칙 (하위 폴더까지 본다):
      - 이름에 「썸네일」·「대표」가 든 폴더  -> 그 안 그림 = 대표사진
      - 이름에 「상세」가 든 폴더            -> 그 안 그림 = 상세 조각 (번호순, 번호 없는 그림은 뒤)
      - 썸네일 폴더가 따로 있으면, 맨 위 폴더의 숫자 그림은 상세 조각으로 본다 (예: 하모 1~8.png)
      - 그 밖: 숫자 그림 = 대표사진, 아주 긴 그림 = 상세, 카톡·포스터 = 올리지 않음
    """
    main, detail, pieces, kakao, skip = [], [], [], [], []
    dirs = lambda f: [x for x in (f.parent.relative_to(root).parts if root else ())]
    has_thumb = any(any(k in d for k in THUMB_DIR for d in dirs(f)) for f in files)
    for f in files:
        s, ds = f.stem, dirs(f)
        if re.match(r"(?i)kakaotalk|카톡", s):
            kakao.append(f)
        elif any(k in d for k in DETAIL_DIR for d in ds):
            pieces.append(f)
        elif any(k in d for k in THUMB_DIR for d in ds):
            main.append((-1 if s.startswith("대표") else (_num(s) if NUMBERED.fullmatch(s) else 999), f))
        elif _tall(f):  # 이름에 「상세」가 있어도 포스터(세로 2배쯤)는 상세가 아님
            detail.append(f)
        elif ds:  # 규칙 밖 하위 폴더의 그림 (예: 카톡 사진 모음) -> 올리지 않음
            kakao.append(f)
        elif s.startswith("대표") and not has_thumb:
            main.append((-1, f))
        elif NUMBERED.fullmatch(s):
            (pieces.append(f) if has_thumb else main.append((_num(s), f)))
        else:
            kakao.append(f)  # 숫자·상세가 아닌 포스터·광고 그림 = 홍보이미지로 보고 올리지 않음
    main.sort(key=lambda x: x[0])
    nat = lambda f: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", f.stem)]
    return [f for _, f in main], sorted(detail, key=nat) + sorted(pieces, key=_piece_key), kakao, skip


def unwrap(src: Path) -> Path:
    """압축을 풀면 폴더 하나로 감싸져 있는 경우가 많다 -> 그 안으로 들어간다."""
    while True:
        kids = [k for k in src.iterdir() if not k.name.startswith(".")]
        if len(kids) == 1 and kids[0].is_dir():
            src = kids[0]
        else:
            return src


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, pid = Path(sys.argv[1]), int(sys.argv[2])
    src = unwrap(src)
    files = [f for f in src.rglob("*") if f.is_file() and f.suffix.lower() in EXT]
    main_f, detail_f, kakao, skip = classify(files, src)
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
