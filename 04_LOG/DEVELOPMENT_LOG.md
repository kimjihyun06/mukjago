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
