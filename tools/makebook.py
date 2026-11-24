"""개발 기록 -> 출판 원자료(07_BOOK/RAW_HISTORY.md).

손으로 옮기면 반드시 틀어진다. **기록에서 뽑는다.**
열쇠·개인정보는 여기서 한 번 걸러 내지만, 출판 전에 **눈으로 한 번 더** 본다.

쓰기:
    python tools/makebook.py          원자료 다시 만들기
    python tools/makebook.py --check  샐 만한 것이 있는지만 본다
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import state as S

RAW = ROOT / "07_BOOK" / "RAW_HISTORY.md"

LEAK = [
    (re.compile(r"\bAQ\.[A-Za-z0-9_\-]{10,}"), "열쇠"),
    (re.compile(r"\bAIza[A-Za-z0-9_\-]{20,}"), "열쇠"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{10,}"), "열쇠"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "열쇠"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}"), "열쇠"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "메일 주소"),
    (re.compile(r"\b01[016-9][-.\s]?\d{3,4}[-.\s]?\d{4}\b"), "전화번호"),
    (re.compile(r"\b\d{6}[-\s]?[1-4]\d{6}\b"), "주민번호 꼴"),
]


def find_leaks(text: str):
    return [(w, m.group(0)[:16] + "...")
            for pat, w in LEAK for m in pat.finditer(text)]


def mask(text: str) -> str:
    for pat, _ in LEAK:
        text = pat.sub(lambda m: m.group(0)[:4] + "*" * 8, text)
    return text


def parse_dev():
    if not S.DEV.exists():
        return []
    txt = S.DEV.read_text(encoding="utf-8")
    recs = []
    for b in re.split(r"^=+$", txt, flags=re.M):
        m = re.search(r"\[DEVELOPMENT RECORD #(\d+)\]", b)
        if not m:
            continue
        rec = {"no": int(m.group(1))}
        d = re.search(r"^DATE:\s*(.*)$", b, re.M)
        t = re.search(r"^TIME:\s*(.*)$", b, re.M)
        rec["date"] = d.group(1).strip() if d else ""
        rec["time"] = t.group(1).strip() if t else ""
        for key, label in S.DEV_LABEL.items():
            mm = re.search(rf"^{re.escape(label)}\n(.*?)(?=\n\[|\n=|\Z)",
                           b, re.S | re.M)
            rec[key] = mm.group(1).strip() if mm else ""
        recs.append(rec)
    return sorted(recs, key=lambda r: r["no"])


HEAD = """# RAW HISTORY - 출판 원자료

> 이 파일은 **`tools/makebook.py` 가 기록에서 뽑아 만든다.**
>    손으로 고치지 않는다 - 다시 뽑으면 지워진다.
>    고칠 것이 있으면 `04_LOG/` 의 원래 기록을 고치고 다시 뽑는다.
>
> 열쇠·개인정보는 한 번 걸러 냈지만, **출판 전에 눈으로 한 번 더** 본다.
>
> 다듬은 원고는 `BOOK_MANUSCRIPT.md` 로 간다. **RAW -> EDIT -> BOOK**

마지막으로 뽑은 때: {when}

---

## 숫자 (실제 기록에서 셈)

{stats}

---
"""

SEC = """
## 제{no:03d}회 · {date} {time}

### 무엇이 문제였나
{context}

### 사용자가 지시한 것
{user}

### 분석
{analysis}

### 실제로 한 일
{execution}

### 건드린 파일
{files}

### 일어난 오류
{error}

### 진범
{cause}

### 고친 방법
{fix}

### 어떻게 쟀나
{test}

### 결과
{result}

### 정한 것
{decision}

---
"""


def build() -> str:
    recs = parse_dev()
    stats_txt = "\n".join(f"- {k}: **{v:,}**" for k, v in S.stats().items())
    body = [HEAD.format(when=datetime.now().strftime("%Y-%m-%d %H:%M"),
                        stats=stats_txt)]
    for r in recs:
        body.append(SEC.format(
            no=r["no"], date=r["date"], time=r["time"],
            context=r.get("context") or "-", user=r.get("user") or "-",
            analysis=r.get("analysis") or "-",
            execution=r.get("execution") or "-",
            files=r.get("files") or "-",
            error=r.get("error") or "(없음)",
            cause=r.get("cause") or "(없음)",
            fix=r.get("fix") or "(없음)",
            test=r.get("test") or "-", result=r.get("result") or "-",
            decision=r.get("decision") or "-"))
    for p, title in ((S.ERR, "오류 역사"), (S.DEC, "결정 역사"),
                     (S.TEST, "시험 역사")):
        if p.exists():
            t = re.sub(r"^# .*$", "", p.read_text(encoding="utf-8"),
                       count=1, flags=re.M).strip()
            body.append(f"\n# {title}\n\n{t}\n\n---\n")
    return mask("\n".join(body))


def main() -> None:
    if "--check" in sys.argv:
        src = S.DEV.read_text(encoding="utf-8") if S.DEV.exists() else ""
        leaks = find_leaks(src)
        if leaks:
            print("!! 샐 만한 것:")
            for what, bit in leaks:
                print(f"   {what}: {bit}")
            sys.exit(1)
        print("OK  기록에서 열쇠·개인정보 꼴을 찾지 못했습니다.")
        print("    (모양으로만 찾습니다 - 출판 전에 눈으로 한 번 더 보세요)")
        return
    text = build()
    S._write(RAW, text)
    print(f"원자료를 뽑았습니다 -> {RAW}")
    print(f"  {len(parse_dev())}회차 · {len(text):,}자")


if __name__ == "__main__":
    main()
