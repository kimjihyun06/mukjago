/* 먹자GO 공통 스크립트 — 머리글·바닥글·장바구니·상품 카드·각 페이지 동작
 * 회사 정보: js/config.js / 상품(엑셀 자동): js/products.js / 문구·후기·공지: js/content.js */
(function () {
  "use strict";
  const S = window.SITE, P = window.PRODUCTS || [], C = window.CATEGORIES || {}, HOME = window.HOME || {};
  const $ = (q, el = document) => el.querySelector(q);
  const won = (n) => Number(n).toLocaleString("ko-KR") + "원";
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const byId = (id) => P.find((p) => String(p.id) === String(id));
  const params = new URLSearchParams(location.search);
  const shipText = (s) => (s === 0 ? "무료배송" : s == null ? "택배비 문의" : `택배비 ${won(s)}`);
  const optLabel = (o) => (!o.unit || o.name.includes(o.unit) ? o.name : `${o.name} (${o.unit})`);
  const fromPrice = (p) => `${won(p.price)}${p.options.filter((o) => !o.soldout).length > 1 ? "~" : ""}`;

  /* ---------- 저장 (이 기기 브라우저에만) ---------- */
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  const cart = {
    // 항목: { id: 상품번호, o: 옵션 순번, qty }
    all: () => store.get("mg_cart2", []).filter((x) => byId(x.id)?.options[x.o]),
    save(v) { store.set("mg_cart2", v); updateBadges(); },
    add(id, o = 0, qty = 1) {
      const c = cart.all(); const it = c.find((x) => x.id === id && x.o === o);
      it ? (it.qty += qty) : c.push({ id, o, qty }); cart.save(c);
    },
    count: () => cart.all().reduce((a, x) => a + x.qty, 0),
  };
  const wish = {
    all: () => store.get("mg_wish2", []).filter(byId),
    toggle(id) { const w = wish.all(); const i = w.indexOf(id); i >= 0 ? w.splice(i, 1) : w.push(id); store.set("mg_wish2", w); updateBadges(); return i < 0; },
    has: (id) => wish.all().includes(id),
  };

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
  const bindKakao = (root = document) => root.querySelectorAll("[data-kakao]").forEach((a) => a.addEventListener("click", openKakao));

  /* ---------- 머리글 ---------- */
  function header() {
    const navs = [["list.html", "전체상품", "all"], ["list.html?cat=today", "오늘의특가", "today"],
      ...Object.entries(C).map(([k, c]) => [`list.html?cat=${k}`, c.name, k]), ["notice.html#partner", "입점문의", "partner"]];
    const cur = params.get("cat") || (location.pathname.endsWith("list.html") ? "all" : "");
    return `
    <div class="topbar"><div class="wrap">
      <a href="#" data-member>로그인</a><span>|</span>
      <a href="#" data-member class="join">회원가입<em class="bubble">${esc(S.welcomeCoupon)} 쿠폰</em></a><span>|</span>
      <a href="notice.html">고객센터</a>
    </div></div>
    <div class="logo-row wrap"><a href="index.html" class="logo" aria-label="${esc(S.name)} 홈"><img src="images/logo.png" alt="${esc(S.name)} - ${esc(S.slogan)}" width="360" height="175"></a></div>
    <nav class="gnb" aria-label="주 메뉴"><div class="wrap">
      <button class="menu-btn" aria-label="메뉴 열기" aria-expanded="false">☰</button>
      <ul class="gnb-list">${navs.map(([h, t, k], i) =>
        `<li><a href="${h}"${k === cur ? ' aria-current="page"' : ""}>${i === 0 ? "<b>≡</b> " : ""}${esc(t)}</a></li>`).join("")}</ul>
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
  function thumb(p, cls = "thumb", src) {
    const img = src || (p.images || [])[0];
    return img
      ? `<div class="${cls}"><img src="${esc(img)}" alt="${esc(p.name)}" loading="lazy"></div>`
      : `<div class="${cls} ph ph-${p.cat}" role="img" aria-label="${esc(p.name)} 사진 준비 중"><span>${p.emoji || "🛒"}</span><small>사진 준비 중</small></div>`;
  }
  function badges(p) {
    return `<p class="tags">${p.ship === 0 ? '<span class="tg free">무료배송</span>' : ""}<span class="tg">${esc(p.tax || "")}</span>${
      p.deadline ? `<span class="tg dl">마감 ${esc(p.deadline)}</span>` : ""}</p>`;
  }
  function card(p) {
    const soldAll = p.options.every((o) => o.soldout);
    return `<article class="card${soldAll ? " sold" : ""}">
      <a href="product.html?id=${p.id}" class="card-link">
        ${thumb(p)}
        <h3>${esc(p.name)}</h3>
        <p class="price"><strong>${soldAll ? "품절" : fromPrice(p)}</strong>${p.options.length > 1 ? `<small>옵션 ${p.options.length}개</small>` : ""}</p>
        ${badges(p)}
      </a>
      <div class="card-act">
        <button class="wish${wish.has(p.id) ? " on" : ""}" data-wish="${p.id}" aria-label="찜하기" aria-pressed="${wish.has(p.id)}">♡</button>
        <a class="add" href="product.html?id=${p.id}">${p.options.length > 1 ? "옵션 선택" : "자세히 보기"}</a>
      </div>
    </article>`;
  }
  const grid = (list) => list.length ? `<div class="grid">${list.map(card).join("")}</div>` : `<p class="empty">상품이 없습니다.</p>`;
  const pick = (ids) => ids.map(byId).filter(Boolean);
  const newest = (n) => [...P].sort((a, b) => (b.start || "").localeCompare(a.start || "")).slice(0, n);

  /* ---------- 메인 ---------- */
  function pageHome() {
    const bs = (S.banners || []).slice(0, 10), slider = $("#banner");
    slider.innerHTML = `<div class="slides">${bs.map((b, i) => {
      const href = b.link || "#";
      if (b.image && !b.title) return `<a class="slide img-only" href="${esc(href)}"><img src="${esc(b.image)}" alt="배너 ${i + 1}"></a>`;
      return `<a class="slide" href="${esc(href)}" style="--slide-bg:${esc(b.color || "#2c5a1c")}">
        <div class="slide-text"><h2>${esc(b.title)}</h2><p>${esc(b.text || "")}</p><span class="more">자세히 보기 →</span></div>
        ${b.image ? `<img src="${esc(b.image)}" alt="" ${i ? 'loading="lazy"' : ""}>` : ""}${b.emoji && !b.image ? `<span class="slide-emoji" aria-hidden="true">${b.emoji}</span>` : ""}</a>`;
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
    $("#sec-today").innerHTML = grid(HOME.today?.length ? pick(HOME.today) : newest(6));
    $("#sec-best").innerHTML = grid(pick(HOME.best || []).slice(0, 6));
    Object.keys(C).forEach((k) => {
      const sec = $(`#sec-${k}`); if (!sec) return;
      const list = P.filter((p) => p.cat === k);
      sec.innerHTML = `<div class="sec-head"><div><h2>${esc(C[k].title)}</h2><p>${esc(C[k].sub)}</p></div><a href="list.html?cat=${k}" class="more-link">${list.length}개 전체보기 ›</a></div>` +
        grid([...list].sort((a, b) => (b.start || "").localeCompare(a.start || "")).slice(0, 6));
    });
    $("#kakao-pw").textContent = S.kakaoPassword;
    bindKakao();
    const rv = window.REVIEWS || [];
    $("#reviews").innerHTML = rv.length ? rv.map((r) => { const p = byId(r.productId);
      return `<figure class="review">${p ? thumb(p, "rthumb") : ""}<figcaption>
        <span class="stars" aria-label="별점 ${r.stars}점">${"★".repeat(r.stars)}${"☆".repeat(5 - r.stars)}</span>
        <blockquote>${esc(r.text)}</blockquote><cite>${esc(r.name)} · ${p ? esc(p.name) : ""}</cite></figcaption></figure>`; }).join("")
      : `<div class="review-empty"><p>💬 첫 후기를 기다리고 있어요!</p><p class="muted">드셔 보신 소감을 카카오톡 특가방에 남겨 주시면 이곳에 소개해 드립니다.</p></div>`;
  }

  /* ---------- 목록·검색 ---------- */
  function pageList() {
    const cat = params.get("cat"), q = (params.get("q") || "").trim();
    let list = P, title = "전체상품", sub = `먹자GO 의 모든 상품 ${P.length}개를 도매가로 만나보세요.`;
    if (cat === "today") { list = newest(12); title = "지금 안 사면 '손해', 오늘의 특가전!"; sub = "망설이면 놓치는 오늘의 최저가, 실속 구성과 가격을 한 번에 잡으세요!"; }
    else if (C[cat]) { list = P.filter((p) => p.cat === cat); title = C[cat].title; sub = C[cat].sub; }
    if (q) { const k = q.toLowerCase(); list = list.filter((p) => [p.name, C[p.cat]?.name, ...p.options.map((o) => o.name)].join(" ").toLowerCase().includes(k)); title = `'${q}' 검색 결과`; sub = `${list.length}개 상품`; }
    document.title = `${title} | ${S.name}`;
    $("#list-title").textContent = title; $("#list-sub").textContent = sub;
    const sort = $("#sort");
    const render = () => {
      const l = [...list];
      if (sort.value === "new") l.sort((a, b) => (b.start || "").localeCompare(a.start || ""));
      if (sort.value === "low") l.sort((a, b) => a.price - b.price);
      if (sort.value === "high") l.sort((a, b) => b.price - a.price);
      if (sort.value === "free") l.sort((a, b) => (a.ship === 0 ? 0 : 1) - (b.ship === 0 ? 0 : 1));
      $("#list").innerHTML = grid(l);
    };
    sort.onchange = render; render();
  }

  /* ---------- 상세 ---------- */
  function pageProduct() {
    const p = byId(params.get("id")), box = $("#product");
    if (!p) { box.innerHTML = `<p class="empty">상품을 찾을 수 없습니다. <a href="list.html">전체상품 보기</a></p>`; return; }
    document.title = `${p.name} | ${S.name}`;
    const imgs = p.images || [];
    const first = p.options.findIndex((o) => !o.soldout);
    box.innerHTML = `
      <nav class="crumb" aria-label="위치"><a href="index.html">홈</a> › <a href="list.html?cat=${p.cat}">${esc(C[p.cat]?.name || "")}</a> › <span>${esc(p.name)}</span></nav>
      <div class="pd">
        <div class="pd-gallery">
          ${thumb(p, "pd-img", imgs[0])}
          ${imgs.length > 1 ? `<div class="pd-thumbs">${imgs.map((s, i) => `<button data-img="${esc(s)}"${i ? "" : ' class="on"'} aria-label="사진 ${i + 1}"><img src="${esc(s)}" alt=""></button>`).join("")}</div>` : ""}
        </div>
        <div class="pd-info">
          <p class="pd-cat">${esc(C[p.cat]?.name || "")}</p>
          <h1>${esc(p.name)}</h1>
          <p class="price lg"><strong id="unit-price">${fromPrice(p)}</strong></p>
          <dl class="pd-spec">
            <dt>배송</dt><dd id="ship-txt">${shipText(p.ship)}</dd>
            <dt>과세</dt><dd>${esc(p.tax || "-")} 상품</dd>
            ${p.deadline ? `<dt>주문마감</dt><dd>${esc(p.deadline)} (마감 후 주문은 다음 출고)</dd>` : ""}
          </dl>
          <label class="opt-label" for="opt">옵션 선택</label>
          <select id="opt" class="opt">${p.options.map((o, i) =>
            `<option value="${i}"${o.soldout ? " disabled" : ""}${i === first ? " selected" : ""}>${esc(optLabel(o))} — ${o.soldout ? "품절" : won(o.price)}</option>`).join("")}</select>
          <div class="qty"><button data-q="-1" aria-label="수량 빼기">−</button><input id="qty" type="number" min="1" value="1" aria-label="수량"><button data-q="1" aria-label="수량 더하기">＋</button></div>
          <p class="total">합계 <strong id="total"></strong> <small id="total-ship" class="muted"></small></p>
          <div class="pd-btns">
            <button class="wish big${wish.has(p.id) ? " on" : ""}" data-wish="${p.id}" aria-label="찜하기" aria-pressed="${wish.has(p.id)}">♡</button>
            <button class="btn-line big" id="pd-add">장바구니</button>
            <button class="btn big" data-kakao>카톡으로 주문하기</button>
          </div>
          <p class="pd-note">주문은 카카오톡 특가방(비밀번호 ${esc(S.kakaoPassword)}) 또는 고객센터 <a href="tel:${S.phone.replace(/-/g, "")}">${esc(S.phone)}</a> 로 받습니다.</p>
        </div>
      </div>
      <section class="pd-detail" aria-labelledby="h-detail"><h2 id="h-detail">상세정보</h2>
        <img class="pd-top" src="${esc(p.top)}" alt="${esc(p.name)} 판매가 안내 - 먹자고 ${esc(S.phone)}" loading="lazy">
        ${(p.detail || []).length ? p.detail.map((src) => `<img src="${esc(src)}" alt="${esc(p.name)} 상세" loading="lazy">`).join("")
          : `<div class="detail-ph" role="img" aria-label="상세 이미지 준비 중"><span>${p.emoji || "🛒"}</span><p>상세 이미지 준비 중입니다</p></div>`}
      </section>
      <section><div class="sec-head"><div><h2>함께 보면 좋은 상품</h2></div></div>${grid(P.filter((x) => x.cat === p.cat && x.id !== p.id).slice(0, 3))}</section>`;
    const sel = $("#opt"), qty = $("#qty");
    const upd = () => {
      const o = p.options[+sel.value]; qty.value = Math.max(1, parseInt(qty.value) || 1);
      $("#unit-price").textContent = o.soldout ? "품절" : won(o.price);
      $("#total").textContent = won(o.price * qty.value);
      $("#ship-txt").textContent = shipText(o.ship);
      $("#total-ship").textContent = o.ship ? `+ 택배비 ${won(o.ship)}` : o.ship === 0 ? "(무료배송)" : "";
    };
    box.querySelectorAll("[data-q]").forEach((b) => (b.onclick = () => { qty.value = (+qty.value || 1) + +b.dataset.q; upd(); }));
    qty.oninput = upd; sel.onchange = upd; upd();
    box.querySelectorAll("[data-img]").forEach((b) => (b.onclick = () => {
      $(".pd-img img", box).src = b.dataset.img; box.querySelectorAll("[data-img]").forEach((x) => x.classList.toggle("on", x === b));
    }));
    $("#pd-add").onclick = () => {
      const o = p.options[+sel.value]; if (o.soldout) return toast("품절된 옵션입니다");
      cart.add(p.id, +sel.value, +qty.value); toast(`장바구니에 ${qty.value}개 담았습니다`);
    };
    bindKakao(box);
  }

  /* ---------- 장바구니·찜 ---------- */
  function pageCart() {
    const tab = params.get("tab") === "wish" ? "wish" : "cart";
    document.querySelectorAll(".tabs a").forEach((a) => a.classList.toggle("on", a.dataset.tab === tab));
    const box = $("#cart");
    const draw = () => {
      if (tab === "wish") { box.innerHTML = grid(wish.all().map(byId)); return; }
      const items = cart.all().map((x, i) => ({ ...x, i, p: byId(x.id), op: byId(x.id).options[x.o] }));
      if (!items.length) { box.innerHTML = `<p class="empty">장바구니가 비었습니다. <a href="list.html">상품 보러 가기</a></p>`; return; }
      const sum = items.reduce((a, x) => a + x.op.price * x.qty, 0);
      // 택배비: 상품(시트)마다 한 번씩 (같은 상품 여러 옵션은 묶음 배송으로 계산)
      const shipBy = {}; items.forEach((x) => { const s = x.op.ship; if (s) shipBy[x.id] = Math.max(shipBy[x.id] || 0, s); });
      const ship = Object.values(shipBy).reduce((a, b) => a + b, 0);
      box.innerHTML = `<ul class="cart-list">${items.map((x) => `<li>
        ${thumb(x.p, "cthumb")}<div class="cname"><a href="product.html?id=${x.id}">${esc(x.p.name)}</a><small>${esc(optLabel(x.op))} · ${shipText(x.op.ship)}</small></div>
        <div class="qty sm"><button data-cq="${x.i}" data-d="-1" aria-label="빼기">−</button><span>${x.qty}</span><button data-cq="${x.i}" data-d="1" aria-label="더하기">＋</button></div>
        <strong>${won(x.op.price * x.qty)}</strong><button class="del" data-del="${x.i}" aria-label="삭제">✕</button></li>`).join("")}</ul>
        <div class="cart-sum"><p>상품 합계 <strong>${won(sum)}</strong></p><p>예상 택배비 <b>${won(ship)}</b></p>
        <p class="muted">택배비는 상품(산지)마다 따로 붙으며, 정확한 금액은 주문 시 안내해 드립니다.</p>
        <button class="btn big" id="copy-order">주문 내용 복사</button> <button class="btn big kakao" data-kakao>카톡으로 주문하기</button>
        <p class="pd-note">「주문 내용 복사」를 누른 뒤 카카오톡 특가방(비밀번호 ${esc(S.kakaoPassword)})이나 문자(${esc(S.phone)})에 붙여 넣어 주세요.</p></div>`;
      $("#copy-order").onclick = () => {
        const txt = `[먹자GO 주문]\n${items.map((x) => `- ${x.p.name} / ${optLabel(x.op)} × ${x.qty} = ${won(x.op.price * x.qty)}`).join("\n")}\n상품 합계: ${won(sum)}\n예상 택배비: ${won(ship)}`;
        (navigator.clipboard?.writeText(txt) || Promise.reject()).then(() => toast("주문 내용을 복사했습니다"), () => prompt("아래 내용을 복사하세요", txt));
      };
      bindKakao(box);
    };
    box.addEventListener("click", (e) => {
      const q = e.target.closest("[data-cq]"), d = e.target.closest("[data-del]"), c = cart.all();
      if (q) { const it = c[+q.dataset.cq]; it.qty = Math.max(1, it.qty + +q.dataset.d); cart.save(c); draw(); }
      if (d) { c.splice(+d.dataset.del, 1); cart.save(c); draw(); }
    });
    draw();
  }

  /* ---------- 공지 ---------- */
  function pageNotice() {
    $("#notices").innerHTML = (window.NOTICES || []).map((n, i) =>
      `<details${i === 0 ? " open" : ""}><summary><span>${esc(n.title)}</span><time>${esc(n.date)}</time></summary><p>${esc(n.body)}</p></details>`).join("");
    document.querySelectorAll("[data-phone]").forEach((el) => (el.textContent = S.phone));
    document.querySelectorAll("[data-email]").forEach((el) => (el.textContent = S.company.email));
    document.querySelectorAll("[data-hours]").forEach((el) => (el.textContent = S.hours));
    bindKakao();
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
      const w = e.target.closest("[data-wish]"), m = e.target.closest("[data-member]");
      if (w) { const on = wish.toggle(+w.dataset.wish); w.classList.toggle("on", on); w.setAttribute("aria-pressed", on); toast(on ? "찜했습니다" : "찜을 해제했습니다"); }
      if (m) { e.preventDefault(); toast("회원 서비스는 준비 중입니다. 주문은 카카오톡 특가방으로 해 주세요!"); }
    });
    const mb = $(".menu-btn");
    if (mb) mb.onclick = () => { const o = document.body.classList.toggle("nav-open"); mb.setAttribute("aria-expanded", o); };
  });
})();
