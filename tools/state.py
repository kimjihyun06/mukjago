"""상태판·개발기록·자가점검 — 손이 아니라 명령으로.

규칙을 글로만 적어 두면 지키지 않게 된다. **명령 한 줄로 되게** 만든다.

쓰기:
    python tools/state.py                 지금 상태 + 자가점검
    python tools/state.py check           걸쇠 전부 돌리기
    python tools/state.py log             개발 기록 한 건 (대화형)
    python tools/state.py log --json x.json   기록 한 건 (파일로)
    python tools/state.py test            시험 기록 한 건
    python tools/state.py error           오류 기록 한 건
    python tools/state.py decide          결정 기록 한 건
    python tools/state.py checkpoint      지금을 재개 지점으로 저장
    python tools/state.py set key=value   상태판의 한 칸만 고치기
    python tools/state.py stats           출판용 숫자 뽑기

프로젝트만의 걸쇠를 더하려면 `tools/guards_project.py` 를 만들고
그 안에 `def guards() -> list[tuple[str, bool, str]]` 를 둔다.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "04_LOG"
BOOK = ROOT / "07_BOOK"

STATE = LOG / "PROJECT_STATE.md"
CHECKPOINT = LOG / "CHECKPOINT.md"
DEV = LOG / "DEVELOPMENT_LOG.md"
ERR = LOG / "ERROR_LOG.md"
TEST = LOG / "TEST_LOG.md"
DEC = LOG / "DECISION_LOG.md"
CHANGE = LOG / "CHANGELOG.md"


def now():
    t = datetime.now()
    return t.strftime("%Y-%m-%d"), t.strftime("%H:%M")


def _write(p: Path, text: str) -> None:
    """임시파일 -> 교체. 쓰다 실패해도 원본이 날아가지 않는다.

    [실제로 데인 것] 윈도는 백신·동기화 프로그램이 파일을 잠깐 잡고 있으면
    replace 를 거부한다(WinError 5). 한 번 실패했다고 포기하면 기록이 빠진다.
    """
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    last = None
    for wait in (0, 0.15, 0.4, 0.9, 1.6):
        if wait:
            time.sleep(wait)
        try:
            tmp.replace(p)
            return
        except PermissionError as e:
            last = e
    raise RuntimeError(
        f"{p.name} 을 바꾸지 못했습니다(윈도가 막음). "
        f"내용은 {tmp.name} 에 있습니다: {last}")


def _append(p: Path, text: str) -> None:
    old = p.read_text(encoding="utf-8") if p.exists() else ""
    _write(p, old.rstrip() + "\n\n" + text.strip() + "\n")


def next_no(path: Path, pattern: str) -> int:
    """지난 번호 다음 것. **지우거나 다시 쓰지 않는다.**

    [실제로 데인 것] 줄 머리(^)를 쓰는 본은 re.M 없이는 한 건도 못 찾는다.
    못 찾으면 1 로 되돌아가 **앞 기록을 덮어쓴다.**
    """
    if not path.exists():
        return 1
    nums = [int(m) for m in re.findall(
        pattern, path.read_text(encoding="utf-8"), re.M)]
    return (max(nums) + 1) if nums else 1


# -- 자가점검 ------------------------------------------------------
def running_servers():
    """지금 듣고 있는 포트. **끄지 않는다 - 비켜 가려고 본다.**"""
    try:
        out = subprocess.run(["netstat", "-ano"], capture_output=True,
                             text=True, errors="replace").stdout
    except Exception:
        return []
    # 모든 포트를 잡으면 윈도 안쪽 것까지 수십 개가 떠 아무도 안 본다.
    # **개발 서버가 쓰는 자리**만 본다.
    found = []
    for line in out.splitlines():
        if "LISTENING" not in line:
            continue
        m = re.search(r":(\d{4,5})\s", line)
        if not m:
            continue
        port = int(m.group(1))
        if 3000 <= port <= 9999:
            found.append((m.group(1), line.split()[-1]))
    return sorted(set(found))[:10]


SYSTEM_OK = ("c:/windows", "c:\\windows", "c:/program files",
             "c:\\program files", "c:/programdata", "c:\\programdata",
             "/usr/", "/opt/", "/library/", "/system/")


def guards():
    """프로그램 걸쇠를 한자리에서 돌린다."""
    sys.path.insert(0, str(ROOT))
    out = []

    # 1) 모든 .py 문법
    bad = []
    pys = [f for f in ROOT.rglob("*.py")
           if not any(x in f.parts for x in
                      (".venv", "venv", "__pycache__", "node_modules",
                       "site-packages", "build", "dist"))]
    for f in pys:
        try:
            compile(f.read_text(encoding="utf-8", errors="replace"),
                    str(f), "exec")
        except SyntaxError as e:
            bad.append(f"{f.name}:{e.lineno}")
    out.append(("문법", not bad,
                f"{len(pys)}개 모두 정상" if not bad
                else ", ".join(bad[:4])))

    # 2) 폴더 밖 절대경로 (자가포함)
    leaks = []
    pat = re.compile(r"""["']([A-Za-z]:[\\/][^"']{3,}|/[A-Za-z][^"']{6,})["']""")
    me = str(ROOT).lower().replace("\\", "/")
    # 걸쇠 자신과 설치기는 보기(예시) 경로를 품고 있다 - 빼고 본다.
    SKIP = ("state.py", "makebook.py", "guards_project.py",
            "협업체계_설치.py")
    for f in pys:
        if f.name in SKIP:
            continue
        for m in pat.finditer(f.read_text(encoding="utf-8", errors="replace")):
            hit = m.group(1)
            low = hit.lower().replace("\\", "/")
            if low.startswith(SYSTEM_OK) or low.startswith(me):
                continue
            leaks.append(f"{f.name}: {hit[:40]}")
    out.append(("자가포함", not leaks,
                "폴더 밖 절대경로 없음" if not leaks
                else "; ".join(leaks[:3])))

    # 3) 열쇠가 평문으로 적혀 있는가
    KEYPAT = [re.compile(r"\bAQ\.[A-Za-z0-9_\-]{15,}"),
              re.compile(r"\bAIza[A-Za-z0-9_\-]{25,}"),
              re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}"),
              re.compile(r"\bsk-[A-Za-z0-9]{30,}"),
              re.compile(r"\bghp_[A-Za-z0-9]{30,}")]
    found = []
    for f in list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.md")) \
            + list(ROOT.rglob("*.txt")) + list(ROOT.rglob("*.json")):
        if any(x in f.parts for x in (".venv", "venv", "__pycache__",
                                      "node_modules", "site-packages")):
            continue
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for p in KEYPAT:
            if p.search(t):
                found.append(f.name)
                break
    out.append(("열쇠 평문", not found,
                "없음" if not found else f"의심: {', '.join(found[:3])}"))

    # 4) 기록이 성한가
    missing = [p.name for p in (STATE, DEV, ERR, TEST, DEC) if not p.exists()]
    out.append(("기록 파일", not missing,
                "모두 있음" if not missing else f"없음: {', '.join(missing)}"))

    # 5) 번호가 어긋나지 않았는가
    dup = []
    for p, pat_ in ((DEV, r"\[DEVELOPMENT RECORD #(\d+)\]"),
                    (ERR, r"\[ERROR #(\d+)\]"),
                    (DEC, r"\[DECISION #(\d+)\]"),
                    (TEST, r"^\| T(\d+) \|")):
        if not p.exists():
            continue
        ns = re.findall(pat_, p.read_text(encoding="utf-8"), re.M)
        if len(ns) != len(set(ns)):
            dup.append(p.name)
    out.append(("기록 번호", not dup,
                "겹침 없음" if not dup else f"겹침: {', '.join(dup)}"))

    # 6) 프로젝트만의 걸쇠 (있으면)
    gp = ROOT / "tools" / "guards_project.py"
    if gp.exists():
        try:
            sys.path.insert(0, str(ROOT / "tools"))
            import guards_project
            out.extend(guards_project.guards())
        except Exception as e:
            out.append(("프로젝트 걸쇠", False, f"{type(e).__name__}: {e}"))
    return out


