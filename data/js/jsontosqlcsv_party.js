const fs = require("fs-extra");
const path = require("path");
const exportType = "parties";
const inFile = path.join(__dirname, `../${exportType}.json`);
const outFile = path.join(__dirname, `../db/${exportType}.csv`);

let data = fs.readFileSync(inFile);

data = JSON.parse(data);

let rowData = "id|pid|code|name_np|name_en|short_np|short_en|color|symbol|created_at|updated_at" + "\r\n";
data.parties.forEach((p, pi) => {
  rowData += `${pi + 1}|${p.id}|${p.code}|${p.name_np}|${p.name_en}|${p.short_name_np || p.name_np}|${p.short_name_en || p.name_en}|${p.color}|${p.symbol}|${new Date().toISOString().slice(0, 19).replace("T", " ")}|${new Date().toISOString().slice(0, 19).replace("T", " ")}\r\n`;
});
fs.writeFileSync(outFile, rowData);
