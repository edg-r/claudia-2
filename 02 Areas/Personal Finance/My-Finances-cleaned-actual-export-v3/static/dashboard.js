const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
const $ = (id) => document.getElementById(id);

let state = {
  month: null,
  data: null,
  groupId: null,
  categoryId: null,
  uncategorizedOnly: false,
  accountId: null,
  privacyMode: false,
};

const pieColors = [
  "#18684a", "#a84a3a", "#315f7d", "#b67b24", "#704f8f",
  "#4d7f72", "#c06448", "#5b6f91", "#9b7335", "#7b6b58",
  "#8f3f55", "#3f7b8f", "#6c756f", "#577a42", "#a15d25",
];

function formatMoney(value) {
  return money.format(value || 0);
}

function formatPercent(value, total) {
  if (!total) return "0.0%";
  return `${((Math.abs(value || 0) / Math.abs(total)) * 100).toFixed(1)}%`;
}

function displayMoney(value, total = state.data?.latestMonth?.outflow || 0) {
  return state.privacyMode ? formatPercent(value, total) : formatMoney(value);
}

function totalSpendingForVisibleRows(rows) {
  return rows.reduce((sum, row) => sum + Math.abs(row.spending || 0), 0);
}

function classForAmount(value) {
  return value >= 0 ? "positive" : "negative";
}

function setStatus(message) {
  $("syncStatus").textContent = message;
}

function renderCashChart(monthly) {
  const max = Math.max(...monthly.flatMap((m) => [m.inflow, m.outflow]), 1);
  $("cashChart").innerHTML = monthly.map((month) => {
    const selected = month.month === state.data.currentMonth ? "selected" : "";
    const inHeight = Math.max(3, (month.inflow / max) * 220);
    const outHeight = Math.max(3, (month.outflow / max) * 220);
    return `
      <button class="month-bar ${selected}" type="button" data-month="${month.month}" title="${month.month}: ${formatMoney(month.inflow)} in / ${formatMoney(month.outflow)} out">
        <span class="bars">
          <span class="bar in" style="height:${inHeight}px"></span>
          <span class="bar out" style="height:${outHeight}px"></span>
        </span>
        <label>${month.month.slice(5)}</label>
      </button>
    `;
  }).join("");
  document.querySelectorAll(".month-bar").forEach((button) => {
    button.addEventListener("click", () => loadSummary(button.dataset.month));
  });
}

function renderAccounts(accounts) {
  $("accounts").innerHTML = accounts.map((account) => {
    const active = state.accountId === account.id ? "active" : "";
    return `
    <button class="account ${active}" type="button" data-account-id="${account.id}">
      <div>
        <strong>${account.name}</strong>
        <small>${account.syncSource} / ${account.lastSync || "not synced"}</small>
      </div>
      <div class="amount ${classForAmount(account.balance)}">${displayMoney(account.balance, state.data.netWorth)}</div>
    </button>
  `;
  }).join("");

  document.querySelectorAll(".account").forEach((button) => {
    button.addEventListener("click", () => {
      state.accountId = state.accountId === button.dataset.accountId ? null : button.dataset.accountId;
      state.groupId = null;
      state.categoryId = null;
      state.uncategorizedOnly = false;
      renderAccounts(state.data.accounts);
      renderTransactions();
      renderChips();
    });
  });
}

function renderBars(id, rows, valueKey, labelKey, detail) {
  const max = Math.max(...rows.map((row) => Math.abs(row[valueKey])), 1);
  $(id).innerHTML = rows.length ? rows.map((row) => {
    const pct = Math.min(100, (Math.abs(row[valueKey]) / max) * 100);
    return `
      <div class="row-item">
        <div class="row-top">
          <strong>${row[labelKey]}</strong>
          <span>${detail(row)}</span>
        </div>
        <div class="track"><div class="fill" style="width:${pct}%"></div></div>
      </div>
    `;
  }).join("") : "<small>No rows for this month yet.</small>";
}

function categoryRows() {
  let rows = state.data.categories;
  if (state.groupId) rows = rows.filter((row) => row.groupId === state.groupId);
  if (state.uncategorizedOnly) rows = rows.filter((row) => row.id === "uncategorized" || row.category === "Uncategorized");
  return rows;
}

