const fs = require("fs-extra");
const path = require("path");
const exportType = "federal"; // "federal" | "provincial" | "provinces" | "districts" | regions
const inFile = path.join(__dirname, `../${exportType}.json`);
const outFile = path.join(__dirname, `../db/${exportType}.csv`);

let data = fs.readFileSync(inFile);

data = JSON.parse(data);

let rowData = "id|pid|did|rid|rtype|declared|result|elected|created_at|updated_at" + "\r\n";
let rowDataProvince = "id|pid|name_np|name_en|color|created_at|updated_at" + "\r\n";
let rowDataDistrict = "id|did|pid|name_np|name_en|tfr|tpr|created_at|updated_at" + "\r\n";
let rowDataRegion = "id|rid|did|pid|rtype|name_np|name_en|created_at|updated_at" + "\r\n";
let dcount = 1;
let rcount = 1;
let count = 1;
data.provinces.forEach((p, pi) => {
  if (exportType === "provinces") {
    rowDataProvince += `${pi + 1}|${p.id}|${p.name_np}|${p.name_en}|${p.color}|${new Date().toISOString().slice(0, 19).replace("T", " ")}|${new Date().toISOString().slice(0, 19).replace("T", " ")}\r\n`;
  }
  p.districts.forEach((d) => {
    if (exportType === "districts") {
      rowDataDistrict += `${dcount}|${d.id}|${p.id}|${d.name_np}|${d.name_en}|${d.total_fregions}|${d.total_pregions}|${new Date().toISOString().slice(0, 19).replace("T", " ")}|${new Date().toISOString().slice(0, 19).replace("T", " ")}\r\n`;
      dcount++;
    } else if (exportType === "regions") {
      d.regions.forEach((r) => {
        rowDataRegion += `${rcount}|${r.id}|${d.id}|${p.id}|${r.rtype}|${r.name_np}|${r.name_en}|${new Date().toISOString().slice(0, 19).replace("T", " ")}|${new Date().toISOString().slice(0, 19).replace("T", " ")}\r\n`;
        rcount++;
      });
    } else {
      d.regions.forEach((r, i) => {
        let result = "[";
        r.result.forEach((res) => {
          result += JSON.stringify(res) + ",";
        });

        result = result.replace(/"/g, '""');
        result = result.replace(/,\s*$/, "");

        result += "]";
        if (i === 2) {
          r.elected = r.result.sort((a, b) => b.vote - a.vote)[0];
          r.declared = 1;
        } else {
          r.elected = {};
          r.declared = 0;
        }
        r.elected = JSON.stringify(r.elected).replace(/"/g, '""');
        let rData = `${count}|"${p.id}"|"${d.id}"|"${r.id}"|${exportType}|"${r.declared}"|"${result}"|"${r.elected}"|"${new Date().toISOString().slice(0, 19).replace("T", " ")}"|"${new Date().toISOString().slice(0, 19).replace("T", " ")}"\r\n`;
        rowData += rData;
        count++;
      });
    }
  });
});
if (exportType === "provinces") {
  fs.writeFileSync(outFile, rowDataProvince);
} else if (exportType === "districts") {
  fs.writeFileSync(outFile, rowDataDistrict);
} else if (exportType === "regions") {
  fs.writeFileSync(outFile, rowDataRegion);
} else {
  fs.writeFileSync(outFile, rowData);
}
