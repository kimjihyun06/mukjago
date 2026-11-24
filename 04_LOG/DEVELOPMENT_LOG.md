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
