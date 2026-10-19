// Paste this into your sign-up Google Sheet: Extensions > Apps Script.
// Each website sign-up is added as a new row. Only you can see the sheet;
// the website can add rows but can't read anything.
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (sheet.getLastRow() === 0) sheet.appendRow(["Date", "Email", "First name"]);
  const email = String(e.parameter.email || "").trim();
  if (email) sheet.appendRow([new Date(), email, String(e.parameter.fname || "").trim()]);
  return ContentService.createTextOutput("ok");
}