function pieRows() {
  if (state.groupId || state.uncategorizedOnly) return categoryRows();
  return state.data.groups.map((row) => ({
    id: row.id,
    label: row.group,
    txCount: row.txCount,
    spending: row.spending,
    type: "group",
  }));
}

function polarToCartesian(cx, cy, radius, angleInDegrees) {
  const angleInRadians = (angleInDegrees - 90) * Math.PI / 180;
  return {
    x: cx + (radius * Math.cos(angleInRadians)),
    y: cy + (radius * Math.sin(angleInRadians)),
  };
}

function describeArc(cx, cy, radius, startAngle, endAngle) {
  const start = polarToCartesian(cx, cy, radius, endAngle);
  const end = polarToCartesian(cx, cy, radius, startAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  return ["M", start.x, start.y, "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y].join(" ");
}

function selectedTransactions() {
  let rows = state.accountId ? state.data.accountTransactions : state.data.recent;
  if (state.accountId) rows = rows.filter((row) => row.accountId === state.accountId);
  if (state.groupId) {
    const group = state.data.groups.find((row) => row.id === state.groupId);
    if (group) rows = rows.filter((row) => row.group === group.group);
  }
  if (state.uncategorizedOnly) rows = rows.filter((row) => row.category === "Uncategorized");
  if (state.categoryId) {
    const category = state.data.categories.find((row) => row.id === state.categoryId);
    if (category) rows = rows.filter((row) => row.category === category.category);
  }
  return rows;
}

function renderCategories() {
  const showingGroups = !state.groupId && !state.uncategorizedOnly;
  const rows = showingGroups
    ? state.data.groups.map((row) => ({
      id: row.id,
      category: row.group,
      group: "Macro group",
      txCount: row.txCount,
      spending: row.spending,
      type: "group",
    }))
    : categoryRows();
  const max = Math.max(...rows.map((row) => row.spending), 1);
  const visibleTotal = totalSpendingForVisibleRows(rows);
  $("categories").innerHTML = rows.length ? rows.map((row) => {
    const pct = Math.min(100, (row.spending / max) * 100);
    const active = state.categoryId === row.id || state.groupId === row.id ? "active" : "";
    return `
      <button class="category-card ${active}" type="button" data-type="${row.type || "category"}" data-category-id="${row.id}">
        <span class="category-name">${row.category}</span>
        <strong>${displayMoney(row.spending, visibleTotal)}</strong>
        <small>${row.group} / ${row.txCount} tx</small>
        <span class="track"><span class="fill" style="width:${pct}%"></span></span>
      </button>
    `;
  }).join("") : "<small>No categories in this month.</small>";

  document.querySelectorAll(".category-card").forEach((button) => {
    button.addEventListener("click", () => {
      state.uncategorizedOnly = false;
      state.accountId = null;
      if (button.dataset.type === "group") {
        state.groupId = state.groupId === button.dataset.categoryId ? null : button.dataset.categoryId;
        state.categoryId = null;
      } else {
        state.categoryId = state.categoryId === button.dataset.categoryId ? null : button.dataset.categoryId;
      }
      renderPie();
      renderCategories();
      renderTransactions();
      renderChips();
    });
  });
}

function renderPie() {
  const rows = pieRows();
  const total = rows.reduce((sum, row) => sum + row.spending, 0);
  $("pieTotal").textContent = state.privacyMode ? "100%" : formatMoney(total);
  const activeGroup = state.data.groups.find((row) => row.id === state.groupId);
  const activeCategory = state.data.categories.find((row) => row.id === state.categoryId);
  $("pieSelection").textContent = state.uncategorizedOnly
    ? "Uncategorized"
    : activeCategory ? activeCategory.category : activeGroup ? activeGroup.group : "Click a group";

  if (!rows.length || total <= 0) {
    $("categoryPie").innerHTML = `<circle cx="110" cy="110" r="82" class="pie-empty"></circle>`;
    return;
  }

  let angle = 0;
  const slices = rows.map((row, index) => {
    const degrees = (row.spending / total) * 360;
    const start = angle;
    const end = angle + degrees;
    angle = end;
    const active = state.categoryId === row.id ? "active" : "";
    const groupActive = state.groupId === row.id ? "active" : "";
    const label = row.label || row.category;
    const share = (row.spending / total) * 100;
    return `
      <path
        class="pie-slice ${active} ${groupActive}"
        data-id="${row.id}"
        data-type="${row.type || "category"}"
        data-label="${label}"
        data-amount="${displayMoney(row.spending, total)}"
        data-share="${share.toFixed(1)}%"
        d="${describeArc(110, 110, 82, start, end)}"
        stroke="${pieColors[index % pieColors.length]}"
      >
        <title>${label}: ${share.toFixed(1)}%${state.privacyMode ? "" : ` / ${formatMoney(row.spending)}`}</title>
      </path>
    `;
  }).join("");
  $("categoryPie").innerHTML = slices + `<circle cx="110" cy="110" r="48" class="pie-hole"></circle>`;

  document.querySelectorAll(".pie-slice").forEach((slice) => {
    slice.addEventListener("pointerenter", () => showPieTooltip(slice));
    slice.addEventListener("pointermove", (event) => movePieTooltip(event));
    slice.addEventListener("pointerleave", hidePieTooltip);
    slice.addEventListener("click", () => {
      state.uncategorizedOnly = false;
      state.accountId = null;
      if (slice.dataset.type === "group") {
        state.groupId = state.groupId === slice.dataset.id ? null : slice.dataset.id;
        state.categoryId = null;
      } else {
        state.categoryId = state.categoryId === slice.dataset.id ? null : slice.dataset.id;
      }
      renderPie();
      renderCategories();
      renderTransactions();
      renderChips();
    });
  });
}

function showPieTooltip(slice) {
  const tooltip = $("pieTooltip");
  tooltip.innerHTML = `<strong>${slice.dataset.label}</strong><span>${slice.dataset.share} of spend${state.privacyMode ? "" : ` / ${slice.dataset.amount}`}</span>`;
  tooltip.hidden = false;
}

function movePieTooltip(event) {
  const stage = event.currentTarget.closest(".pie-stage");
  const rect = stage.getBoundingClientRect();
  $("pieTooltip").style.left = `${event.clientX - rect.left + 14}px`;
  $("pieTooltip").style.top = `${event.clientY - rect.top + 14}px`;
}

function hidePieTooltip() {
  $("pieTooltip").hidden = true;
}

function renderTransactions() {
  const rows = selectedTransactions();
  const activeGroup = state.data.groups.find((row) => row.id === state.groupId);
  const activeCategory = state.data.categories.find((row) => row.id === state.categoryId);
  const activeAccount = state.data.accounts.find((row) => row.id === state.accountId);
  $("transactionTitle").textContent = activeAccount
    ? `${activeAccount.name} Transactions`
    : state.uncategorizedOnly
      ? "Uncategorized Transactions"
      : activeCategory ? activeCategory.category : activeGroup ? activeGroup.group : "Monthly Transactions";
  $("transactionCount").textContent = `${rows.length} rows`;
  $("transactions").innerHTML = rows.map((row) => `
    <tr>
      <td>${row.date}</td>
      <td>${row.payee}</td>
      <td>${row.category}</td>
      <td>${row.account}</td>
      <td class="num ${classForAmount(row.amount)}">${displayMoney(row.amount)}</td>
    </tr>
  `).join("");
}


function renderBudgetWatch(rows) {
  const max = Math.max(...rows.map((row) => Math.max(row.spent || 0, row.budgeted || 0)), 1);
  $("budgets").innerHTML = rows.length ? rows.map((row) => {
    const pct = Math.min(100, ((row.spent || 0) / max) * 100);
    const used = row.budgeted ? `${Math.round((row.spent / row.budgeted) * 1000) / 10}% used` : "No budget";
    const fraction = row.budgeted ? `${formatMoney(row.spent)} / ${formatMoney(row.budgeted)}` : `${formatMoney(row.spent)} spent`;
    const budgetText = state.privacyMode
      ? `${used} · ${displayMoney(row.spent, row.budgeted || row.spent)}`
      : `${used} · ${fraction}`;
    const categories = (row.categories || []).map((category) => `
      <div class="budget-child">
        <span>${category.category}</span>
        <strong>${displayMoney(category.spending, row.spent || category.spending)}</strong>
      </div>
    `).join("");
    return `
      <details class="budget-group">
        <summary>
          <span class="chevron">›</span>
          <strong>${row.group}</strong>
          <span>${budgetText}</span>
        </summary>
        <div class="track"><div class="fill" style="width:${pct}%"></div></div>
        <div class="budget-children">${categories || "<small>No spending categories this month.</small>"}</div>
      </details>
    `;
  }).join("") : "<small>No budget rows for this month.</small>";
}

function renderMonthOptions(months) {
  const select = $("monthSelect");
  select.innerHTML = months.map((month) => `<option value="${month}">${month}</option>`).join("");
  select.value = state.data.currentMonth;
}

function renderChips() {
  $("allCategories").textContent = state.groupId ? "All Groups" : "All Groups";
  $("allCategories").classList.toggle("active", !state.uncategorizedOnly && !state.categoryId && !state.groupId);
  $("uncategorizedOnly").classList.toggle("active", state.uncategorizedOnly);
}

function renderAll() {
  const data = state.data;
  $("categoryMonth").textContent = data.currentMonth;
  document.body.classList.toggle("privacy-mode", state.privacyMode);
  $("privacyToggle").setAttribute("aria-pressed", String(state.privacyMode));
  $("privacyToggle").textContent = state.privacyMode ? "Show Dollars" : "Percent Mode";
  $("netWorth").textContent = state.privacyMode ? "100%" : formatMoney(data.netWorth);
  $("cashBalance").textContent = displayMoney(data.cashBalance, data.netWorth);
  $("debtBalance").textContent = displayMoney(data.debtBalance, data.netWorth);
  $("monthNet").textContent = displayMoney(data.latestMonth.net, data.latestMonth.outflow);
  $("monthNet").className = classForAmount(data.latestMonth.net);
  $("monthInflow").textContent = displayMoney(data.latestMonth.inflow, data.latestMonth.outflow);
  $("monthOutflow").textContent = state.privacyMode ? "100%" : formatMoney(data.latestMonth.outflow);
  renderMonthOptions(data.availableMonths);
  renderCashChart(data.monthly);
  renderAccounts(data.accounts);
  renderPie();
  renderCategories();
  renderTransactions();
  renderBars("groups", data.groups, "spending", "group", (row) => `${displayMoney(row.spending)} / ${row.txCount} tx`);
  renderBudgetWatch(data.budgets);
  renderChips();
}

async function loadSummary(month = state.month) {
  setStatus("Reading db.sqlite...");
  const url = month ? `/api/summary?month=${encodeURIComponent(month)}` : "/api/summary";
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Summary failed: ${response.status}`);
  state.data = await response.json();
  state.month = state.data.currentMonth;
  state.groupId = null;
  state.categoryId = null;
  state.uncategorizedOnly = false;
  state.accountId = null;
  renderAll();
  setStatus("Ready");
}

async function syncSimpleFin() {
  $("sync").disabled = true;
  setStatus("Syncing SimpleFIN...");
  try {
    const response = await fetch("/api/sync", { method: "POST" });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `Sync failed: ${response.status}`);
    setStatus(`Synced: ${data.transactions_inserted} new, ${data.transactions_skipped} skipped. Backup made.`);
    await loadSummary(state.month);
  } catch (error) {
    setStatus(error.message);
  } finally {
    $("sync").disabled = false;
  }
}

$("refresh").addEventListener("click", () => loadSummary(state.month).catch((error) => setStatus(error.message)));
$("sync").addEventListener("click", syncSimpleFin);
$("privacyToggle").addEventListener("click", () => {
  state.privacyMode = !state.privacyMode;
  renderAll();
});
$("monthSelect").addEventListener("change", (event) => loadSummary(event.target.value).catch((error) => setStatus(error.message)));
$("allCategories").addEventListener("click", () => {
  state.groupId = null;
  state.categoryId = null;
  state.uncategorizedOnly = false;
  state.accountId = null;
  renderPie();
  renderCategories();
  renderTransactions();
  renderChips();
});
$("uncategorizedOnly").addEventListener("click", () => {
  state.groupId = null;
  state.categoryId = null;
  state.accountId = null;
  state.uncategorizedOnly = !state.uncategorizedOnly;
  renderPie();
  renderCategories();
  renderTransactions();
  renderChips();
});

loadSummary().catch((error) => setStatus(error.message));