def self_audit() -> str:
    d, t = now()
    srv = running_servers()
    lines = [f"[SELF AUDIT] {d} {t}", "", f"PROJECT : {ROOT}"]
    lines.append("돌고 있는 것 : "
                 + (", ".join(f"포트 {p}" for p, _ in srv[:8])
                    if srv else "없음")
                 + ("   <- 끄지 말 것" if srv else ""))
    lines.append("")
    for name, ok, note in guards():
        lines.append(f"  {'OK ' if ok else '!! '} {name:10} {note}")
    return "\n".join(lines)


# -- 상태판 --------------------------------------------------------
STATE_TMPL = """# PROJECT STATE

> **지금** 상태만 적는다. 과거는 `DEVELOPMENT_LOG.md` 로 간다.

| | |
|---|---|
| Last Updated | {date} {time} |
| Version | {version} |

## 지금 하는 일
{current}

## 끝난 일
{done}

## 남은 일
{todo}

## 막힌 것
{blocked}

## 마지막 오류
{error}

## 마지막 시험
{test}

## 승인 기다리는 것
{pending}

## 위험
{risk}

## 다음
{next}
"""

FIELDS = (("current", "지금 하는 일"), ("done", "끝난 일"),
          ("todo", "남은 일"), ("blocked", "막힌 것"),
          ("error", "마지막 오류"), ("test", "마지막 시험"),
          ("pending", "승인 기다리는 것"), ("risk", "위험"), ("next", "다음"))


