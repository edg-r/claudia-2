/**
 * GO GPS Inventory automation for the Google Sheets version.
 *
 * Install:
 * 1. Open the TEST workbook after importing it into Google Sheets.
 * 2. Go to Extensions > Apps Script.
 * 3. Paste this file into the script editor and save.
 * 4. Run setupInventoryAutomation once and approve permissions.
 *
 * What it does:
 * - Assigns stable GOGPS-0001 style Item IDs when new Inventory rows are added.
 * - Preserves existing Item IDs.
 * - Adds Date Added / Last Updated values.
 * - Reinstalls formula columns if a new row is inserted.
 * - Applies low/out/watch/healthy consumable color rules.
 */

const GO_GPS_CONFIG = {
  inventorySheetName: "Inventory",
  checkoutSheetName: "Checkouts Returns",
  legacyCheckoutSheetName: "Checkouts & Returns",
  dashboardSheetName: "TEST Dashboard",
  idPrefix: "GOGPS-",
  idDigits: 4,
  firstDataRow: 2,
  nextIdProperty: "GO_GPS_NEXT_ITEM_NUMBER",
};

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("GO GPS Inventory")
    .addItem("Set up automation", "setupInventoryAutomation")
    .addItem("Repair Inventory sheet for AppSheet", "repairInventorySheetForAppSheet")
    .addItem("Backfill missing Item IDs", "backfillMissingItemIds")
    .addToUi();
}

