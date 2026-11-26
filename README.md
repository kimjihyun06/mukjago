# 먹자GO 홈페이지

- 저장소: https://github.com/kimjihyun06/mukjago (공개)
- 홈페이지: https://kimjihyun06.github.io/mukjago/

> 도매가로 만나는 맛있는 세상 — 주식회사 잇플로우

빌드 도구 없이 HTML·CSS·JS 만으로 만든 쇼핑몰 홈페이지입니다.
GitHub 에 올리면 **GitHub Pages** 로 바로 배포됩니다 (무료).

---

## 1. 필요한 프로그램 (윈도, 처음 한 번)

| 프로그램 | 쓰는 곳 | 설치 |
|---|---|---|
| **Git** | GitHub 과 주고받기 | https://git-scm.com/download/win |
| **Python 3.12** | 점검·기록 도구 (`tools/`) | https://www.python.org/downloads/ — 설치 첫 화면에서 **Add Python to PATH** 꼭 체크 |
| **VS Code** | 파일 고치기·미리보기 | https://code.visualstudio.com/ |
| **Claude Code** | AI 와 함께 작업 | Claude 데스크톱 앱 또는 https://claude.ai/code |
| GitHub Desktop (선택) | 버튼으로 올리기 | https://desktop.github.com/ |

PowerShell 에서 한 번에 설치하려면 (윈도 10/11):

```bash
winget install Git.Git Python.Python.3.12 Microsoft.VisualStudioCode
```

설치 후 확인:

```bash
git --version
```

```bash
python --version
```

## 2. 내 컴퓨터로 받아오기 (처음 한 번)

```bash
cd C:\Users\Administrator\Desktop\my-hamepage\my-hamepage
```

```bash
git clone https://github.com/kimjihyun06/mukjago.git kimjihyun06-homepage
```

처음 올릴 때 이름·메일을 한 번 정해 둡니다:

```bash
git config --global user.name "김지현"
```

```bash
git config --global user.email "<GitHub 에 등록한 메일>"
```

## 3. 배포 켜기 (처음 한 번, GitHub 웹에서)

1. 저장소 → **Settings** → 왼쪽 **Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `main` / `/ (root)` → **Save**
4. 1~2분 뒤 주소가 뜹니다: **https://kimjihyun06.github.io/mukjago/**

## 4. 매일 작업하는 순서

```text
① 받아오기      git pull                    (다른 사람이 고친 것 먼저 받기)
② 점검          python tools/state.py       (또는 상태확인.bat 더블클릭)
③ 고치기        직접 또는 Claude 에게 부탁
④ 확인          index.html 더블클릭 → 컴퓨터·휴대폰 크기로 보기
⑤ 점검          python tools/state.py check (모두 OK 여야 올림)
⑥ 올리기        git add . → git commit -m "무엇을 바꿨나" → git push
⑦ 기록          python tools/state.py log
```

`main` 에 올라간 것은 1~2분 뒤 **실제 홈페이지에 바로 반영**됩니다.
큰 변경은 새 가지(branch)에서 작업 → Pull Request → 확인 후 합치기를 권합니다.
PR·push 때마다 GitHub Actions 가 점검(`state.py check`)을 자동으로 돌립니다.

## 5. 상품·가격 올리기 (공급표 엑셀)

