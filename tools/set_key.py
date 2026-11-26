"""API 키를 내 PC 의 **암호화된 금고**에 넣는다 (파일·화면·기록에 남기지 않음).

쓰기:
    python tools/set_key.py            Gemini API 키 넣기 (입력할 때 화면에 안 보임)
    python tools/set_key.py --check    키가 들어 있는지만 확인 (값은 안 보여 줌)
    python tools/set_key.py --delete   키 지우기

- 윈도: 「자격 증명 관리자」(Windows Credential Manager)에 저장 — 윈도 로그인 계정으로 암호화된다.
  (제어판 → 자격 증명 관리자 → Windows 자격 증명 → "mukjago-homepage" 에서 보거나 지울 수 있음)
- 맥: 키체인, 리눅스: Secret Service 에 저장.
- tools/generate_images.py 는 여기서 키를 꺼내 쓴다. 저장소에는 키가 절대 들어가지 않는다.
- 처음 한 번: pip install -r requirements.txt  (keyring 이 설치됨)
"""
from __future__ import annotations

import getpass
import sys

SERVICE, NAME = "mukjago-homepage", "GEMINI_API_KEY"


def get_key() -> str | None:
    """금고에서 키를 꺼낸다. keyring 이 없거나 비어 있으면 None."""
    try:
        import keyring
        return keyring.get_password(SERVICE, NAME)
    except Exception:
        return None


def main():
    try:
        import keyring
    except ImportError:
        sys.exit("keyring 이 없습니다. 먼저: pip install -r requirements.txt")
    if "--check" in sys.argv:
        k = keyring.get_password(SERVICE, NAME)
        print("들어 있음 (끝 4자리: …" + k[-4:] + ")" if k else "없음")
        return
    if "--delete" in sys.argv:
        try:
            keyring.delete_password(SERVICE, NAME)
            print("지웠습니다.")
        except Exception:
            print("지울 키가 없습니다.")
        return
    print("aistudio.google.com 에서 복사한 Gemini API 키를 붙여 넣고 Enter (화면에는 안 보입니다)")
    k = getpass.getpass("키: ").strip()
    if not k:
        sys.exit("비어 있어 저장하지 않았습니다.")
    keyring.set_password(SERVICE, NAME, k)
    print(f"암호화된 금고에 저장했습니다 ({keyring.get_keyring().__class__.__name__}). 끝 4자리: …{k[-4:]}")


if __name__ == "__main__":
    main()
