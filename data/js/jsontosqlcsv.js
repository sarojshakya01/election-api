const fs = require("fs-extra");
const path = require("path");
const dataType = "provincial"; // "federal" | "provincial" | "districts"
const inFile = path.join(__dirname, `../${dataType}.json`);
const outFile = path.join(__dirname, `../db/${dataType}.csv`);

let data = fs.readFileSync(inFile);

data = JSON.parse(data);

let rowData = "pid|did|type|rid|declared|result|elected|created_at|updated_at" + "\r\n";

let rowDataProvince = "id|pid|name_np|name_en|created_at|updated_at" + "\r\n";
let rowDataDistrict = "id|did|pid|name_np|name_en|created_at|updated_at" + "\r\n";
let dcount = 1;
data.provinces.forEach((p, pi) => {
  rowDataProvince += `${pi + 1}|${p.id}|${p.name_np}|${p.name_en}|${new Date().toISOString().slice(0, 19).replace('T', ' ')}|${new Date().toISOString().slice(0, 19).replace('T', ' ')}\r\n`;
  p.districts.forEach((d, di) => {
    if (dataType === "districts") {
      rowDataDistrict += `${dcount}|${d.id}|${p.id}|${p.name_np}|${p.name_en}|${new Date().toISOString().slice(0, 19).replace('T', ' ')}|${new Date().toISOString().slice(0, 19).replace('T', ' ')}\r\n`;
      dcount++;
    } else {
      d.regions.forEach((r, i) => {
        let result = "[";
        r.result.forEach((res) => {
          result += JSON.stringify(res) + ",";
        });

        result = result.replaceAll('"', '""');
        result = result.replace(/,\s*$/, "");

        result += "]";
        if (i === 2) {
          r.elected = r.result.sort((a, b) => b.vote - a.vote)[0];
          r.declared = 1;
        } else {
          r.elected = {};
          r.declared = 0;
        }
        r.elected = JSON.stringify(r.elected).replaceAll('"', '""');
        let rData = `"${p.id}"|"${d.id}"|${dataType}|"${r.id}"|"${r.declared}"|"${result}"|"${r.elected}"|"${new Date().toISOString().slice(0, 19).replace('T', ' ')}"|"${new Date().toISOString().slice(0, 19).replace('T', ' ')}"\r\n`;
        rowData += rData;
      });
    }
  });
});

if (dataType === "districts") {
  fs.writeFileSync(outFile, rowDataDistrict);
  fs.writeFileSync(outFile.replace("districts", "provinces"), rowDataProvince);
} else {
  fs.writeFileSync(outFile, rowData);
}