def read_state() -> dict:
    if not STATE.exists():
        return {}
    txt = STATE.read_text(encoding="utf-8")
    out = {}
    for key, head in FIELDS:
        m = re.search(rf"^## {head}\n(.*?)(?=\n## |\Z)", txt, re.S | re.M)
        out[key] = (m.group(1).strip() if m else "")
    m = re.search(r"\| Version \| (.*?) \|", txt)
    out["version"] = m.group(1).strip() if m else "0.1.0"
    return out


def save_state(**kw) -> None:
    cur = read_state()
    cur.update({k: v for k, v in kw.items() if v is not None})
    d, t = now()
    _write(STATE, STATE_TMPL.format(
        date=d, time=t, version=cur.get("version", "0.1.0"),
        **{k: (cur.get(k) or "-") for k, _ in FIELDS}))


# -- 기록 한 건씩 --------------------------------------------------
DEV_FIELDS = ["user", "context", "analysis", "plan", "execution", "files",
              "error", "cause", "fix", "test", "result", "decision", "next"]
DEV_LABEL = {"user": "[USER] 사용자 지시", "context": "[CONTEXT] 그때 상황",
             "analysis": "[ANALYSIS] 분석", "plan": "[PLAN] 계획",
             "execution": "[EXECUTION] 실제 한 일",
             "files": "[FILES] 건드린 파일",
             "error": "[ERROR] 오류", "cause": "[ROOT CAUSE] 진범",
             "fix": "[FIX] 고침", "test": "[TEST] 어떻게 쟀나",
             "result": "[RESULT] 결과", "decision": "[DECISION] 정한 것",
             "next": "[NEXT] 다음"}


def add_dev(rec: dict) -> int:
    no = next_no(DEV, r"\[DEVELOPMENT RECORD #(\d+)\]")
    d, t = now()
    body = ["=" * 58, f"[DEVELOPMENT RECORD #{no:03d}]", "",
            f"DATE: {rec.get('date', d)}", f"TIME: {rec.get('time', t)}", ""]
    for f in DEV_FIELDS:
        v = str(rec.get(f, "") or "").strip()
        if v:
            body += [DEV_LABEL[f], v, ""]
    body.append("=" * 58)
    _append(DEV, "\n".join(body))
    return no


