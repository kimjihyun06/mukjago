"""자료 폴더 전체를 훑어 **전 품목**의 대표사진·상세페이지를 한 번에 연결한다.

쓰기 (내 PC, 이 저장소 폴더에서):
    python tools/import_all_photos.py            ..\\자료\\엑셀 전체를 훑어 연결 + 홈페이지 갱신
    python tools/import_all_photos.py --dry      무엇을 어느 상품에 연결할지만 보여 줌 (바꾸지 않음)
    python tools/import_all_photos.py <폴더>     다른 자료 폴더를 지정
    (또는 사진전체갱신.bat 더블클릭)

어떻게 찾나:
  - 「상품 폴더」 = 그 안(또는 썸네일·상세·대표 하위 폴더)에 그림이 있는 폴더.
  - 폴더 이름과 상품(엑셀 시트) 이름을 비교해 가장 닮은 상품에 연결한다.
    (띄어쓰기·괄호·「국내산」 같은 흔한 말은 빼고 비교. 예: 「국내산 햇밤」 폴더 -> 국내산 햇밤 상품)
  - 애매하면(두 상품이 비슷하게 닮음) 연결하지 않고 목록으로 알려 준다 → 그 상품만
    python tools/import_photos.py <폴더> <상품번호> 로 직접.
  - 폴더 안 규칙은 tools/import_photos.py 그대로 (숫자=대표, 긴 그림/상세 폴더=상세, 카톡·포스터=안 올림).
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import import_photos as IP  # noqa: E402

HELPER = ("썸네일", "상세", "대표")
STOP = ("국내산", "국산", "프리미엄", "명품", "특가", "산지직송", "제철", "햇", "26년", "100%")


def norm(s: str) -> str:
    s = re.sub(r"\(.*?\)|\[.*?\]", "", s)
    for w in STOP:
        s = s.replace(w, "")
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def has_images(d: Path) -> bool:
    imgs = lambda p: any(f.is_file() and f.suffix.lower() in IP.EXT for f in p.iterdir())
    try:
        return imgs(d) or any(k.is_dir() and any(h in k.name for h in HELPER) and imgs(k) for k in d.iterdir())
    except PermissionError:
        return False


def product_folders(base: Path):
    for d in sorted(p for p in base.rglob("*") if p.is_dir()):
        if any(h in d.name for h in HELPER):
            continue  # 썸네일·상세 폴더는 부모 상품 폴더의 일부
        if has_images(d):
            yield d


def best_match(name: str, products):
    n = norm(name)
    scored = []
    for p in products:
        cands = {norm(p["name"])} | {norm(o["name"]) for o in p["options"]}
        s = max((difflib.SequenceMatcher(None, n, c).ratio() + (0.3 if c and (c in n or n in c) else 0)) for c in cands if c)
        scored.append((s, p))
    scored.sort(key=lambda x: -x[0])
    top = scored[0], (scored[1] if len(scored) > 1 else (0, None))
    (s1, p1), (s2, p2) = top
    if p2 and s1 - s2 < 0.08:
        # 비슷하면 괄호·「100%」까지 살린 원래 이름으로 다시 비교 (예: 간장게장 vs 간장게장(하프절단))
        light = lambda s: re.sub(r"[^0-9A-Za-z가-힣%]", "", s)
        l1 = difflib.SequenceMatcher(None, light(name), light(p1["name"])).ratio()
        l2 = difflib.SequenceMatcher(None, light(name), light(p2["name"])).ratio()
        if abs(l1 - l2) >= 0.05:
            win, lose = ((s1, p1), (s2, p2)) if l1 > l2 else ((s1, p2), (s2, p1))
            return (win[0], win[1]), (win[0] - 0.2, lose[1])  # 차이가 분명해졌으니 확정
    return top


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    base = Path(args[0]) if args else ROOT.parent / "자료" / "엑셀"
    if not base.exists():
        sys.exit(f"자료 폴더가 없습니다: {base}")
    t = (ROOT / "js" / "products.js").read_text(encoding="utf-8")
    products = json.loads(t[t.index("["): t.rindex("]") + 1])

    plan, unsure, used = [], [], {}
    for d in product_folders(base):
        (s1, p1), (s2, p2) = best_match(d.name, products)
        rel = d.relative_to(base)
        if s1 < 0.75 or (p2 and s1 - s2 < 0.08):
            unsure.append(f"{rel}  (가장 닮은: {p1['id']} {p1['name']} {s1:.2f}" + (f", 다음: {p2['id']} {p2['name']} {s2:.2f})" if p2 else ")"))
            continue
        if p1["id"] in used:
            unsure.append(f"{rel}  (상품 {p1['id']} {p1['name']} 에 이미 {used[p1['id']]} 폴더가 연결됨)")
            continue
        used[p1["id"]] = str(rel)
        plan.append((d, p1))

    print(f"자료 폴더: {base}")
    print(f"연결할 것 {len(plan)}개, 확인 필요 {len(unsure)}개\n")
    for d, p in plan:
        print(f"  p{p['id']:02d} {p['name']:<24} <- {d.relative_to(base)}")
    if unsure:
        print("\n  [확인 필요 — 연결 안 함]")
        for u in unsure:
            print("   ", u)
    if dry or not plan:
        return
    print()
    for d, p in plan:
        sys.argv = ["import_photos.py", str(d), str(p["id"])] + (["--kakao-detail"] if "--kakao-detail" in sys.argv else [])
        IP.main()
    print("\n홈페이지 상품 목록 다시 만들기 …")
    subprocess.run([sys.executable, str(ROOT / "tools" / "import_excel.py")], check=False)


if __name__ == "__main__":
    main()
