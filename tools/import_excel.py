"""공급표 엑셀 -> 홈페이지 상품 (js/products.js) + 상세 상단 안내 이미지.

쓰기:
    python tools/import_excel.py                       ../자료/엑셀 의 가장 최근 .xlsx 사용
    python tools/import_excel.py <엑셀파일경로>          파일을 직접 지정
    python tools/import_excel.py --no-images           안내 이미지는 다시 만들지 않음

규칙 (엑셀을 이렇게 읽는다):
  - 시트 하나 = 상품 하나. 시트 안의 품목명 하나하나 = 선택 옵션.
  - **숨김 시트는 올리지 않는다** (품절·판매중단 시트).
  - 같은 품목명이 여러 줄이면 **일자가 가장 늦은 줄**의 실제 판매가·택배비를 쓴다.
  - 비고에 「품절」이 적힌 줄이 마지막 가격보다 늦으면 그 옵션은 품절로 표시.
  - 공급가액·마진 같은 **매입 정보는 홈페이지에 절대 싣지 않는다.**

사진 (상품 번호 폴더 images/products/pNN/ 에 넣고 이 명령을 다시 돌린다):
  - 숫자 이름 (1.jpg, 2.jpg ...)        -> 대표사진 (전부, 숫자 순서대로)
  - detail 로 시작 (detail-1.jpg ...)   -> 상세페이지 이미지 (안내 이미지 아래)
  - top.jpg                            -> 이 명령이 자동으로 만드는 상단 안내 이미지
상품 번호는 tools/product_ids.json 에 시트 이름별로 고정된다 (시트 순서가 바뀌어도 그대로).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDS = ROOT / "tools" / "product_ids.json"
OUT = ROOT / "js" / "products.js"
IMG = ROOT / "images" / "products"
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def find_xlsx(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    folder = ROOT.parent / "자료" / "엑셀"
    files = sorted(folder.glob("*.xlsx"), key=lambda p: p.stat().st_mtime)
    files = [f for f in files if not f.name.startswith("~$")]
    if not files:
        sys.exit(f"엑셀이 없습니다: {folder}\n  python tools/import_excel.py <엑셀경로> 로 지정하세요")
    return files[-1]


def num(v):
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        s = v.replace(",", "").replace("원", "").strip()
        try:
            return float(s)
        except ValueError:
            return None
    return None


def ymd(v) -> str:
    """261013 -> 2026-10-13. (2611112 처럼 잘못 친 것도 앞 6자리로 읽음)"""
    s = re.sub(r"\D", "", str(v or ""))[:6]
    if len(s) != 6:
        return ""
    return f"20{s[:2]}-{s[2:4]}-{s[4:]}"


def category(kind: str, tax: str) -> str:
    kind = kind or ""
    if kind == "김치":
        return "kimchi"
    if kind == "수산":
        return "easy" if tax == "과세" else "sea"   # 게장·무침·새우장 = 반찬
    return "farm"


EMOJI = [("김치", "🥬"), ("묵은지", "🥬"), ("소박이", "🥒"), ("게장", "🦀"), ("새우장", "🦐"), ("굴", "🦪"), ("석화", "🦪"), ("게", "🦀"), ("새우", "🦐"), ("오징어", "🦑"), ("문어", "🐙"),
         ("고동", "🐚"), ("바지락", "🐚"), ("꼬막", "🐚"), ("가리비", "🐚"), ("김", "🍙"), ("홍어", "🐟"),
         ("과메기", "🐟"), ("조기", "🐟"), ("박대", "🐟"), ("방어", "🐟"), ("하모", "🐟"),
         ("김치", "🥬"), ("소박이", "🥒"), ("고구마", "🍠"), ("밤", "🌰"), ("옥수수", "🌽"), ("양파", "🧅"),
         ("파프리카", "🫑"), ("시금치", "🥬"), ("봄동", "🥬"), ("케일", "🥬"), ("채소", "🥗"), ("호박", "🎃"),
         ("무", "🥕"), ("마", "🍠"), ("히카마", "🥔")]


def emoji(name: str) -> str:
    for k, e in EMOJI:
        if k in name:
            return e
    return "🛒"


def read_sheets(path: Path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    sheets = []
    for ws in wb.worksheets:
        rows = [r for r in ws.iter_rows(values_only=True) if any(v is not None for v in r)]
        hi = next((i for i, r in enumerate(rows) if "품목명" in r), None)
        if hi is None:
            continue
        head = [(str(x).split("\n")[0].strip() if x else "") for x in rows[hi]]
        col = {}
        for j, n in enumerate(head):
            col.setdefault(n, j)
        sp = col.get("실제 판매가")
        ship_j = next((j for j, n in enumerate(head) if n == "택배비" and sp is not None and j > sp), None)

        def g(r, k):
            j = col.get(k)
            return r[j] if j is not None and j < len(r) else None

        opts, meta, soldout = {}, {"start": "", "deadline": "", "kind": "", "tax": ""}, {}
        for r in rows[hi + 1:]:
            d = ymd(g(r, "일자"))
            for k in ("판매 활동 내역", "비고"):
                t = str(g(r, k) or "")
                if "판매개시" in t and not meta["start"]:
                    m = re.search(r"(\d{2})\.\s*(\d{1,2})\.\s*(\d{1,2})", t)
                    meta["start"] = f"20{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else d
            dl = g(r, "발주 마감시간")
            if isinstance(dl, str) and dl.strip() and not meta["deadline"]:
                meta["deadline"] = re.sub(r"\s+", " ", dl).strip()
            name = str(g(r, "품목명") or "").strip()
            note = str(g(r, "비고") or "")
            if name and "품절" in note:
                soldout[name] = d
            price = num(g(r, "실제 판매가"))
            if not name or not price:
                continue
            meta["kind"] = meta["kind"] or str(g(r, "구분") or "").strip()
            meta["tax"] = meta["tax"] or str(g(r, "면세/과세유무") or "").strip()
            unit = str(g(r, "옵션") or "").strip()
            if not unit:  # 옵션칸이 빈 옛 줄 -> 같은 품목명의 기존 옵션에 붙인다
                unit = next((k[1] for k in opts if k[0] == name), "")
            key = (name, unit)
            o = opts.get(key)
            if o is None or d >= o["date"]:
                ship_raw = r[ship_j] if ship_j is not None and ship_j < len(r) else None
                opts[key] = {"name": name, "unit": unit, "price": int(round(price)),
                              "ship": None if num(ship_raw) is None else int(num(ship_raw)),
                              "tax": str(g(r, "면세/과세유무") or meta["tax"]).strip(), "date": d}
        known = {o["ship"] for o in opts.values() if o["ship"] is not None}
        if known == {0}:  # 「-」 칸: 같은 시트가 모두 무료배송이면 무료로 (홍게 포스터로 확인함)
            for o in opts.values():
                if o["ship"] is None:
                    o["ship"] = 0
        for (n, u), o in opts.items():
            if n in soldout and soldout[n] >= o["date"]:
                o["soldout"] = True
        if "안내" in meta["deadline"]:  # 「마감시간 따로 안내x」 등은 싣지 않는다
            meta["deadline"] = ""
        if opts:
            sheets.append({"sheet": ws.title, "hidden": ws.sheet_state != "visible", **meta, "options": list(opts.values())})
    return sheets


def images_for(pid: str):
    folder = IMG / pid
    if not folder.exists():
        return [], []
    files = [f for f in folder.iterdir() if f.suffix.lower() in IMG_EXT]
    main = sorted((f for f in files if f.stem.isdigit()), key=lambda f: int(f.stem))
    detail = sorted((f for f in files if f.stem.lower().startswith("detail")),
                    key=lambda f: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", f.stem)])
    rel = lambda f: f.relative_to(ROOT).as_posix()
    return [rel(f) for f in main], [rel(f) for f in detail]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    xlsx = find_xlsx(args[0] if args else None)
    sheets = read_sheets(xlsx)
    ids = json.loads(IDS.read_text(encoding="utf-8")) if IDS.exists() else {}
    nxt = max(ids.values(), default=0) + 1
    for s in sheets:
        if s["sheet"] not in ids:
            ids[s["sheet"]] = nxt
            nxt += 1
    IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")

    info_f = ROOT / "tools" / "product_info.json"
    info = json.loads(info_f.read_text(encoding="utf-8")) if info_f.exists() else {}
    products, hidden = [], []
    for s in sheets:
        if s["hidden"]:
            hidden.append(s["sheet"])
            continue
        pid = ids[s["sheet"]]
        folder = f"p{pid:02d}"
        main_imgs, detail_imgs = images_for(folder)
        opts = [{k: o[k] for k in ("name", "unit", "price", "ship", "tax")} | ({"soldout": True} if o.get("soldout") else {})
                for o in s["options"]]
        live = [o for o in opts if not o.get("soldout")] or opts
        name = re.sub(r"^★\s*특가\s*", "", s["sheet"]).strip()
        products.append({
            "id": pid, "name": name, "cat": category(s["kind"], s["tax"]),
            "tax": s["tax"], "deadline": s["deadline"], "start": s["start"],
            "price": min(o["price"] for o in live),
            "ship": min((o["ship"] for o in live if o["ship"] is not None), default=None),
            "emoji": emoji(name), "images": main_imgs,
            "top": f"images/products/{folder}/top.jpg", "detail": detail_imgs,
            "options": opts,
            **({"info": info[str(pid)]} if str(pid) in info else {}),
        })

    head = (f"/* 자동 생성 파일 — 손으로 고치지 마세요 (다시 만들면 지워집니다).\n"
            f" * 원본: {xlsx.name}\n * 만든 때: {datetime.now():%Y-%m-%d %H:%M}\n"
            f" * 다시 만들기: python tools/import_excel.py\n"
            f" * 문구·후기·공지·분류는 js/content.js 에서 고칩니다. */\n")
    OUT.write_text(head + "window.PRODUCTS = " + json.dumps(products, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    lines = ["상품 번호표 (자동 생성) — 사진은 images/products/<폴더>/ 에 넣습니다", "",
             "폴더   주소                      대표사진 상세  상품"]
    for p in sorted(products, key=lambda x: x["id"]):
        lines.append(f"p{p['id']:02d}   product.html?id={p['id']:<4}      {len(p['images']):>3}    {len(p['detail']):>3}   {p['name']}")
    if hidden:
        lines += ["", "올리지 않은 숨김 시트: " + ", ".join(hidden)]
    (ROOT / "상품번호표.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    n_opt = sum(len(p["options"]) for p in products)
    print(f"엑셀: {xlsx.name}")
    print(f"  시트 {len(sheets)}개 -> 상품 {len(products)}개 (옵션 {n_opt}개), 숨김 시트 {len(hidden)}개 제외")
    print(f"  대표사진 있는 상품 {sum(1 for p in products if p['images'])}개, 상세이미지 있는 상품 {sum(1 for p in products if p['detail'])}개")
    print(f"  -> {OUT.relative_to(ROOT)}")

    if "--no-images" not in sys.argv:
        sys.path.insert(0, str(ROOT / "tools"))
        import make_top_images
        made = make_top_images.build(products)
        print(f"  상단 안내 이미지 {made}개 -> images/products/pNN/top.jpg")


if __name__ == "__main__":
    main()
