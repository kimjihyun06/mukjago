"""상세페이지 맨 위 안내 이미지 만들기 (images/products/pNN/top.jpg).

카카오톡으로 받은 홍보 이미지를 그대로 쓰지 않고, **엑셀의 실제 판매가로**
먹자GO 만의 안내 이미지를 새로 그린다 (저작권 걱정 없는 자체 디자인).
가격이 바뀌면 `python tools/import_excel.py` 를 다시 돌리면 이 이미지도 함께 바뀐다.

    python tools/make_top_images.py      js/products.js 를 읽어 전부 다시 그림
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "tools" / "fonts"
GREEN, GREEN_D, ORANGE, INK, SUB, LINE, BG = "#2c5a1c", "#1e4213", "#f07a1a", "#1d1d1f", "#5f6368", "#e4e6e8", "#f7f8f6"
W = 1080
PHONE, BRAND = "010-8017-7457", "먹자고"


def font(size, weight="Bold"):
    return ImageFont.truetype(str(FONT / f"Pretendard-{weight}.otf"), size)


def won(n):
    return f"{n:,}원"


def fit(draw, text, max_w, size, weight="ExtraBold", min_size=34):
    while size > min_size and draw.textlength(text, font=font(size, weight)) > max_w:
        size -= 2
    return font(size, weight)


def wrap(draw, text, f, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=f) > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    return lines + ([cur] if cur else [])


def ship_text(s):
    return "무료배송" if s == 0 else ("택배비 문의" if s is None else f"택배비 {won(s)}")


def draw_product(p) -> Image.Image:
    opts = p["options"]
    row_h = 74
    im = Image.new("RGB", (W, 1800 + row_h * len(opts)), "white")  # 넉넉히 그리고 끝에서 자른다
    d = ImageDraw.Draw(im)

    # 머리: 로고 + 주황 띠
    logo = Image.open(ROOT / "images" / "logo.png").convert("RGBA")
    logo.thumbnail((300, 150))
    im.paste(logo, ((W - logo.width) // 2, 28), logo)
    y = 28 + logo.height + 18
    d.rectangle([0, y, W, y + 64], fill=ORANGE)
    t = "도매가로 만나는 맛있는 세상 · 오늘의 특가"
    d.text((W // 2, y + 32), t, font=font(32), fill="white", anchor="mm")
    y += 64 + 36

    # 상품 이름
    f = fit(d, p["name"], W - 120, 68)
    for line in wrap(d, p["name"], f, W - 120)[:2]:
        d.text((W // 2, y), line, font=f, fill=INK, anchor="mt")
        y += f.size + 14
    y += 10

    # 알림 칩
    chips = [p.get("tax") and f"{p['tax']} 상품", ship_text(p.get("ship")),
             p.get("deadline") and not re.search("안내", p["deadline"]) and f"주문마감 {p['deadline']}"]
    chips = [c for c in chips if c]
    cf = font(28)
    widths = [d.textlength(c, font=cf) + 44 for c in chips]
    x = (W - (sum(widths) + 16 * (len(chips) - 1))) // 2
    for c, w in zip(chips, widths):
        d.rounded_rectangle([x, y, x + w, y + 54], radius=27, outline=GREEN, width=3, fill="#eef5ea")
        d.text((x + w / 2, y + 27), c, font=cf, fill=GREEN_D, anchor="mm")
        x += w + 16
    y += 54 + 40

    # 특징 (tools/product_info.json — 홍보이미지에서 옮긴 사실)
    info = p.get("info") or {}
    if info.get("sub"):
        d.text((W // 2, y), info["sub"], font=fit(d, info["sub"], W - 160, 34, "Bold", 24), fill=GREEN_D, anchor="mt")
        y += 64
    pts = info.get("points", [])[:4]
    if pts:
        cw = (W - 120 - 18 * (len(pts) - 1)) / len(pts)
        for i, pt in enumerate(pts):
            x0 = 60 + i * (cw + 18)
            d.rounded_rectangle([x0, y, x0 + cw, y + 110], radius=18, fill="#eef5ea")
            d.text((x0 + cw / 2, y + 30), "●", font=font(22), fill=ORANGE, anchor="mm")
            pf = fit(d, pt, cw - 24, 28, "Bold", 18)
            d.text((x0 + cw / 2, y + 72), pt, font=pf, fill=INK, anchor="mm")
        y += 110 + 22
    extra = " · ".join(x for x in (info.get("origin") and f"원산지 {info['origin']}", info.get("courier")) if x)
    if extra:
        d.text((W // 2, y), extra, font=fit(d, extra, W - 120, 26, "Regular", 18), fill=SUB, anchor="mt")
        y += 52
    y += 14

    # 옵션 가격표
    d.rectangle([60, y, W - 60, y + 64], fill=GREEN)
    d.text((90, y + 32), "구성", font=font(30), fill="white", anchor="lm")
    d.text((W - 90, y + 32), "판매가", font=font(30), fill="white", anchor="rm")
    y += 64
    for i, o in enumerate(opts):
        if i % 2:
            d.rectangle([60, y, W - 60, y + row_h], fill=BG)
        label = o["name"] if o["unit"] in o["name"] or not o["unit"] else f"{o['name']} ({o['unit']})"
        lf = fit(d, label, W - 470, 30, "Regular", 22)
        sold = o.get("soldout")
        d.text((90, y + row_h / 2), label, font=lf, fill=SUB if sold else INK, anchor="lm")
        d.text((W - 90, y + row_h / 2), "품절" if sold else won(o["price"]), font=font(36, "ExtraBold"),
               fill=SUB if sold else ORANGE, anchor="rm")
        d.line([60, y + row_h, W - 60, y + row_h], fill=LINE, width=2)
        y += row_h
    y += 28
    note = "※ 판매가는 공급가에 따라 바뀔 수 있습니다." + ("" if p.get("ship") == 0 else " 택배비는 별도입니다.")
    d.text((W // 2, y), note, font=font(24, "Regular"), fill=SUB, anchor="mt")
    y += 70

    # 주문 안내 상자
    d.rounded_rectangle([60, y, W - 60, y + 120], radius=20, fill="#fff3e8", outline=ORANGE, width=3)
    d.text((W // 2, y + 38), "주문·문의는 카카오톡 특가방 또는 전화로!", font=font(32), fill=INK, anchor="mm")
    d.text((W // 2, y + 84), "평일 오전 10시 ~ 오후 5시 (주말·공휴일 휴무)", font=font(26, "Regular"), fill=SUB, anchor="mm")

    # 바닥 띠: 먹자고 / 전화
    H = y + 120 + 40 + 150
    d.rectangle([0, H - 150, W, H], fill=GREEN)
    d.text((W // 2, H - 75), f"{BRAND}  /  {PHONE}", font=font(60, "ExtraBold"), fill="white", anchor="mm")
    return im.crop((0, 0, W, H))


def build(products) -> int:
    n = 0
    for p in products:
        out = ROOT / p["top"]
        out.parent.mkdir(parents=True, exist_ok=True)
        draw_product(p).save(out, quality=86, optimize=True)
        n += 1
    return n


if __name__ == "__main__":
    t = (ROOT / "js" / "products.js").read_text(encoding="utf-8")
    data = json.loads(t[t.index("["): t.rindex("]") + 1])
    print(f"{build(data)}개 그림")