def add_test(rec: dict) -> int:
    if not TEST.exists():
        _write(TEST, "# TEST LOG\n\n"
                     "> 잰 값만 적는다. **「돌았다」는 시험이 아니다.**\n\n"
                     "| 번호 | 날짜 | 대상 | 어떻게 쟀나 | 바란 값 "
                     "| 실제 값 | 판정 |\n|---|---|---|---|---|---|---|\n")
    no = next_no(TEST, r"^\| T(\d+) \|")
    d, _ = now()
    row = (f"| T{no:03d} | {rec.get('date', d)} | {rec.get('target', '')} "
           f"| {rec.get('how', '')} | {rec.get('want', '')} "
           f"| {rec.get('got', '')} | {rec.get('verdict', '')} |")
    _write(TEST, TEST.read_text(encoding="utf-8").rstrip() + "\n" + row + "\n")
    return no


def add_error(rec: dict) -> int:
    no = next_no(ERR, r"\[ERROR #(\d+)\]")
    d, t = now()
    _append(ERR, "\n".join([
        f"## [ERROR #{no:03d}] {rec.get('title', '')}", "",
        f"- 때: {rec.get('date', d)} {rec.get('time', t)}",
        f"- 어떤 때 나나: {rec.get('when', '')}",
        f"- 겉으로 보이는 것: {rec.get('symptom', '')}",
        f"- 다시 내는 법: {rec.get('repro', '')}",
        f"- 진범: {rec.get('cause', '')}",
        f"- 고침: {rec.get('fix', '')}",
        f"- 어떻게 확인했나: {rec.get('verify', '')}",
        f"- 지금 상태: {rec.get('status', '고침')}"]))
    return no


def add_decision(rec: dict) -> int:
    no = next_no(DEC, r"\[DECISION #(\d+)\]")
    d, _ = now()
    _append(DEC, "\n".join([
        f"## [DECISION #{no:03d}] {rec.get('title', '')}", "",
        f"- 때: {rec.get('date', d)}",
        f"- 무엇이 문제였나: {rec.get('problem', '')}",
        f"- 고를 수 있던 것: {rec.get('options', '')}",
        f"- 고른 것: **{rec.get('chosen', '')}**",
        f"- 까닭: {rec.get('why', '')}",
        f"- 버린 것과 그 까닭: {rec.get('rejected', '')}",
        f"- 영향: {rec.get('impact', '')}",
        f"- 승인: {rec.get('approved', '-')}"]))
    return no


def save_checkpoint(note: str = "") -> None:
    d, t = now()
    s = read_state()
    srv = running_servers()
    _write(CHECKPOINT, f"""# CHECKPOINT

> 작업을 다시 시작할 때 **이것부터** 본다.

- 때: {d} {t}
- 자리: `{ROOT}`
- 판본: {s.get('version', '0.1.0')}
- 돌고 있는 것: {', '.join(f'포트 {p}' for p, _ in srv[:8]) if srv else '없음'}

## 지금 목표
{s.get('current', '-') or '-'}

## 끝난 것
{s.get('done', '-') or '-'}

## 남은 것
{s.get('todo', '-') or '-'}

## 막힌 것
{s.get('blocked', '-') or '-'}

## 마지막 오류
{s.get('error', '-') or '-'}

## 마지막 시험
{s.get('test', '-') or '-'}

## 승인 기다리는 것
{s.get('pending', '-') or '-'}

## 다음에 할 일
{s.get('next', '-') or '-'}

## 잊으면 안 되는 것
{note or '- 돌고 있는 프로그램을 끄지 않는다 (빈 포트를 쓴다)'}
""")


