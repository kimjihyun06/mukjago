# DEVELOPMENT LOG

> 번호는 **지우거나 다시 쓰지 않는다.** 100 에서 끝내지 않고 계속 쌓는다.
> 한 건 적으려면: `python tools/state.py log`

==========================================================
[DEVELOPMENT RECORD #001]

DATE: 2026-11-24
TIME: 09:05

[USER] 사용자 지시
이 폴더에 홈페이지를 만들어서 깃허브에 올려 배포. 필요한 프로그램·환경·협업체계를 이 환경에 맞춰 설정하고 진행

[CONTEXT] 그때 상황
손그림 시안 4장(머리글·배너·특가·Best·농/축/수산·카톡방·후기·바닥글), 로고, 고등어 사진, 카톡 특가방 포스터, 사업자등록증, 협업체계 꾸러미(배포_협업체계) 받음. 클라우드 Claude Code 에서 작업

[ANALYSIS] 분석
기존 index/product.html 은 대표님 PC 에만 있고 받지 못함 → 시안대로 새로 만듦. 실제 상품·가격 자료가 없어 고등어 1건(8,900원) 외에는 예시 상품으로 채우고 「예시 상품」 표시

[PLAN] 계획
정적 사이트 → 협업체계 설치 → 전용 걸쇠 → CI·템플릿 → 기록 → GitHub 올리기

[EXECUTION] 실제 한 일
index/list/product/cart/notice/terms/privacy 7쪽, js/config.js·products.js·app.js, css/style.css, images 6개 작성. 협업체계 꾸러미를 state.py setup 으로 설치하고 CLAUDE.md 자리표시자 채움. tools/guards_project.py(링크·상품번호·사진·민감자료), .github/workflows/check.yml, PR·이슈 틀, README, .gitignore, .nojekyll

[FILES] 건드린 파일
*.html, js/*, css/style.css, images/*, CLAUDE.md, 운영규칙.txt, tools/*, 04_LOG/*, 07_BOOK/*, .github/*, README.md, .gitignore

[ERROR] 오류
① 상세페이지 가격 왼쪽에 큰 빈칸 ② 걸쇠가 설명 속 보기 경로와 카톡 참여코드 1004 를 문제로 잡음

[ROOT CAUSE] 진범
① 버튼용 .big 클래스(padding)가 가격 p 에도 붙음 ② 주석을 안 걸러냄, 비밀번호 꼴 길이 기준이 너무 짧음

[FIX] 고침
① price lg 로 이름 바꿈 ② 주석 제거 후 검사, 값 8자 이상만

[TEST] 어떻게 쟀나
TEST_LOG T001~T004

[RESULT] 결과
걸쇠 9/9 OK, 가로 넘침 0, JS 오류 0

[DECISION] 정한 것
DECISION #001, #002

[NEXT] 다음
GitHub 저장소 이름 확인 → push → Pages 켜기 → 실제 주소에서 다시 측정

==========================================================

==========================================================
[DEVELOPMENT RECORD #002]

DATE: 2026-11-26
TIME: 03:57

[USER] 사용자 지시
공급표 엑셀(늘푸른우리 제품 공급표_잇플로우)의 시트별 실제판매가·택배비·면세/과세·품목명으로 홈페이지 작성. 숫자 이름 이미지는 전부 대표사진, 카톡 이미지는 상세 맨 위에 (먹자고/010-8017-7457, 저작권 안 걸리게 새로 만들어), 없으면 자리만, 그 아래 상세 이미지 그대로. 자동 원격 진행

[CONTEXT] 그때 상황
엑셀 1개만 업로드됨(62시트). D: 드라이브의 사진 폴더는 받지 못함 → 사진 자리·자동 연결 장치만 만들고 실제 사진은 아직 없음

[ANALYSIS] 분석
시트=상품, 날짜별 가격 이력, 숨김 11시트=품절/중단. 공급가액·마진은 비공개여야 함

[PLAN] 계획
엑셀 읽기 스크립트 → 상단 안내 이미지 생성 → 화면 개편 → 검산·측정

[EXECUTION] 실제 한 일
tools/import_excel.py, tools/make_top_images.py(Pretendard OFL 글꼴 동봉), js/content.js 분리, app.js 옵션·택배비·과세·갤러리·상세 순서 개편, 배너 교체, 예시 상품/후기/고등어 사진 삭제, 걸쇠 「매입정보」 추가, 상품갱신.bat, 상품번호표.txt, requirements.txt

[FILES] 건드린 파일
tools/import_excel.py, tools/make_top_images.py, tools/fonts/*, tools/product_ids.json, tools/guards_project.py, js/products.js(자동), js/content.js, js/app.js, js/config.js, css/style.css, *.html, images/products/pNN/top.jpg ×51, README.md, CLAUDE.md, 상품갱신.bat, 상품번호표.txt

[ERROR] 오류
옵션 합쳐짐(ERROR #001), 걸쇠 오탐 2건(문서 속 보기 경로, 파일명 supply), 김치에 김(🍙) 그림

[ROOT CAUSE] 진범
열쇠 설계, 걸쇠 기준 넓음, 그림글자 검색 순서

[FIX] 고침
(품목명,옵션) 열쇠, 걸쇠 기준 좁힘, 김치를 먼저 검사

[TEST] 어떻게 쟀나
TEST_LOG T005~T010

[RESULT] 결과
상품 51·옵션 225, 엑셀과 불일치 0, 걸쇠 10/10, 넘침 0, 오류 0

[DECISION] 정한 것
DECISION #003~#005

[NEXT] 다음
사진 zip 받기 → images/products/pNN/ 에 배치 → import 다시. GitHub 저장소 주소 받기

==========================================================

==========================================================
[DEVELOPMENT RECORD #003]

DATE: 2026-11-26
TIME: 04:07

[USER] 사용자 지시
밥도둑 폴더 사진 zip 8개 전달 (간장게장·순살게장·양념게장·곱창김·삼점암꽃게장·새꼬막무침·생굴무침·새우장)

[CONTEXT] 그때 상황
앞선 zip 5개는 빈 폴더였음. 이번 zip 은 이름이 깨져 와서 안의 상세페이지 파일 이름으로 상품을 맞춤

[ANALYSIS] 분석
상세페이지는 폭 860~1000, 세로 18,000~25,000px (6~13MB). 숫자사진 일부 6MB/4000px. 홍보이미지는 전부 공급업체 상호·전화 포함

[PLAN] 계획
사진 넣기 도구 → 8상품 배치 → 홍보이미지 사실만 옮겨 다시 그림 → 측정

[EXECUTION] 실제 한 일
tools/import_photos.py (대표 맨앞, 숫자순, 상세 2000px 조각, 1MB 이하, 홍보이미지 제외), tools/product_info.json (14·23·24·30), make_top_images 에 특징 칸, 상세페이지에 특징·원산지·택배 표시

[FILES] 건드린 파일
tools/import_photos.py, tools/product_info.json, tools/import_excel.py, tools/make_top_images.py, js/app.js, css/style.css, images/products/p14,p23~p25,p27~p30/*, js/products.js, 상품번호표.txt, CLAUDE.md, README.md

[ERROR] 오류
ERROR #002 휴대폰 가로 넘침

[ROOT CAUSE] 진범
그리드 min-width

[FIX] 고침
.pd > * { min-width: 0 }

[TEST] 어떻게 쟀나
T011~T013

[RESULT] 결과
8상품 대표사진 77장·상세 89조각, 깨진 그림 0, 넘침 0, 걸쇠 10/10

[DECISION] 정한 것
DECISION #006

[NEXT] 다음
나머지 43상품 사진, 26번(하프절단 간장게장) 사진 없음, GitHub 주소

==========================================================

==========================================================
[DEVELOPMENT RECORD #004]

DATE: 2026-11-26
TIME: 04:09

[USER] 사용자 지시
하프절단 간장게장 사진 zip 3개 (11.jpg, 12.jpg 따로 보냄)

[CONTEXT] 그때 상황
윈도 복사본 이름 「7 (1).jpg」「8 (1).jpg」 가 섞여 옴. 6000×4000 원본 사진 4장(12~14MB)

[ANALYSIS] 분석
기존 규칙(이름 전체가 숫자)으로는 「7 (1)」 이 숫자 사진으로 잡히지 않아 홍보이미지로 빠질 뻔함

[EXECUTION] 실제 한 일
import_photos.py 가 「N (k)」 도 숫자 사진으로 보고 N 다음 순서에 놓게 고침. p26 배치, 상세페이지 위·중간·아래 확인(다른 업체 상호·번호 없음)

[FILES] 건드린 파일
tools/import_photos.py, images/products/p26/*, js/products.js, 상품번호표.txt

[TEST] 어떻게 쟀나
T014

[RESULT] 결과
사진 있는 상품 9/51, 걸쇠 10/10

[NEXT] 다음
나머지 42상품 사진, GitHub 주소

==========================================================

==========================================================
[DEVELOPMENT RECORD #005]

DATE: 2026-11-26
TIME: 04:17

[USER] 사용자 지시
제철 수산물 폴더 zip 4개 (홍게·과메기·백고동·참조기)

[CONTEXT] 그때 상황
백고동(백골뱅이)은 엑셀에서 숨김 시트(판매중단). 참조기는 숫자 사진 없이 카톡 사진·포스터만

[ANALYSIS] 분석
홍게 포스터가 이름에 「상세」를 달고 있어 상세로 오인될 수 있었음. 홍게 상세 2장은 옵션별 같은 내용

[EXECUTION] 실제 한 일
상세 판정을 모양 기준으로, 택배비 「-」 규칙, 홍게·참조기 사실을 product_info 에 옮겨 안내 이미지에 반영(홍게 중량 주의문 빨간 글씨), 과메기·홍게 사진 배치. 백고동은 판매 상품이 아니라 올리지 않음. 참조기 카톡 사진은 규칙대로 올리지 않음

[FILES] 건드린 파일
tools/import_photos.py, tools/import_excel.py, tools/make_top_images.py, tools/product_info.json, js/app.js, css/style.css, images/products/p11,p15/*, p12/top.jpg

[TEST] 어떻게 쟀나
T015

[RESULT] 결과
사진 있는 상품 11/51

[DECISION] 정한 것
DECISION #007, #008

[NEXT] 다음
참조기 대표사진 여부 확인, 나머지 40상품

==========================================================

==========================================================
[DEVELOPMENT RECORD #006]

DATE: 2026-11-26
TIME: 04:21

[USER] 사용자 지시
제철 수산물 zip 2개 (하모샤브샤브, 국내산 방어필렛) — 이번엔 하위 폴더 구조

[CONTEXT] 그때 상황
하모: 맨 위 1~8.png(860×1100 상세 조각) + 하모샤브샤브썸네일/1~5 + 포스터 + 카톡 폴더. 방어: 대방어 상세페이지/(조각 9 + 맛있게 즐기기) + 대방어 썸네일/2,4

[ANALYSIS] 분석
기존 규칙(숫자=대표)이면 하모 상세 조각 8장이 대표사진으로 잘못 들어감. 압축이 폴더 하나로 감싸져 와서 맨 위 판단도 틀어짐(처음 시험에서 하모 조각 8장이 전부 제외됨 — 확인 후 고침)

[EXECUTION] 실제 한 일
import_photos.py: 하위 폴더 탐색, 썸네일/대표 폴더=대표, 상세 폴더=조각, 썸네일 폴더 있으면 맨 위 숫자=조각, 감싼 폴더 자동 진입. 하모(포스터)·방어(상세 조각) 사실을 product_info 에 옮김

[FILES] 건드린 파일
tools/import_photos.py, tools/product_info.json, images/products/p17,p18/*, README.md

[TEST] 어떻게 쟀나
T016

[RESULT] 결과
사진 있는 상품 13/51

[NEXT] 다음
하모 상세 3번 조각에 「우리농축산의 하모 샤브샤브」 문구(전화번호 없음) — 둘지 사용자 확인

==========================================================

==========================================================
[DEVELOPMENT RECORD #007]

DATE: 2026-11-26
TIME: 04:24

[USER] 사용자 지시
메뉴 시안 이미지 + 자료 폴더(1 전체상품 ~ 8 입점문의) 대로 김치류 추가, 하위 메뉴·상세까지 폴더·엑셀 참조해 수정

[CONTEXT] 그때 상황
농산물·김치류의 하위 폴더 내용은 아직 받지 못함

[EXECUTION] 실제 한 일
content.js CATEGORIES 를 farm·meat·sea·kimchi·easy 로 (폴더 순서), 각 하위 메뉴와 상품명 낱말 규칙. import_excel 의 수산(과세)→easy 규칙 제거(수산물로). 드롭다운 메뉴(데스크톱 hover/focus, 휴대폰 펼침), 목록 하위 탭·개수, 상세 위치에 하위 메뉴, 첫 화면 칸을 메뉴 순서·빈 분류 숨김

[FILES] 건드린 파일
js/content.js, js/app.js, css/style.css, list.html, index.html, tools/import_excel.py, js/products.js, CLAUDE.md, README.md

[ERROR] 오류
CSS 「2번째 메뉴 빨강」 규칙이 드롭다운 2번째 칸에도 걸림 → 지움. 국탕류 낱말 「국」이 「국내산」에 걸릴 뻔 → 국밥·탕·찌개·육개장

[TEST] 어떻게 쟀나
T017

[RESULT] 결과
8메뉴, 하위 14칸, 51상품 배정, 넘침·오류 0, 걸쇠 10/10

[DECISION] 정한 것
DECISION #009

[NEXT] 다음
농산물·김치류 하위 폴더 이름 확인, 축산물·간편식품 상품 엑셀

==========================================================

==========================================================
[DEVELOPMENT RECORD #008]

DATE: 2026-11-26
TIME: 05:00

[USER] 사용자 지시
농산물 하위=신선채소·제철 과일, 김치류 하위=배추김치·기타김치류. 참조기 카톡 사진은 상세로 추가(대표는 숫자 사진). 홍게 5kg 상세는 추가 안 함

[EXECUTION] 실제 한 일
content.js 하위 메뉴 교체(제철 과일에 과일 이름 낱말 미리 넣음 — 지금 엑셀엔 과일 없음), import_photos.py --kakao-detail 선택 추가(카톡 이름의 실물 사진만, 포스터는 계속 제외), p12 상세 5장

[FILES] 건드린 파일
js/content.js, tools/import_photos.py, images/products/p12/detail-1~5.jpg, js/products.js, 상품번호표.txt

[TEST] 어떻게 쟀나
T018

[RESULT] 결과
하모 상세 「우리농축산의」 조각은 상세로 그대로 둠(사용자 답 3 「상세페이지로 사용」으로 해석 — 확인 필요)

[NEXT] 다음
사용자 새 요청: 필요한 이미지 API 자동 생성 — 업체·비용 승인과 열쇠 필요

==========================================================

==========================================================
[DEVELOPMENT RECORD #009]

DATE: 2026-11-26
TIME: 05:12

[USER] 사용자 지시
필요한 이미지는 api 를 이용해서 자동 생성 (Gemini, 연출 이미지 표시, 대표사진 38개)

[CONTEXT] 그때 상황
열쇠는 네트워크 비밀값으로 저장(프록시가 붙임, 값은 보지 않음). 입력창 2번 닫힘 → 사용자가 다시 띄워 달라 해서 3번째에 저장됨

[EXECUTION] 실제 한 일
tools/ai_prompts.json(상품별 영어 묘사), tools/generate_images.py(이미 있으면 건너뜀·429 재시도·--dry/--only/--force), import_excel 이 실제 사진 없을 때만 ai-1.jpg 를 대표로 + ai 표시, app.js·css 「연출 이미지」 딱지

[FILES] 건드린 파일
tools/ai_prompts.json, tools/generate_images.py, tools/import_excel.py, js/app.js, css/style.css, images/products/pNN/ai-1.jpg ×38, js/products.js, README.md, CLAUDE.md

[ERROR] 오류
대게가 킹크랩으로, 봄동이 배추로 그려짐

[ROOT CAUSE] 진범
대게 묘사에 king crab 낱말이 섞임 / 봄동 모양 묘사 부족

[FIX] 고침
묘사 고쳐 그 상품만 --force

[TEST] 어떻게 쟀나
T019

[RESULT] 결과
대표사진 51/51, 생성 40장 약 $1.60

[NEXT] 다음
사용자 PC(D:) 에 반영 — zip 받아 덮어쓰기 또는 GitHub 연결

==========================================================

==========================================================
[DEVELOPMENT RECORD #010]

DATE: 2026-11-26
TIME: 05:20

[USER] 사용자 지시
GitHub 연결해서 진행, 저장소 만들어 달라, 공개로, API 키·암호는 암호화

[EXECUTION] 실제 한 일
gh api 로 kimjihyun06/kimjihyun06-homepage 생성(이 세션은 비공개만 가능), add_repo, main 푸시(9커밋). 공개 전환은 프록시가 설정 쓰기를 막아 실패 → 사용자가 Settings 에서. 공개 전 기록 전체 검사. tools/set_key.py(keyring) 추가

[FILES] 건드린 파일
tools/set_key.py, tools/generate_images.py, requirements.txt, README.md, CLAUDE.md

[ERROR] 오류
저장소 공개 전환 HTTP 403 (Repository settings writes are not permitted through this proxy)

[FIX] 고침
사용자가 직접 Settings → General → Change visibility

[TEST] 어떻게 쟀나
T020

[NEXT] 다음
사용자: 공개 전환 → Pages 켜기 → 배포 주소 확인

==========================================================

==========================================================
[DEVELOPMENT RECORD #011]

DATE: 2026-11-26
TIME: 05:28

[USER] 사용자 지시
https://github.com/kimjihyun06/mukjago 공개 저장소에 올려 배포 (원격 자동)

[CONTEXT] 그때 상황
사용자가 직접 만든 공개 빈 저장소. 배포 지시 = 승인

[EXECUTION] 실제 한 일
mukjago 에 main 푸시(커밋 그대로, 걸쇠 10/10). Pages 켜기 API 는 프록시가 막음(403) → 사용자 클릭 필요. README 를 mukjago 주소로, main 의 기본 올림 대상을 mukjago 로

[FILES] 건드린 파일
README.md, 04_LOG/*

[ERROR] 오류
POST repos/kimjihyun06/mukjago/pages → HTTP 403 (Access to this GitHub API path is not permitted through this proxy)

[FIX] 고침
사용자가 Settings → Pages 에서 main / (root) 저장

[NEXT] 다음
Pages 켜진 뒤 https://kimjihyun06.github.io/mukjago/ 실측

==========================================================

==========================================================
[DEVELOPMENT RECORD #012]

DATE: 2026-11-26
TIME: 05:46

[USER] 사용자 지시
자료\엑셀 폴더에 상세페이지 이미지가 있으면 홈페이지에 넣어야 하는데 없다 (국내산 햇밤). 전 품목 확인해서 연결

[CONTEXT] 그때 상황
클라우드 세션은 PC(D:) 를 못 봄. 받은 것은 대화창 캡처(91×2000 축소본)뿐이라 쓸 수 없음. 연결된 PC 폴더 0

[EXECUTION] 실제 한 일
tools/import_all_photos.py (자료 폴더 전체 → 폴더 이름으로 상품 짝짓기, 애매하면 보류, 원래 이름으로 동점 가르기), 사진전체갱신.bat (git pull → 미리보기 → 확인 → 연결 → 점검 → 확인 → push), product_info 에 kakao_detail·skip_files 저장, import_photos AI 유지 규칙

[FILES] 건드린 파일
tools/import_all_photos.py, tools/import_photos.py, tools/product_info.json, 사진전체갱신.bat, README.md, CLAUDE.md

[ERROR] 오류
ERROR #003

[TEST] 어떻게 쟀나
T024

[RESULT] 결과
도구는 준비됨. 실제 전 품목 연결은 PC 에서 bat 실행 또는 Remote Control 연결 후

[NEXT] 다음
사용자: PC 에서 사진전체갱신.bat 또는 Remote Control 연결

==========================================================

==========================================================
[DEVELOPMENT RECORD #013]

DATE: 2026-11-26
TIME: 06:37

[USER] 사용자 지시
모든 필요한 프로그램과 환경을 구축해두세요

[CONTEXT] 그때 상황
사용자 PC 에 Claude Code 설치·로그인 완료(D:\my-hamepage\my-hamepage). PC 의 Claude 가 git·python 이 없음을 찾아 설치 허락을 묻는 중. 클라우드 세션은 PC 에 직접 설치 불가

[EXECUTION] 실제 한 일
tools/setup_windows.ps1 (winget 으로 Git·Python 3.12·VS Code, Claude PATH, 홈페이지 clone 또는 pull·옛 폴더 보관, pip requirements, git 사용자·core.quotepath, state.py check, 자료 폴더 확인). UTF-8 BOM·CRLF. README 0장, CLAUDE.md 표

[FILES] 건드린 파일
tools/setup_windows.ps1, README.md, CLAUDE.md

[TEST] 어떻게 쟀나
PowerShell 이 클라우드에 없어 구문 검사·실행 못 함 (확인 필요: PC 에서 실행 결과)

[NEXT] 다음
PC 의 Claude Code 가 스크립트를 받아 실행 → 결과 확인 → import_all_photos --dry

==========================================================

==========================================================
[DEVELOPMENT RECORD #014]

DATE: 2026-11-26
TIME: 16:44

[USER] 사용자 지시
엑셀을 제1원칙으로 자료\엑셀 폴더 사진을 전 품목에 연결 (클라우드 세션이 전달, 확인 필요 폴더와 push 는 대표님께 먼저 묻기)

[CONTEXT] 그때 상황
PC D:\my-hamepage\my-hamepage 에서 setup_windows.ps1 로 새로 clone. 최신 엑셀 늘푸른우리 제품 공급표_잇플로우.xlsx: 시트 62개 (보임 51, 숨김 11)

[ANALYSIS] 분석
import_all_photos --dry: 연결 49개, 확인 필요 8개. 엑셀 대조 결과 확인 필요 8개 중 5개는 숨김 시트이거나 시트가 없음 (활 바지락, 백고동, 특가 급냉암꽃게, 특가속초 박달홍게는 숨김 / 절임배추는 시트 없음)

[PLAN] 계획
49개만 연결. 확인 필요 8개와 p57(꿀고구마+베니하루카 폴더 공용)은 대표님 답을 받은 뒤에

[EXECUTION] 실제 한 일
실행함: git 가지 photos-all-20261126 / python tools/import_all_photos.py (안에서 import_excel.py 도 실행됨) / python tools/state.py check

[FILES] 건드린 파일
images/products/pNN/* (49개 상품), js/products.js

[TEST] 어떻게 쟀나
작업 전 js/products.js 사본과 작업 후를 비교해 쟀다. state.py check 10개 모두 OK

[RESULT] 결과
상품 51→51, 옵션 225→225, 가격 바뀐 옵션 0, 실제 대표사진 있는 상품 13→43, 상세 있는 상품 14→50, AI 연출 대표 38→8 (12,37,43,46,49,51,53,57). p45 햇밤: 대표 8장, 상세 10조각

[DECISION] 정한 것
확인 필요 폴더는 대표님 확인 전에는 연결하지 않는다 (대표님이 직접 지시함)

[NEXT] 다음
확인 필요 8개와 p57 답 받기 → 연결 → push 허락 받기

==========================================================
