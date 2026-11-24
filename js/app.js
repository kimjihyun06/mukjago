/* 먹자GO 공통 스크립트 — 머리글·바닥글·장바구니·상품 카드·각 페이지 동작
 * 회사 정보는 js/config.js, 상품은 js/products.js 에서 고칩니다. */
(function () {
  "use strict";
  const S = window.SITE, P = window.PRODUCTS || [], C = window.CATEGORIES || {};
  const $ = (q, el = document) => el.querySelector(q);
  const won = (n) => Number(n).toLocaleString("ko-KR") + "원";
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pct = (p) => (p.price > p.sale ? Math.round((1 - p.sale / p.price) * 100) : 0);
  const byId = (id) => P.find((p) => String(p.id) === String(id));
  const params = new URLSearchParams(location.search);

  /* ---------- 저장 (브라우저에만 저장) ---------- */
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  const cart = {
    all: () => store.get("mg_cart", []),
    save(v) { store.set("mg_cart", v); updateBadges(); },
    add(id, qty = 1) {
      const c = cart.all(); const it = c.find((x) => x.id === id);
      it ? (it.qty += qty) : c.push({ id, qty }); cart.save(c);
    },
    count: () => cart.all().reduce((a, x) => a + x.qty, 0),
  };
  const wish = {
    all: () => store.get("mg_wish", []),
    toggle(id) {
      const w = wish.all(); const i = w.indexOf(id);
      i >= 0 ? w.splice(i, 1) : w.push(id); store.set("mg_wish", w); updateBadges(); return i < 0;
    },
    has: (id) => wish.all().includes(id),
  };

  /* ---------- 알림 ---------- */
  function toast(msg) {
    let t = $("#toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 2200);
  }
  function openKakao(e) {
    if (e) e.preventDefault();
    if (S.kakaoOpenChat) window.open(S.kakaoOpenChat, "_blank", "noopener");
    else toast(`카카오톡 특가방 링크 준비 중입니다. 고객센터 ${S.phone} 로 문의해 주세요.`);
  }
  window.MG = { toast, openKakao, cart, wish };

  /* ---------- 머리글 ---------- */
  function header() {
    const navs = [
      ["list.html", "전체상품", "all"], ["list.html?cat=today", "오늘의특가", "today"],
      ["list.html?cat=farm", "농산물", "farm"], ["list.html?cat=meat", "축산물", "meat"],
      ["list.html?cat=sea", "수산물", "sea"], ["list.html?cat=easy", "간편식품", "easy"],
      ["notice.html#partner", "입점문의", "partner"],
    ];
    const cur = params.get("cat") || (location.pathname.endsWith("list.html") ? "all" : "");
    return `
    <div class="topbar"><div class="wrap">
      <a href="#" data-member>로그인</a><span>|</span>
      <a href="#" data-member class="join">회원가입<em class="bubble">${esc(S.welcomeCoupon)} 쿠폰</em></a><span>|</span>
      <a href="notice.html">고객센터</a>
    </div></div>
    <div class="logo-row wrap">
      <a href="index.html" class="logo" aria-label="${esc(S.name)} 홈"><img src="images/logo.png" alt="${esc(S.name)} - ${esc(S.slogan)}" width="360" height="175"></a>
    </div>
    <nav class="gnb" aria-label="주 메뉴"><div class="wrap">
      <button class="menu-btn" aria-label="메뉴 열기" aria-expanded="false">☰</button>
      <ul class="gnb-list">${navs.map(([h, t, k], i) =>
        `<li><a href="${h}"${k === cur ? ' aria-current="page"' : ""}>${i === 0 ? "<b>≡</b> " : ""}${t}</a></li>`).join("")}</ul>
      <form class="search" action="list.html" role="search">
        <input name="q" type="search" placeholder="검색" aria-label="상품 검색" value="${esc(params.get("q") || "")}">
        <button aria-label="검색">🔍</button>
      </form>
      <div class="icons">
        <a href="cart.html?tab=wish" aria-label="찜한 상품">♡<i class="badge" data-wish-badge></i></a>
        <a href="#" data-member aria-label="내 정보">👤</a>
        <a href="cart.html" aria-label="장바구니">🛒<i class="badge" data-cart-badge></i></a>
      </div>
    </div></nav>`;
  }

  /* ---------- 바닥글 ---------- */
  function footer() {
    const c = S.company;
    return `
    <div class="wrap foot-top">
      <div class="cs">
        <p><strong>${esc(S.name)} 고객센터</strong> <a class="tel" href="tel:${S.phone.replace(/-/g, "")}">${esc(S.phone)}</a></p>
        <dl><dt>운영시간</dt><dd>${esc(S.hours)}</dd><dt>입금계좌안내</dt><dd>${esc(S.bank)}</dd></dl>
      </div>
      <div class="foot-btns"><a href="notice.html#ask" class="btn-line">문의하기</a><a href="notice.html" class="btn-line">공지사항</a></div>
    </div>
    <div class="wrap foot-bottom">
      <div class="foot-links"><img src="images/logo.png" alt="${esc(S.name)}" width="110" height="54">
        <a href="terms.html">이용약관</a><a href="privacy.html"><b>개인정보처리방침</b></a></div>
      <p class="biz">상호명 : ${esc(c.name)} <i>|</i> 대표자 : ${esc(c.ceo)} <i>|</i> 사업자등록번호 : ${esc(c.bizNo)} <i>|</i> 사업장주소 : ${esc(c.address)}<br>
      통신판매업신고번호 : ${esc(c.mailOrderNo)} <i>|</i> 이메일 : ${esc(c.email)} <i>|</i> 연락처 : ${esc(S.phone)} <i>|</i> 호스팅제공자 : ${esc(c.hosting)}</p>
      <p class="copy">Copyright © 2026 ${esc(c.name)}. All rights reserved.</p>
    </div>`;
  }

  function updateBadges() {
    document.querySelectorAll("[data-cart-badge]").forEach((b) => { const n = cart.count(); b.textContent = n || ""; b.hidden = !n; });
    document.querySelectorAll("[data-wish-badge]").forEach((b) => { const n = wish.all().length; b.textContent = n || ""; b.hidden = !n; });
  }

  /* ---------- 상품 카드 ---------- */
  function thumb(p, cls = "thumb") {
    return p.image
      ? `<div class="${cls}"><img src="${esc(p.image)}" alt="${esc(p.name)}" loading="lazy"></div>`
      : `<div class="${cls} ph ph-${p.cat}" role="img" aria-label="${esc(p.name)} 사진 준비 중"><span>${p.emoji || "🛒"}</span><small>사진 준비 중</small></div>`;
  }
  function card(p) {
    const d = pct(p);
    return `<article class="card">
      <a href="product.html?id=${p.id}" class="card-link">
        ${thumb(p)}
        ${p.sample ? '<span class="sample">예시 상품</span>' : ""}
        <h3>${esc(p.name)}</h3>
        <p class="price">${d ? `<b class="pct">${d}%</b>` : ""}<strong>${won(p.sale)}</strong>${d ? `<del>${won(p.price)}</del>` : ""}</p>
      </a>
      <div class="card-act">
        <button class="wish${wish.has(p.id) ? " on" : ""}" data-wish="${p.id}" aria-label="찜하기" aria-pressed="${wish.has(p.id)}">♡</button>
        <button class="add" data-add="${p.id}">담기</button>
      </div>
    </article>`;
  }
  const grid = (list) => list.length ? `<div class="grid">${list.map(card).join("")}</div>` : `<p class="empty">상품이 없습니다.</p>`;

  /* ---------- 페이지: 메인 ---------- */
  function pageHome() {
    // 배너 슬라이드
    const bs = (S.banners || []).slice(0, 10);
    const slider = $("#banner");
    slider.innerHTML = `<div class="slides">${bs.map((b, i) => {
      const href = b.link || "#";
      if (b.image && !b.title) return `<a class="slide img-only" href="${esc(href)}"><img src="${esc(b.image)}" alt="배너 ${i + 1}"></a>`;
      return `<a class="slide" href="${esc(href)}" style="--slide-bg:${esc(b.color || "#2c5a1c")}">
        <div class="slide-text"><h2>${esc(b.title)}</h2><p>${esc(b.text || "")}</p><span class="more">자세히 보기 →</span></div>
        ${b.image ? `<img src="${esc(b.image)}" alt="" ${i ? 'loading="lazy"' : ""}>` : ""}</a>`;
    }).join("")}</div>
    ${bs.length > 1 ? `<button class="nav prev" aria-label="이전 배너">‹</button><button class="nav next" aria-label="다음 배너">›</button>
    <div class="dots">${bs.map((_, i) => `<button aria-label="${i + 1}번 배너"></button>`).join("")}</div>` : ""}`;
    let idx = 0; const slides = $(".slides", slider), dots = slider.querySelectorAll(".dots button");
    const go = (i) => { idx = (i + bs.length) % bs.length; slides.style.transform = `translateX(-${idx * 100}%)`; dots.forEach((d, j) => d.classList.toggle("on", j === idx)); };
    if (bs.length > 1) {
      $(".prev", slider).onclick = () => go(idx - 1); $(".next", slider).onclick = () => go(idx + 1);
      dots.forEach((d, j) => (d.onclick = () => go(j)));
      let timer = setInterval(() => go(idx + 1), 5000);
      slider.addEventListener("mouseenter", () => clearInterval(timer));
      slider.addEventListener("mouseleave", () => (timer = setInterval(() => go(idx + 1), 5000)));
    }
    go(0);
    slider.querySelectorAll('a[href="#kakao"]').forEach((a) => a.addEventListener("click", openKakao));

    $("#coupon-amount").textContent = S.welcomeCoupon;
    $("#sec-today").innerHTML = grid(P.filter((p) => p.tags?.includes("today")).slice(0, 6));
    $("#sec-best").innerHTML = grid(P.filter((p) => p.tags?.includes("best")).slice(0, 6));
    ["farm", "meat", "sea"].forEach((k) => {
      const sec = $(`#sec-${k}`);
      sec.innerHTML = `<div class="sec-head"><div><h2>${esc(C[k].title)}</h2><p>${esc(C[k].sub)}</p></div><a href="list.html?cat=${k}" class="more-link">더보기 ›</a></div>` +
        grid(P.filter((p) => p.cat === k).slice(0, 3));
    });
    $("#kakao-pw").textContent = S.kakaoPassword;
    document.querySelectorAll("[data-kakao]").forEach((a) => a.addEventListener("click", openKakao));
    const rv = window.REVIEWS || [];
    $("#reviews").innerHTML = rv.map((r) => { const p = byId(r.productId);
      return `<figure class="review">${p ? thumb(p, "rthumb") : ""}<figcaption>
        <span class="stars" aria-label="별점 ${r.stars}점">${"★".repeat(r.stars)}${"☆".repeat(5 - r.stars)}</span>
        <blockquote>${esc(r.text)}</blockquote><cite>${esc(r.name)} · ${p ? esc(p.name) : ""}</cite>${r.sample ? '<span class="sample">예시 후기</span>' : ""}
      </figcaption></figure>`; }).join("");
  }

  /* ---------- 페이지: 목록·검색 ---------- */
  function pageList() {
    const cat = params.get("cat"), q = (params.get("q") || "").trim();
    let list = P, title = "전체상품", sub = "먹자GO 의 모든 상품을 도매가로 만나보세요.";
    if (cat === "today") { list = P.filter((p) => p.tags?.includes("today")); title = "지금 안 사면 '손해', 오늘의 특가전!"; sub = "망설이면 놓치는 오늘의 최저가, 실속 구성과 가격을 한 번에 잡으세요!"; }
    else if (C[cat]) { list = P.filter((p) => p.cat === cat); title = C[cat].title; sub = C[cat].sub; }
    if (q) { const k = q.toLowerCase(); list = list.filter((p) => (p.name + " " + (C[p.cat]?.name || "") + " " + (p.origin || "")).toLowerCase().includes(k)); title = `'${q}' 검색 결과`; sub = `${list.length}개 상품`; }
    document.title = `${title} | ${S.name}`;
    $("#list-title").textContent = title; $("#list-sub").textContent = sub;
    const sort = $("#sort");
    const render = () => {
      const l = [...list];
      if (sort.value === "low") l.sort((a, b) => a.sale - b.sale);
      if (sort.value === "high") l.sort((a, b) => b.sale - a.sale);
      if (sort.value === "pct") l.sort((a, b) => pct(b) - pct(a));
      $("#list").innerHTML = grid(l);
    };
    sort.onchange = render; render();
  }

  /* ---------- 페이지: 상세 ---------- */
  function pageProduct() {
    const p = byId(params.get("id"));
    const box = $("#product");
    if (!p) { box.innerHTML = `<p class="empty">상품을 찾을 수 없습니다. <a href="list.html">전체상품 보기</a></p>`; return; }
    document.title = `${p.name} | ${S.name}`;
    const d = pct(p);
    box.innerHTML = `
      <nav class="crumb" aria-label="위치"><a href="index.html">홈</a> › <a href="list.html?cat=${p.cat}">${esc(C[p.cat]?.name || "")}</a> › <span>${esc(p.name)}</span></nav>
      <div class="pd">
        ${thumb(p, "pd-img")}
        <div class="pd-info">
          ${p.sample ? '<span class="sample">예시 상품</span>' : ""}
          <h1>${esc(p.name)}</h1>
          <p class="pd-desc">${esc(p.desc || "")}</p>
          <p class="price lg">${d ? `<b class="pct">${d}%</b>` : ""}<strong>${won(p.sale)}</strong>${d ? `<del>${won(p.price)}</del>` : ""}</p>
          <dl class="pd-spec"><dt>구성</dt><dd>${esc(p.unit || "-")}</dd><dt>원산지</dt><dd>${esc(p.origin || "-")}</dd><dt>배송</dt><dd>택배 (주문 후 안내)</dd></dl>
          <div class="qty"><button data-q="-1" aria-label="수량 빼기">−</button><input id="qty" type="number" min="1" value="1" aria-label="수량"><button data-q="1" aria-label="수량 더하기">＋</button></div>
          <p class="total">합계 <strong id="total">${won(p.sale)}</strong></p>
          <div class="pd-btns">
            <button class="wish big${wish.has(p.id) ? " on" : ""}" data-wish="${p.id}" aria-label="찜하기" aria-pressed="${wish.has(p.id)}">♡</button>
            <button class="btn-line big" id="pd-add">장바구니</button>
            <button class="btn big" data-kakao>카톡으로 주문하기</button>
          </div>
          <p class="pd-note">주문은 카카오톡 특가방(비밀번호 ${esc(S.kakaoPassword)}) 또는 고객센터 <a href="tel:${S.phone.replace(/-/g, "")}">${esc(S.phone)}</a> 로 받습니다.</p>
        </div>
      </div>
      <section class="pd-detail"><h2>상세정보</h2>
        ${(p.detail || []).map((src) => `<img src="${esc(src)}" alt="${esc(p.name)} 상세" loading="lazy">`).join("") ||
          (p.image ? `<img src="${esc(p.image)}" alt="${esc(p.name)}" loading="lazy">` : "")}
        <p>${esc(p.desc || "")}</p>
      </section>
      <section><div class="sec-head"><div><h2>함께 보면 좋은 상품</h2></div></div>${grid(P.filter((x) => x.cat === p.cat && x.id !== p.id).slice(0, 3))}</section>`;
    const qty = $("#qty"), upd = () => { qty.value = Math.max(1, parseInt(qty.value) || 1); $("#total").textContent = won(p.sale * qty.value); };
    box.querySelectorAll("[data-q]").forEach((b) => (b.onclick = () => { qty.value = (+qty.value || 1) + +b.dataset.q; upd(); }));
    qty.oninput = upd;
    $("#pd-add").onclick = () => { cart.add(p.id, +qty.value); toast(`장바구니에 ${qty.value}개 담았습니다`); };
    box.querySelectorAll("[data-kakao]").forEach((a) => a.addEventListener("click", openKakao));
  }

  /* ---------- 페이지: 장바구니·찜 ---------- */
  function pageCart() {
    const tab = params.get("tab") === "wish" ? "wish" : "cart";
    document.querySelectorAll(".tabs a").forEach((a) => a.classList.toggle("on", a.dataset.tab === tab));
    const box = $("#cart");
    const draw = () => {
      if (tab === "wish") { box.innerHTML = grid(wish.all().map(byId).filter(Boolean)); return; }
      const items = cart.all().map((x) => ({ ...x, p: byId(x.id) })).filter((x) => x.p);
      if (!items.length) { box.innerHTML = `<p class="empty">장바구니가 비었습니다. <a href="list.html">상품 보러 가기</a></p>`; return; }
      const sum = items.reduce((a, x) => a + x.p.sale * x.qty, 0);
      box.innerHTML = `<ul class="cart-list">${items.map((x) => `<li>
        ${thumb(x.p, "cthumb")}<a href="product.html?id=${x.id}" class="cname">${esc(x.p.name)}</a>
        <div class="qty sm"><button data-cq="${x.id}" data-d="-1" aria-label="빼기">−</button><span>${x.qty}</span><button data-cq="${x.id}" data-d="1" aria-label="더하기">＋</button></div>
        <strong>${won(x.p.sale * x.qty)}</strong><button class="del" data-del="${x.id}" aria-label="삭제">✕</button></li>`).join("")}</ul>
        <div class="cart-sum"><p>상품 합계 <strong>${won(sum)}</strong></p><p class="muted">배송비는 주문 시 안내해 드립니다.</p>
        <button class="btn big" id="copy-order">주문 내용 복사</button> <button class="btn big kakao" data-kakao>카톡으로 주문하기</button>
        <p class="pd-note">「주문 내용 복사」를 누른 뒤 카카오톡 특가방(비밀번호 ${esc(S.kakaoPassword)})이나 문자(${esc(S.phone)})에 붙여 넣어 주세요.</p></div>`;
      $("#copy-order").onclick = () => {
        const txt = `[먹자GO 주문]\n${items.map((x) => `- ${x.p.name} × ${x.qty} = ${won(x.p.sale * x.qty)}`).join("\n")}\n합계: ${won(sum)}`;
        (navigator.clipboard?.writeText(txt) || Promise.reject()).then(() => toast("주문 내용을 복사했습니다"), () => prompt("아래 내용을 복사하세요", txt));
      };
      box.querySelectorAll("[data-kakao]").forEach((a) => a.addEventListener("click", openKakao));
    };
    box.addEventListener("click", (e) => {
      const q = e.target.closest("[data-cq]"), d = e.target.closest("[data-del]");
      if (q) { const c = cart.all(); const it = c.find((x) => x.id == q.dataset.cq); it.qty = Math.max(1, it.qty + +q.dataset.d); cart.save(c); draw(); }
      if (d) { cart.save(cart.all().filter((x) => x.id != d.dataset.del)); draw(); }
    });
    draw();
  }

  /* ---------- 페이지: 공지 ---------- */
  function pageNotice() {
    $("#notices").innerHTML = (window.NOTICES || []).map((n, i) =>
      `<details${i === 0 ? " open" : ""}><summary><span>${esc(n.title)}</span><time>${esc(n.date)}</time></summary><p>${esc(n.body)}</p></details>`).join("");
    document.querySelectorAll("[data-phone]").forEach((el) => (el.textContent = S.phone));
    document.querySelectorAll("[data-email]").forEach((el) => (el.textContent = S.company.email));
    document.querySelectorAll("[data-hours]").forEach((el) => (el.textContent = S.hours));
    document.querySelectorAll("[data-kakao]").forEach((a) => a.addEventListener("click", openKakao));
  }

  /* ---------- 시작 ---------- */
  document.addEventListener("DOMContentLoaded", () => {
    const h = $("#site-header"), f = $("#site-footer");
    if (h) h.innerHTML = header();
    if (f) f.innerHTML = footer();
    const pages = { home: pageHome, list: pageList, product: pageProduct, cart: pageCart, notice: pageNotice };
    (pages[document.body.dataset.page] || (() => {}))();
    updateBadges();

    document.addEventListener("click", (e) => {
      const add = e.target.closest("[data-add]"), w = e.target.closest("[data-wish]"), m = e.target.closest("[data-member]");
      if (add) { cart.add(+add.dataset.add); toast("장바구니에 담았습니다"); }
      if (w) { const on = wish.toggle(+w.dataset.wish); w.classList.toggle("on", on); w.setAttribute("aria-pressed", on); toast(on ? "찜했습니다" : "찜을 해제했습니다"); }
      if (m) { e.preventDefault(); toast("회원 서비스는 준비 중입니다. 주문은 카카오톡 특가방으로 해 주세요!"); }
    });
    const mb = $(".menu-btn");
    if (mb) mb.onclick = () => { const o = document.body.classList.toggle("nav-open"); mb.setAttribute("aria-expanded", o); };
  });
})();