def stats() -> dict:
    def count(p: Path, pat: str) -> int:
        # re.M 이 없으면 0 이 나온다 - 출판 통계가 통째로 틀어진다.
        return len(re.findall(pat, p.read_text(encoding="utf-8"), re.M)) \
            if p.exists() else 0
    pys = [f for f in ROOT.rglob("*.py")
           if not any(x in f.parts for x in
                      (".venv", "venv", "__pycache__", "node_modules",
                       "site-packages"))]
    return {
        "개발 기록": count(DEV, r"\[DEVELOPMENT RECORD #\d+\]"),
        "오류 기록": count(ERR, r"\[ERROR #\d+\]"),
        "시험 기록": count(TEST, r"^\| T\d+ \|"),
        "결정 기록": count(DEC, r"\[DECISION #\d+\]"),
        "파이썬 파일": len(pys),
        "줄 수": sum(len(f.read_text(encoding="utf-8", errors="replace")
                        .splitlines()) for f in pys),
    }



# -- 묶음 풀기 ----------------------------------------------------
# 기록틀 여러 개를 한 파일에 담아 두고 구분선으로 나눠 푼다.
# 구분선:  ===== FILE: 이름.md =====
SPLIT = re.compile(r"^=====\s*FILE:\s*(.+?)\s*=====\s*$", re.M)


def unpack(src: Path, dest: Path) -> list[str]:
    """묶음 파일을 풀어 dest 에 놓는다. **이미 있으면 건너뛴다.**"""
    text = src.read_text(encoding="utf-8")
    parts = SPLIT.split(text)
    if len(parts) < 3:
        raise ValueError(f"{src.name} 에 구분선(===== FILE: ... =====)이 "
                         f"없습니다")
    d, t = now()
    done = []
    # parts = [머리글, 이름1, 내용1, 이름2, 내용2, ...]
    for i in range(1, len(parts) - 1, 2):
        name, body = parts[i].strip(), parts[i + 1]
        body = body.replace("{date}", d).replace("{time}", t)
        target = dest / name
        if target.exists():
            done.append(f"{name}: 이미 있음 - 건너뜀")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        _write(target, body.lstrip("\n"))
        done.append(f"{name}: 만듦")
    return done



# -- 배포 꾸러미를 제자리에 놓기 ------------------------------------
# 🔴 bat 에 한글 파일명을 적으면 콘솔 코드페이지에 따라 깨진다.
#    그래서 **파일을 놓는 일은 여기(파이썬)에서** 한다.
KIT = [
    ("1_CLAUDE_rules.txt", "CLAUDE.md"),
    ("2_quick_rules.txt", "운영규칙.txt"),
    ("3_tool_state.txt", "tools/state.py"),
    ("4_tool_makebook.txt", "tools/makebook.py"),
]
KIT_BUNDLE = [
    ("5_log_templates.txt", "04_LOG"),
    ("6_book_templates.txt", "07_BOOK"),
]


def setup(here: Path) -> int:
    """꾸러미 여섯 파일을 제자리에 놓는다. **있는 것은 건드리지 않는다.**"""
    missing = [n for n, _ in KIT + KIT_BUNDLE if not (here / n).exists()]
    if missing:
        print("  [멈춤] 다음 파일이 이 폴더에 없습니다:")
        for n in missing:
            print(f"         {n}")
        print()
        print("  여섯 파일을 INSTALL.bat 과 **같은 폴더**에 두고 다시 하세요.")
        return 1

    for src, dst in KIT:
        t = here / dst
        if t.exists():
            print(f"  {dst:24} 이미 있음 - 건너뜀")
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        _write(t, (here / src).read_text(encoding="utf-8"))
        print(f"  {dst:24} 만듦")

    for src, folder in KIT_BUNDLE:
        for line in unpack(here / src, here / folder):
            print(f"  {folder}/{line}")

    bat = here / "상태확인.bat"
    if bat.exists():
        print(f"  {'상태확인.bat':24} 이미 있음 - 건너뜀")
    else:
        bat.write_bytes(("@echo off\r\n"
                         'cd /d "%~dp0"\r\n'
                         "python tools\\state.py\r\n"
                         "pause\r\n").encode("cp949"))
        print(f"  {'상태확인.bat':24} 만듦")
    return 0