function doGet() {
  return HtmlService.createHtmlOutputFromFile("Index")
    .setTitle("GO GPS Inventory Intake")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function onEdit(e) {
  if (!e || !e.range) return;
  const sheet = e.range.getSheet();
  if (sheet.getName() !== GO_GPS_CONFIG.inventorySheetName) return;

  const lock = LockService.getDocumentLock();
  lock.waitLock(5000);
  try {
    handleInventoryEdit_(sheet, e.range);
  } finally {
    lock.releaseLock();
  }
}

function setupInventoryAutomation() {
  const ss = SpreadsheetApp.getActive();
  const inventory = ss.getSheetByName(GO_GPS_CONFIG.inventorySheetName);
  const dashboard = ss.getSheetByName(GO_GPS_CONFIG.dashboardSheetName);
  if (!inventory) throw new Error(`Missing sheet: ${GO_GPS_CONFIG.inventorySheetName}`);

  const headers = getHeaderMap_(inventory);
  inventory.getRange("B:B").setNumberFormat("@");
  inventory.getRange("G:I").setNumberFormat("0");
  inventory.getRange("J:K").setNumberFormat("$#,##0.00");
  inventory.getRange("L:L").setNumberFormat("@");
  inventory.getRange("M:M").setNumberFormat("0");
  inventory.getRange("R:S").setNumberFormat("yyyy-mm-dd");
  applyInventorySheetValidation_(inventory, headers);
  normalizeConsumableValues_(inventory, headers);

  const lastFormulaRow = Math.max(inventory.getMaxRows(), 501);
  for (let row = GO_GPS_CONFIG.firstDataRow; row <= lastFormulaRow; row += 1) {
    installInventoryRowFormulas_(inventory, row, headers);
  }

  applyConsumableConditionalFormatting_(inventory, dashboard);
  backfillMissingItemIds();
}

function repairInventorySheetForAppSheet() {
  const ss = SpreadsheetApp.getActive();
  const inventory = ss.getSheetByName(GO_GPS_CONFIG.inventorySheetName);
  const dashboard = ss.getSheetByName(GO_GPS_CONFIG.dashboardSheetName);
  if (!inventory) throw new Error(`Missing sheet: ${GO_GPS_CONFIG.inventorySheetName}`);

  const headers = getHeaderMap_(inventory);
  inventory.getRange("B:B").setNumberFormat("@");
  inventory.getRange("G:I").setNumberFormat("0");
  inventory.getRange("J:K").setNumberFormat("$#,##0.00");
  inventory.getRange("L:L").setNumberFormat("@");
  inventory.getRange("M:M").setNumberFormat("0");
  inventory.getRange("R:S").setNumberFormat("yyyy-mm-dd");

  applyInventorySheetValidation_(inventory, headers);
  normalizeConsumableValues_(inventory, headers);

  const lastFormulaRow = Math.max(inventory.getMaxRows(), 501);
  for (let row = GO_GPS_CONFIG.firstDataRow; row <= lastFormulaRow; row += 1) {
    installInventoryRowFormulas_(inventory, row, headers);
  }

  applyConsumableConditionalFormatting_(inventory, dashboard);
  backfillMissingItemIds();
}

function getInventoryFormOptions() {
  const ss = SpreadsheetApp.getActive();
  const lists = ss.getSheetByName("Lists");
  if (!lists) {
    return {
      categories: [],
      clubs: [],
      locations: [],
      conditions: ["New", "Good", "Fair", "Needs Repair"],
      lookupStatuses: ["Manual entry", "UPC lookup pending"],
    };
  }

  const values = lists.getDataRange().getDisplayValues();
  const headers = values[0] || [];
  const columnValues = (header) => {
    const index = headers.indexOf(header);
    if (index === -1) return [];
    return values
      .slice(1)
      .map((row) => row[index])
      .filter((value) => String(value || "").trim() !== "");
  };

  return {
    clubs: columnValues("Clubs / Owners"),
    categories: columnValues("Categories"),
    locations: columnValues("Locations"),
    conditions: columnValues("Conditions"),
    lookupStatuses: columnValues("Lookup Statuses"),
  };
}

function findInventoryItemByBarcode(barcode) {
  const ss = SpreadsheetApp.getActive();
  const sheet = ss.getSheetByName(GO_GPS_CONFIG.inventorySheetName);
  if (!sheet) throw new Error(`Missing sheet: ${GO_GPS_CONFIG.inventorySheetName}`);

  const headers = getHeaderMap_(sheet);
  const normalized = normalizeBarcode_(barcode);
  const row = findInventoryRowByBarcode_(sheet, headers, normalized);
  if (!row) return { found: false, barcode: normalized };

  const rowValues = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getDisplayValues()[0];
  const get = (header) => rowValues[(headers[header] || 1) - 1] || "";
  return {
    found: true,
    row,
    itemId: get("Item ID"),
    barcode: get("Barcode/UPC"),
    itemName: get("Item Name"),
    category: get("Category"),
    clubOwner: get("Club/Owner"),
    location: get("Location"),
    quantityTotal: get("Quantity Total"),
    quantityAvailable: get("Quantity Available"),
    unitCost: get("Unit Cost"),
    consumable: get("Consumable?"),
    reorderLevel: get("Reorder Level"),
    condition: get("Condition"),
    notes: get("Notes"),
  };
}

function addScannedItemToInventory(payload) {
  const ss = SpreadsheetApp.getActive();
  const sheet = ss.getSheetByName(GO_GPS_CONFIG.inventorySheetName);
  if (!sheet) throw new Error(`Missing sheet: ${GO_GPS_CONFIG.inventorySheetName}`);

  const lock = LockService.getDocumentLock();
  lock.waitLock(5000);
  try {
    const headers = getHeaderMap_(sheet);
    const barcode = normalizeBarcode_(payload && payload.barcode);
    const quantity = Math.max(1, Number(payload && payload.quantity) || 1);
    const existingRow = barcode ? findInventoryRowByBarcode_(sheet, headers, barcode) : 0;
    const targetRow = existingRow || nextBlankInventoryRow_(sheet, headers);

    if (existingRow) {
      const quantityCell = sheet.getRange(targetRow, headers["Quantity Total"]);
      const currentQuantity = Number(quantityCell.getValue()) || 0;
      quantityCell.setValue(currentQuantity + quantity);
      fillBlankInventoryFields_(sheet, targetRow, headers, payload);
      ensureInventoryRowAutomation_(sheet, targetRow, headers);
      return {
        status: "updated",
        row: targetRow,
        itemId: sheet.getRange(targetRow, headers["Item ID"]).getDisplayValue(),
        message: `Updated existing item quantity by ${quantity}.`,
      };
    }

    writeInventoryPayload_(sheet, targetRow, headers, payload, barcode, quantity);
    ensureInventoryRowAutomation_(sheet, targetRow, headers);
    return {
      status: "added",
      row: targetRow,
      itemId: sheet.getRange(targetRow, headers["Item ID"]).getDisplayValue(),
      message: "Added new inventory item.",
    };
  } finally {
    lock.releaseLock();
  }
}

function backfillMissingItemIds() {
  const ss = SpreadsheetApp.getActive();
  const sheet = ss.getSheetByName(GO_GPS_CONFIG.inventorySheetName);
  if (!sheet) throw new Error(`Missing sheet: ${GO_GPS_CONFIG.inventorySheetName}`);

  const lock = LockService.getDocumentLock();
  lock.waitLock(5000);
  try {
    const headers = getHeaderMap_(sheet);
    const lastRow = Math.max(sheet.getLastRow(), GO_GPS_CONFIG.firstDataRow);
    for (let row = GO_GPS_CONFIG.firstDataRow; row <= lastRow; row += 1) {
      if (inventoryRowHasUserData_(sheet, row, headers)) {
        ensureInventoryRowAutomation_(sheet, row, headers);
      }
    }
  } finally {
    lock.releaseLock();
  }
}

function handleInventoryEdit_(sheet, editedRange) {
  const headers = getHeaderMap_(sheet);
  const startRow = Math.max(editedRange.getRow(), GO_GPS_CONFIG.firstDataRow);
  const endRow = editedRange.getLastRow();

  for (let row = startRow; row <= endRow; row += 1) {
    if (inventoryRowHasUserData_(sheet, row, headers)) {
      ensureInventoryRowAutomation_(sheet, row, headers);
    }
  }
}

function ensureInventoryRowAutomation_(sheet, row, headers) {
  const itemIdCell = sheet.getRange(row, headers["Item ID"]);
  if (!itemIdCell.getValue()) {
    itemIdCell.setValue(nextItemId_(sheet, headers["Item ID"]));
  }

  const now = new Date();
  const dateAddedCell = sheet.getRange(row, headers["Date Added"]);
  if (!dateAddedCell.getValue()) {
    dateAddedCell.setValue(now);
  }
  sheet.getRange(row, headers["Last Updated"]).setValue(now);
  sheet.getRange(row, headers["Barcode/UPC"]).setNumberFormat("@");
  installInventoryRowFormulas_(sheet, row, headers);
}

function installInventoryRowFormulas_(sheet, row, headers) {
  const checkoutSheetName = quoteSheetName_(getCheckoutSheetName_());
  if (headers["Quantity Checked Out"]) {
    sheet.getRange(row, headers["Quantity Checked Out"]).setFormula(
      `=IF($A${row}="","",MAX(0,SUMIFS(${checkoutSheetName}!$G:$G,${checkoutSheetName}!$D:$D,$A${row},${checkoutSheetName}!$C:$C,"Checkout")+IF($B${row}="",0,SUMIFS(${checkoutSheetName}!$G:$G,${checkoutSheetName}!$D:$D,$B${row},${checkoutSheetName}!$C:$C,"Checkout"))-SUMIFS(${checkoutSheetName}!$G:$G,${checkoutSheetName}!$D:$D,$A${row},${checkoutSheetName}!$C:$C,"Return")-IF($B${row}="",0,SUMIFS(${checkoutSheetName}!$G:$G,${checkoutSheetName}!$D:$D,$B${row},${checkoutSheetName}!$C:$C,"Return"))))`
    );
  }
  if (headers["Quantity Available"]) {
    sheet.getRange(row, headers["Quantity Available"]).setFormula(`=IF($A${row}="","",MAX(0,$G${row}-$H${row}))`);
  }
  if (headers["Total Value"]) {
    sheet.getRange(row, headers["Total Value"]).setFormula(`=IF($A${row}="","",$G${row}*$J${row})`);
  }
  if (headers["Consumable Level"]) {
    sheet.getRange(row, headers["Consumable Level"]).setFormula(
      `=IF($A${row}="","",IF($L${row}<>"Yes","N/A",IF($I${row}=0,"Out",IF($I${row}<=$M${row},"Low",IF($I${row}<=$M${row}*2,"Watch","Healthy")))))`
    );
  }
  if (headers["Status"]) {
    sheet.getRange(row, headers["Status"]).setFormula(
      `=IF($A${row}="","",IF($O${row}="Needs Repair","Needs Repair",IF($O${row}="Missing","Missing",IF($O${row}="Retired","Retired",IF($I${row}=0,"Checked Out","Available")))))`
    );
  }
}

function applyInventorySheetValidation_(sheet, headers) {
  const maxRows = Math.max(sheet.getMaxRows(), 501);
  const rowCount = maxRows - GO_GPS_CONFIG.firstDataRow + 1;

  if (headers["Quantity Total"]) {
    sheet
      .getRange(GO_GPS_CONFIG.firstDataRow, headers["Quantity Total"], rowCount, 1)
      .setDataValidation(
        SpreadsheetApp.newDataValidation()
          .requireFormulaSatisfied(`=AND(ISNUMBER(G${GO_GPS_CONFIG.firstDataRow}),G${GO_GPS_CONFIG.firstDataRow}=INT(G${GO_GPS_CONFIG.firstDataRow}),G${GO_GPS_CONFIG.firstDataRow}>=0)`)
          .setAllowInvalid(false)
          .setHelpText("Enter 0 or a positive whole number.")
          .build()
      );
  }

  if (headers["Reorder Level"]) {
    sheet
      .getRange(GO_GPS_CONFIG.firstDataRow, headers["Reorder Level"], rowCount, 1)
      .setDataValidation(
        SpreadsheetApp.newDataValidation()
          .requireFormulaSatisfied(`=AND(ISNUMBER(M${GO_GPS_CONFIG.firstDataRow}),M${GO_GPS_CONFIG.firstDataRow}=INT(M${GO_GPS_CONFIG.firstDataRow}),M${GO_GPS_CONFIG.firstDataRow}>=0)`)
          .setAllowInvalid(false)
          .setHelpText("Enter 0 or a positive whole number.")
          .build()
      );
  }

  if (headers["Consumable?"]) {
    sheet
      .getRange(GO_GPS_CONFIG.firstDataRow, headers["Consumable?"], rowCount, 1)
      .setDataValidation(
        SpreadsheetApp.newDataValidation()
          .requireValueInList(["Yes", "No"], true)
          .setAllowInvalid(false)
          .setHelpText("Choose Yes or No.")
          .build()
      );
  }
}

function normalizeConsumableValues_(sheet, headers) {
  const col = headers["Consumable?"];
  if (!col) return;

  const lastRow = Math.max(sheet.getLastRow(), GO_GPS_CONFIG.firstDataRow);
  const range = sheet.getRange(GO_GPS_CONFIG.firstDataRow, col, lastRow - GO_GPS_CONFIG.firstDataRow + 1, 1);
  const values = range.getValues().map(([value]) => {
    const text = String(value || "").trim().toLowerCase();
    if (value === true || text === "true" || text === "yes") return ["Yes"];
    if (value === false || text === "false" || text === "no") return ["No"];
    return [value];
  });
  range.setNumberFormat("@");
  range.setValues(values);
}

function getCheckoutSheetName_() {
  const ss = SpreadsheetApp.getActive();
  if (ss.getSheetByName(GO_GPS_CONFIG.checkoutSheetName)) return GO_GPS_CONFIG.checkoutSheetName;
  if (ss.getSheetByName(GO_GPS_CONFIG.legacyCheckoutSheetName)) return GO_GPS_CONFIG.legacyCheckoutSheetName;
  return GO_GPS_CONFIG.checkoutSheetName;
}

function quoteSheetName_(sheetName) {
  return `'${String(sheetName).replace(/'/g, "''")}'`;
}

function nextItemId_(sheet, itemIdCol) {
  const props = PropertiesService.getDocumentProperties();
  const storedNext = Number(props.getProperty(GO_GPS_CONFIG.nextIdProperty) || 1);
  const maxRow = Math.max(sheet.getLastRow(), GO_GPS_CONFIG.firstDataRow);
  const values = sheet
    .getRange(GO_GPS_CONFIG.firstDataRow, itemIdCol, maxRow - GO_GPS_CONFIG.firstDataRow + 1, 1)
    .getValues()
    .flat();

  const pattern = new RegExp(`^${GO_GPS_CONFIG.idPrefix}(\\d+)$`);
  const existingMax = values.reduce((max, value) => {
    const match = String(value || "").trim().match(pattern);
    return match ? Math.max(max, Number(match[1])) : max;
  }, 0);

  const nextNumber = Math.max(storedNext, existingMax + 1);
  props.setProperty(GO_GPS_CONFIG.nextIdProperty, String(nextNumber + 1));
  return `${GO_GPS_CONFIG.idPrefix}${String(nextNumber).padStart(GO_GPS_CONFIG.idDigits, "0")}`;
}

function inventoryRowHasUserData_(sheet, row, headers) {
  const userColumns = [
    "Barcode/UPC",
    "Item Name",
    "Category",
    "Club/Owner",
    "Location",
    "Quantity Total",
    "Unit Cost",
    "Consumable?",
    "Reorder Level",
    "Condition",
    "Photo Link",
    "Lookup Status",
    "Notes",
  ];
  return userColumns.some((header) => {
    const col = headers[header];
    if (!col) return false;
    return String(sheet.getRange(row, col).getDisplayValue() || "").trim() !== "";
  });
}

function getHeaderMap_(sheet) {
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getDisplayValues()[0];
  return headers.reduce((map, header, index) => {
    if (header) map[String(header).trim()] = index + 1;
    return map;
  }, {});
}

function applyConsumableConditionalFormatting_(inventory, dashboard) {
  const rules = [];
  const levelRange = inventory.getRange("N2:N501");
  const availableRange = inventory.getRange("I2:I501");
  const statusRange = inventory.getRange("P2:P501");

  rules.push(
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Out").setBackground("#F8C7C7").setFontColor("#7A1E1E").setBold(true).setRanges([levelRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Low").setBackground("#F8D7A8").setFontColor("#7A4C00").setBold(true).setRanges([levelRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Watch").setBackground("#F8E3B6").setFontColor("#5E4B00").setBold(true).setRanges([levelRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Healthy").setBackground("#CFE7C8").setFontColor("#245A32").setBold(true).setRanges([levelRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("N/A").setBackground("#EEF2F3").setFontColor("#6B7A80").setRanges([levelRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=AND($L2="Yes",$I2=0)').setBackground("#F8C7C7").setFontColor("#7A1E1E").setBold(true).setRanges([availableRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=AND($L2="Yes",$I2>0,$I2<=$M2)').setBackground("#F8D7A8").setFontColor("#7A4C00").setBold(true).setRanges([availableRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenFormulaSatisfied('=AND($L2="Yes",$I2>$M2,$I2<=$M2*2)').setBackground("#F8E3B6").setFontColor("#5E4B00").setBold(true).setRanges([availableRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Checked Out").setBackground("#D9ECF8").setFontColor("#25536B").setBold(true).setRanges([statusRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Needs Repair").setBackground("#F8E3B6").setFontColor("#5E4B00").setBold(true).setRanges([statusRange]).build(),
    SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo("Missing").setBackground("#F8C7C7").setFontColor("#7A1E1E").setBold(true).setRanges([statusRange]).build()
  );

  inventory.setConditionalFormatRules(rules);

  if (dashboard) {
    dashboard.setConditionalFormatRules([
      SpreadsheetApp.newConditionalFormatRule().whenNumberGreaterThan(0).setBackground("#F8D7A8").setFontColor("#7A4C00").setBold(true).setRanges([dashboard.getRange("F5")]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenNumberGreaterThan(0).setBackground("#F8C7C7").setFontColor("#7A1E1E").setBold(true).setRanges([dashboard.getRange("H5")]).build(),
    ]);
  }
}

function findInventoryRowByBarcode_(sheet, headers, barcode) {
  if (!barcode || !headers["Barcode/UPC"]) return 0;
  const lastRow = Math.max(sheet.getLastRow(), GO_GPS_CONFIG.firstDataRow);
  const values = sheet
    .getRange(GO_GPS_CONFIG.firstDataRow, headers["Barcode/UPC"], lastRow - GO_GPS_CONFIG.firstDataRow + 1, 1)
    .getDisplayValues()
    .flat();
  const index = values.findIndex((value) => normalizeBarcode_(value) === barcode);
  return index === -1 ? 0 : GO_GPS_CONFIG.firstDataRow + index;
}

function nextBlankInventoryRow_(sheet, headers) {
  const itemIdCol = headers["Item ID"] || 1;
  const lastRow = Math.max(sheet.getLastRow(), GO_GPS_CONFIG.firstDataRow);
  const values = sheet
    .getRange(GO_GPS_CONFIG.firstDataRow, itemIdCol, lastRow - GO_GPS_CONFIG.firstDataRow + 1, 1)
    .getDisplayValues()
    .flat();
  const blankIndex = values.findIndex((value) => String(value || "").trim() === "");
  return blankIndex === -1 ? lastRow + 1 : GO_GPS_CONFIG.firstDataRow + blankIndex;
}

function writeInventoryPayload_(sheet, row, headers, payload, barcode, quantity) {
  setInventoryValue_(sheet, row, headers, "Barcode/UPC", barcode, true);
  setInventoryValue_(sheet, row, headers, "Item Name", payload.itemName);
  setInventoryValue_(sheet, row, headers, "Category", payload.category);
  setInventoryValue_(sheet, row, headers, "Club/Owner", payload.clubOwner);
  setInventoryValue_(sheet, row, headers, "Location", payload.location);
  setInventoryValue_(sheet, row, headers, "Quantity Total", quantity);
  setInventoryValue_(sheet, row, headers, "Unit Cost", Number(payload.unitCost) || 0);
  setInventoryValue_(sheet, row, headers, "Consumable?", payload.consumable || "No");
  setInventoryValue_(sheet, row, headers, "Reorder Level", Number(payload.reorderLevel) || 0);
  setInventoryValue_(sheet, row, headers, "Condition", payload.condition || "Good");
  setInventoryValue_(sheet, row, headers, "Photo Link", payload.photoLink);
  setInventoryValue_(sheet, row, headers, "Lookup Status", payload.lookupStatus || "Manual entry");
  setInventoryValue_(sheet, row, headers, "Notes", payload.notes);
}

function fillBlankInventoryFields_(sheet, row, headers, payload) {
  const fields = [
    ["Item Name", payload.itemName],
    ["Category", payload.category],
    ["Club/Owner", payload.clubOwner],
    ["Location", payload.location],
    ["Unit Cost", payload.unitCost],
    ["Consumable?", payload.consumable],
    ["Reorder Level", payload.reorderLevel],
    ["Condition", payload.condition],
    ["Photo Link", payload.photoLink],
    ["Lookup Status", payload.lookupStatus || "Manual entry"],
    ["Notes", payload.notes],
  ];
  fields.forEach(([header, value]) => {
    if (value === undefined || value === null || value === "") return;
    const col = headers[header];
    if (!col) return;
    const cell = sheet.getRange(row, col);
    if (!cell.getValue()) cell.setValue(value);
  });
}

function setInventoryValue_(sheet, row, headers, header, value, asText) {
  const col = headers[header];
  if (!col) return;
  const cell = sheet.getRange(row, col);
  if (asText) cell.setNumberFormat("@");
  cell.setValue(value === undefined || value === null ? "" : value);
}

function normalizeBarcode_(barcode) {
  return String(barcode || "").trim().replace(/\s+/g, "");
}
