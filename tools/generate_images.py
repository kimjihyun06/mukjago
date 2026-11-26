"""대표사진이 없는 상품의 「연출 이미지」를 Gemini 로 만든다 (images/products/pNN/ai-1.jpg).

쓰기:
    python tools/generate_images.py            대표사진 없는 상품만 (이미 만든 것은 건너뜀 = 돈 안 듦)
    python tools/generate_images.py --dry      무엇을 몇 장 만들지만 보여 줌 (호출 없음)
    python tools/generate_images.py --only 3 7 --force   3·7번만 다시 만듦 (돈 듦)
    끝나면: python tools/import_excel.py  (또는 상품갱신.bat)

- 묘사는 tools/ai_prompts.json (상품번호: 영어 묘사). 그림 속 글자·로고·상표는 넣지 않게 지시한다.
- 실제 사진(1.jpg …)이 들어오면 import_photos 가 ai-*.jpg 를 지우고 실제 사진이 대표가 된다.
- 홈페이지에는 「연출 이미지」 표시가 붙는다 (손님 오해 방지).
- 열쇠: 내 PC 에서는 환경변수 GEMINI_API_KEY 에 넣는다 (aistudio.google.com 에서 발급).
  클라우드 세션에서는 저장된 네트워크 비밀값을 프록시가 붙여 준다. **열쇠를 이 파일에 적지 않는다.**
- 비용: 2026-11 기준 gemini-2.5-flash-image 한 장 약 $0.04 (요금은 바뀔 수 있음 — 구글 요금표 확인).
"""
from __future__ import annotations

import base64
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
URL = "https://generativelanguage.googleapis.com/v1beta/openai/images/generations"
MODEL = "gemini-2.5-flash-image"
STYLE = ("Realistic appetizing e-commerce product photo for a Korean online grocery store: {subject}. "
         "Soft natural daylight, clean light background, square 1:1 composition, sharp focus, true-to-life colors. "
         "No text, no letters, no numbers, no logos, no labels, no brand names, no watermark, no people.")
PRICE_PER_IMAGE_USD = 0.04  # 대략값 — 실제 청구는 구글 요금표 기준


def products():
    t = (ROOT / "js" / "products.js").read_text(encoding="utf-8")
    return json.loads(t[t.index("["): t.rindex("]") + 1])


def has_real_photo(pid: int) -> bool:
    d = ROOT / "images" / "products" / f"p{pid:02d}"
    return d.exists() and any(f.stem.isdigit() for f in d.iterdir())


def generate(prompt: str) -> bytes:
    key = os.environ.get("GEMINI_API_KEY") or "proxy-injected"  # 클라우드: 프록시가 진짜 열쇠로 바꿔 끼움
    body = json.dumps({"model": MODEL, "prompt": prompt, "n": 1, "response_format": "b64_json"}).encode()
    for wait in (0, 10, 30, 60):
        if wait:
            print(f"    {wait}초 쉬고 다시 …")
            time.sleep(wait)
        req = urllib.request.Request(URL, data=body, method="POST",
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return base64.b64decode(json.load(r)["data"][0]["b64_json"])
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 503):
                print(f"    HTTP {e.code} (잠시 막힘): {msg[:120]}")
                continue
            raise SystemExit(f"HTTP {e.code}: {msg}")
    raise SystemExit("여러 번 시도했지만 실패했습니다 (요청 한도). 잠시 뒤 다시 돌리면 이어서 만듭니다.")


def main():
    args = sys.argv[1:]
    only = {int(a) for a in args if a.isdigit()}
    force, dry = "--force" in args, "--dry" in args
    prompts = json.loads((ROOT / "tools" / "ai_prompts.json").read_text(encoding="utf-8"))
    todo, skipped, missing = [], [], []
    for p in products():
        pid = p["id"]
        if only and pid not in only:
            continue
        if has_real_photo(pid):
            continue  # 실제 사진이 있으면 AI 사진은 만들지 않는다
        out = ROOT / "images" / "products" / f"p{pid:02d}" / "ai-1.jpg"
        if out.exists() and not force:
            skipped.append(pid)
            continue
        if str(pid) not in prompts:
            missing.append(f"{pid} {p['name']}")
            continue
        todo.append((p, out))
    print(f"만들 것 {len(todo)}장 (예상 약 ${len(todo) * PRICE_PER_IMAGE_USD:.2f}), 이미 있어 건너뜀 {len(skipped)}개")
    if missing:
        print("  묘사 없음 (tools/ai_prompts.json 에 더하세요): " + ", ".join(missing))
    if dry:
        for p, _ in todo:
            print(f"  p{p['id']:02d} {p['name']}")
        return
    made = 0
    for i, (p, out) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] p{p['id']:02d} {p['name']}")
        raw = generate(STYLE.format(subject=prompts[str(p["id"])]))
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.thumbnail((1000, 1000))
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=84, optimize=True, progressive=True)
        made += 1
    print(f"끝: {made}장 만듦 (약 ${made * PRICE_PER_IMAGE_USD:.2f}). 이제 python tools/import_excel.py")


if __name__ == "__main__":
    main()
