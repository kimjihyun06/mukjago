"""먹자GO 홈페이지만의 걸쇠 — `python tools/state.py check` 가 함께 돌린다.

1) 링크·그림 : HTML·JS 가 가리키는 파일이 실제로 있는가
2) 상품 번호 : products.js 의 id 가 겹치지 않는가
3) 사진 크기 : images/ 의 파일이 1MB 이하인가, 이름이 영문인가
4) 민감 자료 : 카드번호·비밀번호 메모·카톡 원본 사진이 섞이지 않았는가
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "자료", "node_modules", "__pycache__", ".venv"}


def _files(*exts):
    for f in ROOT.rglob("*"):
        if f.is_file() and not (SKIP_DIRS & set(f.relative_to(ROOT).parts)):
            if not exts or f.suffix.lower() in exts:
                yield f


def links():
    bad = []
    pat = re.compile(r"""(?:src|href)=["']([^"'#?:]+?)(?:[?#][^"']*)?["']|["']((?:images|css|js)/[^"'?#$]+)["']""")
    for f in _files(".html", ".js", ".css"):
        code = COMMENT.sub("", f.read_text(encoding="utf-8", errors="replace"))  # 설명 속 보기 경로는 빼고
        for m in pat.finditer(code):
            ref = m.group(1) or m.group(2)
            if not ref or ref.startswith(("http", "//", "mailto", "tel", "data")) or "${" in ref:
                continue
            if not (ROOT / ref).exists():
                bad.append(f"{f.name}→{ref}")
    return ("링크·그림", not bad, "모두 있음" if not bad else ", ".join(bad[:4]))


def product_ids():
    p = ROOT / "js" / "products.js"
    if not p.exists():
        return ("상품 번호", False, "products.js 없음")
    t = p.read_text(encoding="utf-8")
    block = t.split("window.PRODUCTS", 1)[-1].split("window.REVIEWS", 1)[0]
    ids = re.findall(r"\bid:\s*(\d+)", block)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    return ("상품 번호", not dup and bool(ids),
            f"{len(ids)}개, 겹침 없음" if not dup else f"겹침: {', '.join(dup)}")


def images():
    big, named = [], []
    for f in (ROOT / "images").rglob("*"):
        if not f.is_file():
            continue
        if f.stat().st_size > 1_000_000:
            big.append(f"{f.name}({f.stat().st_size // 1024}KB)")
        if not re.fullmatch(r"[A-Za-z0-9._\-]+", f.name):
            named.append(f.name)
    ok = not big and not named
    note = "모두 1MB 이하·영문 이름" if ok else "; ".join(
        ([f"큼: {', '.join(big[:3])}"] if big else []) + ([f"한글/공백 이름: {', '.join(named[:3])}"] if named else []))
    return ("사진", ok, note)


CARD = re.compile(r"\b\d{4}[ -]\d{4}[ -]\d{4}[ -]\d{4}\b")
# 값이 8자 이상일 때만 (카톡방 참여코드 1004 처럼 공개용 짧은 번호는 제외)
SECRET = re.compile(r"(비번|비밀번호|password|passwd)\s*[:=\n]\s*[\"']?[^\s\"',]{8,}", re.I)
COMMENT = re.compile(r"/\*.*?\*/|<!--.*?-->|^\s*//.*?$", re.S | re.M)


def sensitive():
    hits = []
    for f in _files():
        rel = f.relative_to(ROOT)
        if f.name.lower().startswith("kakaotalk_") or "카드" in f.name:
            hits.append(f"원본사진? {rel}")
            continue
        if f.suffix.lower() in (".html", ".js", ".css", ".md", ".txt", ".json", ".py", ".yml"):
            if f.name == "guards_project.py":
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
            if CARD.search(t):
                hits.append(f"카드번호 꼴: {rel}")
            if SECRET.search(t):
                hits.append(f"비밀번호 메모 꼴: {rel}")
    return ("민감 자료", not hits, "없음" if not hits else "; ".join(hits[:3]))


def guards() -> list[tuple[str, bool, str]]:
    return [links(), product_ids(), images(), sensitive()]


if __name__ == "__main__":
    for name, ok, note in guards():
        print(f"  {'OK ' if ok else '!! '} {name:10} {note}")
