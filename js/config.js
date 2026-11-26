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
   * 글자 배너  : { title, text, image(배경, 선택), emoji(큰 그림글자, 선택), color(배경색), link }
   */
  banners: [
    {
      title: "산지직송 통영 생굴",
      text: "바다에서 식탁까지, 오늘 주문하고 신선하게 받아보세요",
      emoji: "🦪",
      color: "#1d4e6b",
      link: "product.html?id=3",
    },
    {
      title: "26년 햇 꿀고구마 · 꿀밤고구마",
      text: "한입 크기부터 왕대까지, 무료배송 도매가",
      image: "images/category/farm.jpg",
      color: "#2c5a1c",
      link: "list.html?cat=farm",
    },
    {
      title: "국산 김치 무료배송",
      text: "포기김치·백김치·묵은지·파김치, 도매가로 넉넉하게",
      emoji: "🥬",
      color: "#b3361f",
      link: "list.html?cat=kimchi",
    },
    {
      title: "카카오톡 특가방 오픈!",
      text: "매일 올라오는 실속 특가, 가장 먼저 받아보세요 (비밀번호 1004)",
      emoji: "💬",
      color: "#ef7d1a",
      link: "#kakao",
    },
  ],
};
