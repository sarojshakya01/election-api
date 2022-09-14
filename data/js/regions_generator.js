const fs = require("fs-extra");
const path = require("path");
const dataType = "districts";
const inFile = path.join(__dirname, `../${dataType}.json`);
const inFile2 = path.join(__dirname, `../federal.json`);
const outFile = path.join(__dirname, `../f${dataType}.json`);
let data = fs.readFileSync(inFile);
data = JSON.parse(data);

let data2 = fs.readFileSync(inFile2);
data2 = JSON.parse(data2);

const translateNumber = (num) => {
  num = num.toString();

  if (num.includes(".1")) {
    num = parseFloat(num).toFixed(1).replace(".1", "(क)");
  } else if (num.includes(".2")) {
    num = parseFloat(num).toFixed(1).replace(".2", "(ख)");
  }
  num = num.replace(/0/g, "०");
  num = num.replace(/1/g, "१");
  num = num.replace(/2/g, "२");
  num = num.replace(/3/g, "३");
  num = num.replace(/4/g, "४");
  num = num.replace(/5/g, "५");
  num = num.replace(/6/g, "६");
  num = num.replace(/7/g, "७");
  num = num.replace(/8/g, "८");
  num = num.replace(/9/g, "९");
  return num;
};

let newData = { ...data };
data2.provinces.forEach((p) => {
  p.districts.forEach((d) => {
    let fregions = d.regions.map((r) => ({
      region_id: r.id,
      rtype: "federal",
      district_id: d.id,
      province_id: p.id,
      name_np: translateNumber(r.id),
      name_en: r.id,
    }));

    let pregions = [];
    fregions.forEach((r) => {
      let p1 = {
        region_id: r.ern + 0.1,
        rtype: "provincial",
        district_id: d.id,
        province_id: p.id,
        name_np: translateNumber(r.ern + 0.1),
        name_en: r.ern + 0.1,
      };
      let p2 = {
        region_id: r.ern + 0.2,
        rtype: "provincial",
        district_id: d.id,
        province_id: p.id,
        name_np: translateNumber(r.ern + 0.2),
        name_en: r.ern + 0.2,
      };
      pregions.push(p1);
      pregions.push(p2);
    });
    let dist = data.provinces.find((pro) => pro.id === p.id).districts.find((dist) => dist.id === d.id);
    dist.regions = [...fregions, ...pregions];
  });
});

// data2.provinces.forEach((p) => {
//   p.districts.forEach((d) => {
//     let dist = data.provinces.find((pro) => pro.id === p.id).districts.find((dist) => dist.id === d.id);
//     dist.total_fregions = d.regions.length;
//     dist.total_pregions = 2 * d.regions.length;
//   });
// });

fs.writeFileSync(outFile, JSON.stringify(newData));
