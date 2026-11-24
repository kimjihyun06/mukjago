/* =============================================================
 * 상품 목록 — 상품을 더하거나 고칠 때는 이 파일만 고칩니다.
 *
 *  id        : 번호 (겹치면 안 됩니다. 상세페이지 주소 product.html?id=번호)
 *  name      : 상품 이름
 *  cat       : 분류  farm=농산물  meat=축산물  sea=수산물  easy=간편식품
 *  tags      : today=오늘의 특가전 칸   best=실시간 Best 칸
 *  price     : 정가 (원)          sale : 판매가 (원)
 *  unit      : 구성/중량          origin : 원산지
 *  image     : 사진 경로 (images/products/ 에 넣고 적기). 없으면 emoji 로 표시
 *  detail    : 상세페이지 사진들 ["images/products/상세1.jpg", ...] (선택)
 *  desc      : 상품 설명
 *  sample    : true 이면 「예시 상품」 표시가 붙습니다 → 실제 상품으로 바꾸면 지우세요
 * ============================================================= */
window.CATEGORIES = {
  farm: { name: "농산물", title: "실속 담은 농산물 특가", sub: "매일 찾는 기본 식재료, 거품 뺀 도매가로 한번에!" },
  meat: { name: "축산물", title: "진심을 담은 정직한 축산", sub: "보이는 그대로 알차게, 정직하게 고른 고기." },
  sea:  { name: "수산물", title: "산지직송 수산의 반격", sub: "바다 건너 식탁 직행, 산지에서 바로 보내드립니다!" },
  easy: { name: "간편식품", title: "든든한 간편식품", sub: "밀키트·냉동 간편식, 도매가로 쟁여두세요!" },
};

