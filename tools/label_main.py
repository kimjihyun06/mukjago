"""대표사진(1.jpg)에 상품 이름 글자(이름표)를 넣는다.

쓰기:
    python tools/label_main.py              tools/product_info.json 의 main_label 이 있는 상품 전부
    python tools/label_main.py 9            9번 상품만
설정 (tools/product_info.json):
    "9": {"main_label": "활 돌문어"}
- import_photos.py 가 사진을 다시 넣을 때도 자동으로 붙인다 (원본 폴더 사진은 그대로).
- 아래쪽 가운데에 먹자GO 초록 이름표. 같은 사진에 두 번 붙지 않도록 표시를 남긴다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "tools" / "fonts" / "Pretendard-ExtraBold.otf"
MARK = "mukjago-label"  # JPEG 주석에 남겨 두 번 붙는 것을 막는다


def apply(img_path: Path, text: str) -> bool:
    im = Image.open(img_path)
    if MARK.encode() in (im.info.get("comment") or b""):
        return False
    im = im.convert("RGB")
    w, h = im.size
    d = ImageDraw.Draw(im, "RGBA")
    size = max(28, w // 11)
    f = ImageFont.truetype(str(FONT), size)
    tw = d.textlength(text, font=f)
    px, py = size * 0.9, size * 0.45
    bw, bh = tw + px * 2, size + py * 2
    x0, y0 = (w - bw) / 2, h - bh - h * 0.05
    d.rounded_rectangle([x0 + 4, y0 + 6, x0 + bw + 4, y0 + bh + 6], radius=bh / 2, fill=(0, 0, 0, 70))  # 그림자
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=bh / 2, fill=(44, 90, 28, 235), outline=(255, 255, 255, 230), width=max(2, size // 14))
    d.text((w / 2, y0 + bh / 2), text, font=f, fill="white", anchor="mm")
    im.save(img_path, quality=88, optimize=True, progressive=True, comment=MARK.encode())
    return True


def run(only: set[int] | None = None) -> list[str]:
    info = json.loads((ROOT / "tools" / "product_info.json").read_text(encoding="utf-8"))
    done = []
    for k, v in info.items():
        if not k.isdigit() or not isinstance(v, dict) or not v.get("main_label"):
            continue
        if only and int(k) not in only:
            continue
        p = ROOT / "images" / "products" / f"p{int(k):02d}" / "1.jpg"
        if p.exists():
            done.append(f"p{int(k):02d} {v['main_label']} " + ("붙임" if apply(p, v["main_label"]) else "이미 있음"))
        else:
            done.append(f"p{int(k):02d} 1.jpg 없음 (실제 대표사진이 없으면 붙이지 않음)")
    return done


if __name__ == "__main__":
    ids = {int(a) for a in sys.argv[1:] if a.isdigit()} or None
    for line in run(ids):
        print(line)