1. 최신 공급표를 `my-hamepage\자료\엑셀\` 에 넣습니다 (이 저장소 **바깥** 폴더 — 매입가가 공개되지 않게).
2. `상품갱신.bat` 더블클릭 (또는 `python tools/import_excel.py`)
   - 처음 한 번: `pip install -r requirements.txt`
3. 화면 확인 → 올리기

| 엑셀 | 홈페이지 |
|---|---|
| 시트 하나 | 상품 하나 (`product.html?id=번호`, 번호는 `tools/product_ids.json`) |
| 품목명 + 옵션 | 선택 옵션 |
| 실제 판매가 · 택배비 · 면세/과세 · 발주 마감시간 | 그대로 표시 (택배비 0 = 무료배송) |
| 같은 품목 여러 줄 | **일자가 가장 늦은 줄**의 가격 |
| **숨김 시트** | 올리지 않음 (품절·판매중단) |
| 공급가액 · 마진 | **절대 올리지 않음** |

**사진** — 상품 하나의 사진 폴더를 통째로 넣습니다 (번호는 `상품번호표.txt`):

```bash
python tools/import_photos.py "..\자료\엑셀\5 수산물\밥도둑\순살게장" 28
```

그다음 `상품갱신.bat` 을 다시 실행. 크기 줄이기·긴 상세페이지 자르기는 자동입니다.

| 폴더·파일 | 쓰이는 곳 |
|---|---|
| `…썸네일/`, `…대표/` 폴더 안 그림 | 대표사진 |
| `…상세…/` 폴더 안 그림 | 상세페이지 조각 (번호순) |
| 썸네일 폴더가 따로 있을 때 맨 위의 `1.png 2.png…` | 상세페이지 조각 |
| 썸네일 폴더가 없을 때 `1.jpg 2.jpg…`, `대표이미지.jpg` | 대표사진 |
| 세로로 아주 긴 그림 (이름 무관) | 상세페이지 |
카톡·포스터 홍보이미지는 **올리지 않습니다** (공급업체 이름·전화가 들어 있음) — 내용은 `tools/product_info.json` 에 글로 적으면 상단 안내 이미지에 들어갑니다.

| 파일 이름 | 쓰이는 곳 |
|---|---|
| `1.jpg`, `2.jpg`, … (숫자) | 대표사진 (전부, 숫자 순서) |
| `top.jpg` | 상세 맨 위 안내 이미지 — **자동으로 그려짐** (먹자고 / 010-8017-7457, 엑셀 가격) |
| `detail-1.jpg`, `detail-2.jpg`, … | 상세페이지 이미지 (안내 이미지 아래) |

**AI 연출 이미지** — 실제 사진이 아직 없는 상품의 대표사진을 Gemini 로 만듭니다. 사진 구석에 「연출 이미지」가 표시되고, 실제 사진(숫자 이름)을 넣으면 자동으로 실제 사진으로 바뀝니다.

1. aistudio.google.com → Get API key → Create API key → 복사 (이미지 생성은 결제 연결 필요, 한 장 약 50원)
2. 내 PC 의 **암호화된 금고**(윈도 자격 증명 관리자)에 키 넣기 — 한 번만. 키는 파일·대화창·메모에 적지 않습니다:

```bash
pip install -r requirements.txt
```

```bash
python tools/set_key.py
```

   (입력하는 키는 화면에 안 보입니다. `python tools/set_key.py --check` 로 들어 있는지 확인)

3. 만들기:

```bash
python tools/generate_images.py --dry
```

```bash
python tools/generate_images.py
```

4. `상품갱신.bat` 실행. 묘사를 바꾸려면 `tools/ai_prompts.json` 을 고치고 `python tools/generate_images.py --only 3 --force`

## 6. 무엇을 어디서 고치나

| 고칠 것 | 파일 |
|---|---|
| 회사 정보·전화·계좌·**카톡 오픈채팅 링크**·**메인 배너** | `js/config.js` |
| 상품·가격 | 엑셀 → `상품갱신.bat` (`js/products.js` 는 자동 생성) |
| 메뉴·하위 메뉴·첫 화면 Best·후기·공지사항 | `js/content.js` |
| 첫 화면 칸 순서·문구 | `index.html` |
| 색·글꼴·배치 | `css/style.css` |
| 사진 | `images/` (배너 `images/banners/`, 상품 `images/products/`) |

**사진 넣는 법**
1. 사진 파일 이름을 **영문**으로 바꿉니다 (예: `apple-5kg.jpg`). 1MB 이하로.
2. `images/products/` (배너는 `images/banners/`) 에 넣습니다.
3. Claude 에게: *"product.html?id=1 상품 사진을 images/products/apple-5kg.jpg 로 바꿔줘"*


## 7. 협업 체계

| 파일 | 무엇 |
|---|---|
| `CLAUDE.md` | AI 가 지키는 규칙 (Claude Code 가 자동으로 읽음) |
| `운영규칙.txt` | 사람이 보는 한 장 요약 |
| `04_LOG/` | 상태판·개발/오류/시험/결정 기록 |
| `07_BOOK/` | 기록 → 출판 원자료 |
| `tools/state.py` | 상태 보기·점검·기록 명령 |
| `tools/guards_project.py` | 이 홈페이지 전용 점검 (깨진 링크·사진 크기·**민감 자료**) |

> ⚠️ **카드 사진·비밀번호·카톡 원본 자료는 `자료/` 폴더에 두세요.**
> 그 폴더는 GitHub 에 올라가지 않습니다(`.gitignore`). 올라간 것은 전 세계에 공개됩니다.