window.PRODUCTS = [
  // ---------- 농산물 ----------
  { id: 1, cat: "farm", tags: ["today"], name: "제철 꿀사과 5kg (중과)", price: 39900, sale: 29900, unit: "5kg / 16~18과", origin: "국내산(경북)", emoji: "🍎", desc: "아삭하고 달콤한 제철 사과를 도매가로 보내드립니다.", sample: true },
  { id: 2, cat: "farm", tags: ["best"], name: "하우스 감귤 3kg", price: 24900, sale: 17900, unit: "3kg", origin: "국내산(제주)", emoji: "🍊", desc: "새콤달콤 제주 감귤.", sample: true },
  { id: 3, cat: "farm", tags: [], name: "친환경 브로콜리 1kg", price: 12900, sale: 8900, unit: "1kg (3~4송이)", origin: "국내산", emoji: "🥦", desc: "단단하고 싱싱한 브로콜리.", sample: true },
  { id: 4, cat: "farm", tags: ["today"], name: "샤인머스캣 2kg", price: 35900, sale: 25900, unit: "2kg (3~4송이)", origin: "국내산(경북)", emoji: "🍇", desc: "향 좋고 당도 높은 샤인머스캣.", sample: true },
  { id: 5, cat: "farm", tags: [], name: "햇양파 5kg", price: 11900, sale: 7900, unit: "5kg", origin: "국내산(전남)", emoji: "🧅", desc: "매일 쓰는 기본 식재료.", sample: true },
  { id: 6, cat: "farm", tags: ["best"], name: "논산 딸기 1kg", price: 21900, sale: 15900, unit: "1kg (2팩)", origin: "국내산(충남)", emoji: "🍓", desc: "향긋한 설향 딸기.", sample: true },

  // ---------- 축산물 ----------
  { id: 7, cat: "meat", tags: ["best"], name: "한돈 삼겹살 1kg", price: 32900, sale: 23900, unit: "1kg (500g×2)", origin: "국내산", emoji: "🥓", desc: "두께 그대로, 정직하게 고른 한돈 삼겹살.", sample: true },
  { id: 8, cat: "meat", tags: ["today"], name: "1+등급 한우 등심 500g", price: 69900, sale: 54900, unit: "500g", origin: "국내산(한우)", emoji: "🥩", desc: "마블링 좋은 1+등급 한우 등심.", sample: true },
  { id: 9, cat: "meat", tags: [], name: "통닭 (생닭) 1.1kg × 2", price: 15900, sale: 11900, unit: "1.1kg × 2마리", origin: "국내산", emoji: "🍗", desc: "백숙·치킨용 신선 생닭.", sample: true },
  { id: 10, cat: "meat", tags: [], name: "한돈 목살 1kg", price: 31900, sale: 22900, unit: "1kg", origin: "국내산", emoji: "🍖", desc: "구이용 두툼한 목살.", sample: true },
  { id: 11, cat: "meat", tags: ["best"], name: "LA갈비 2kg", price: 59900, sale: 44900, unit: "2kg", origin: "미국산", emoji: "🍖", desc: "명절·캠핑용 LA갈비.", sample: true },
  { id: 12, cat: "meat", tags: [], name: "오리 슬라이스 1kg", price: 19900, sale: 14900, unit: "1kg", origin: "국내산", emoji: "🦆", desc: "간편 구이용 오리 슬라이스.", sample: true },

  // ---------- 수산물 ----------
  { id: 13, cat: "sea", tags: ["today", "best"], name: "당일 직송 신선한 고등어 1미", price: 12900, sale: 8900, unit: "1미", origin: "국내산", image: "images/products/mackerel.jpg", desc: "산지에서 당일 직송한 신선한 고등어입니다." },
  { id: 14, cat: "sea", tags: [], name: "완도 활전복 1kg (중)", price: 49900, sale: 36900, unit: "1kg (12~14미)", origin: "국내산(완도)", emoji: "🐚", desc: "살아있는 완도 전복.", sample: true },
  { id: 15, cat: "sea", tags: ["best"], name: "흰다리 새우 1kg", price: 24900, sale: 17900, unit: "1kg (40~50미)", origin: "에콰도르산", emoji: "🦐", desc: "구이·찜용 냉동 흰다리 새우.", sample: true },
  { id: 16, cat: "sea", tags: [], name: "노르웨이 생연어 500g", price: 29900, sale: 21900, unit: "500g", origin: "노르웨이산", emoji: "🐟", desc: "회·스테이크용 생연어.", sample: true },

  // ---------- 간편식품 ----------
  { id: 17, cat: "easy", tags: ["today"], name: "부대찌개 밀키트 2~3인분", price: 15900, sale: 9900, unit: "1팩 (2~3인분)", origin: "국내 제조", emoji: "🍲", desc: "끓이기만 하면 완성되는 밀키트.", sample: true },
  { id: 18, cat: "easy", tags: ["best"], name: "왕교자 만두 1.4kg × 2", price: 19900, sale: 13900, unit: "1.4kg × 2봉", origin: "국내 제조", emoji: "🥟", desc: "속이 꽉 찬 냉동 왕교자.", sample: true },
  { id: 19, cat: "easy", tags: [], name: "양념 소불고기 1kg", price: 21900, sale: 15900, unit: "1kg", origin: "국내 제조", emoji: "🥘", desc: "데우기만 하면 되는 양념 불고기.", sample: true },
  { id: 20, cat: "easy", tags: [], name: "냉동 피자 3판", price: 17900, sale: 12900, unit: "3판", origin: "국내 제조", emoji: "🍕", desc: "에어프라이어로 간편하게.", sample: true },
];

/* 고객 후기 — 실제 후기를 받으면 여기에 적으세요 (예시는 sample: true) */
window.REVIEWS = [
  { productId: 13, name: "김**", stars: 5, text: "고등어가 정말 싱싱해요. 구워 먹으니 살이 통통합니다!", sample: true },
  { productId: 7, name: "이**", stars: 5, text: "삼겹살 두께가 좋고 잡내가 없어요. 재구매 의사 있습니다.", sample: true },
  { productId: 1, name: "박**", stars: 4, text: "사과가 아삭하고 달아요. 가격 대비 아주 만족합니다.", sample: true },
  { productId: 18, name: "최**", stars: 5, text: "만두 속이 꽉 차 있어서 아이들이 좋아해요.", sample: true },
];

/* 공지사항 — 위가 최신 */
window.NOTICES = [
  { date: "2026-11-24", title: "먹자GO 홈페이지를 열었습니다", body: "도매가로 만나는 맛있는 세상, 먹자GO 입니다. 주문·문의는 카카오톡 특가방 또는 고객센터(010-8017-7457, 평일 10~17시)로 해 주세요." },
  { date: "2026-11-24", title: "주문·문의 방법 안내", body: "현재 주문은 카카오톡 오픈채팅 특가방(비밀번호 1004)과 고객센터 전화로 받고 있습니다. 장바구니에 담은 상품 목록을 보여 주시면 빠르게 안내해 드립니다." },
];
