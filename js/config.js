/* =============================================================
 * 먹자GO 사이트 설정 — 회사 정보·연락처·배너를 여기서 고칩니다.
 * (이 파일만 고치면 모든 페이지의 머리·바닥글에 함께 바뀝니다)
 * ============================================================= */
window.SITE = {
  name: "먹자GO",
  slogan: "도매가로 만나는 맛있는 세상",

  // 고객센터
  phone: "010-8017-7457",
  hours: "월~금 오전 10시 - 오후 5시 (주말·공휴일 휴무)",
  bank: "기업은행 445-103825-04-013 (주)잇플로우",

  // 카카오톡 오픈채팅 특가방
  // ▶ 오픈채팅 링크(https://open.kakao.com/o/....)를 아래 "" 안에 넣으세요.
  kakaoOpenChat: "",
  kakaoPassword: "1004",

  // 신규회원 웰컴쿠폰 (최대 할인 문구)
  welcomeCoupon: "최대 5,000원",

  // 사업자 정보 (바닥글 — 전자상거래법 표시사항)
  company: {
    name: "주식회사 잇플로우",
    ceo: "양승주, 김지현",
    bizNo: "872-81-03833",
    address: "경상남도 김해시 금관대로 1271, 지하1층(내동)",
    mailOrderNo: "제2026-경남김해-1021호",
    email: "eatflow93@naver.com",
    hosting: "GitHub Pages",
  },

  /* 메인 배너 (1~10장)
   * 이미지 배너: { image: "images/banners/파일이름.jpg", link: "list.html?cat=sea" }
   * 글자 배너  : { title, text, image(배경, 선택), color(배경색), link }
   */
  banners: [
    {
      title: "산지직송 고등어 특가",
      text: "당일 직송, 신선한 고등어 1미 8,900원",
      image: "images/products/mackerel.jpg",
      link: "product.html?id=13",
    },
    {
      title: "도매가 그대로, 매일 특가",
      text: "농·수·축산물부터 간편식품까지 도매가로 만나보세요",
      image: "images/category/farm.jpg",
      color: "#1f5a2a",
      link: "list.html?cat=today",
    },
    {
      title: "카카오톡 특가방 오픈!",
      text: "매일 올라오는 실속 특가, 가장 먼저 받아보세요 (비밀번호 1004)",
      image: "images/category/easy.jpg",
      color: "#ef7d1a",
      link: "#kakao",
    },
  ],
};