def ask(fields):
    print("비워 두면 그 칸은 안 적습니다. 그만두려면 Ctrl+C.\n")
    out = {}
    for key, label in fields:
        try:
            out[key] = input(f"  {label}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n그만둡니다.")
            sys.exit(1)
    return out


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    jf = None
    if "--json" in sys.argv:
        jf = json.loads(Path(sys.argv[sys.argv.index("--json") + 1])
                        .read_text(encoding="utf-8"))

    if cmd in ("", "status"):
        print(self_audit())
        print()
        print(STATE.read_text(encoding="utf-8") if STATE.exists()
              else "상태판이 없습니다 - `python tools/state.py init`")
        return

    if cmd == "check":
        ok = True
        for name, good, note in guards():
            print(f"  {'OK ' if good else '!! '} {name:10} {note}")
            ok = ok and good
        srv = running_servers()
        if srv:
            print(f"\n  * 돌고 있는 것: "
                  f"{', '.join(f'포트 {p}' for p, _ in srv[:8])}"
                  f"  <- 끄지 말 것")
        sys.exit(0 if ok else 1)

    if cmd == "init":
        save_state(current="-", done="-", todo="-")
        print(f"세웠습니다: {STATE}")
        return

    if cmd == "log":
        print(f"개발 기록 #{add_dev(jf or ask([(f, DEV_LABEL[f]) for f in DEV_FIELDS])):03d} 적었습니다")
        return
    if cmd == "test":
        rec = jf or ask([("target", "무엇을"), ("how", "어떻게 쟀나"),
                         ("want", "바란 값"), ("got", "실제 값"),
                         ("verdict", "판정")])
        print(f"시험 기록 T{add_test(rec):03d} 적었습니다")
        return
    if cmd == "error":
        rec = jf or ask([("title", "한 줄 이름"), ("when", "어떤 때 나나"),
                         ("symptom", "겉으로 보이는 것"),
                         ("repro", "다시 내는 법"), ("cause", "진범"),
                         ("fix", "고침"), ("verify", "어떻게 확인했나"),
                         ("status", "지금 상태")])
        print(f"오류 기록 #{add_error(rec):03d} 적었습니다")
        return
    if cmd == "decide":
        rec = jf or ask([("title", "한 줄 이름"), ("problem", "문제"),
                         ("options", "고를 수 있던 것"), ("chosen", "고른 것"),
                         ("why", "까닭"), ("rejected", "버린 것"),
                         ("impact", "영향"), ("approved", "승인")])
        print(f"결정 기록 #{add_decision(rec):03d} 적었습니다")
        return
    if cmd == "checkpoint":
        save_checkpoint(" ".join(sys.argv[2:]))
        print(f"재개 지점 저장 -> {CHECKPOINT}")
        return
    if cmd == "set":
        save_state(**dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a))
        print(f"상태판 갱신 -> {STATE}")
        return
    if cmd == "setup":
        here = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 \
            else Path.cwd().resolve()
        sys.exit(setup(here))

    if cmd == "unpack":
        if len(sys.argv) < 4:
            print("쓰기: python tools/state.py unpack <묶음.txt> <놓을 폴더>")
            sys.exit(1)
        src = Path(sys.argv[2])
        dest = ROOT / sys.argv[3]
        if not src.exists():
            src = ROOT / sys.argv[2]
        if not src.exists():
            print(f"그런 파일이 없습니다: {sys.argv[2]}")
            sys.exit(1)
        for line in unpack(src, dest):
            print(f"  {sys.argv[3]}/{line}")
        return

    if cmd == "stats":
        for k, v in stats().items():
            print(f"  {k:10} {v:,}")
        return
    print(__doc__)


if __name__ == "__main__":
    main()
