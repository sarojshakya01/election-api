const fs = require("fs-extra");
const path = require("path");
const dataType = "provincial"; // "federal" | "proovincial"
const inFile = path.join(__dirname, `${dataType}.sample.json`);
const outFile = path.join(__dirname, `../${dataType}.json`);
let data = fs.readFileSync(inFile);
data = JSON.parse(data);

// make province record
// newData = data.provinces.map((p) => {
//   p.districts.map((d) => {
//     var tempR = [];
//     d.regions.forEach((r) => {
//       r.id = Math.round((r.id + 0.1) * 10) / 10;
//       tempR.push(r);
//       var r2 = { ...r };
//       r2.id = Math.round((r.id + 0.1) * 10) / 10;
//       tempR.push(r2);
//     });
//     d.regions = tempR;
//     return d;
//   });
//   return p;
// });

var names_np = ["पुष्पकमल दाहाल", "केपी ओली", "शेरबहादुर देउवा", "माधव कुमार नेपाल", "जलनाथ खनाल", "बाबुरल भट्टराई", "हिमिला यामी", "रवि लामिछाने", "राजेन्द्र लिङ्देन", "गगन थापा", "सागर ढकाल", "योगेश भट्टराई", "विश्वप्रकाश सुवेदी"];
var names_en = ["Pushpakamal Dahal", "KP Oli", "Sher Bahadur Deuba", "Madhab Kumar Nepal", "Jhalanath Khanal", "Baburam Bhattara", "Hisila Yami", "Rabi Lamichhane", "Ranjendra Lingden", "Gagan Thapa", "Sagar Dhakal", "Yogesh Bhattarai", "Bishwa Prakash Subedi"];
newData = data.provinces.map((p) => {
  p.districts.map((d) => {
    d.regions.map((r, i) => {
      let tempRand1 = [],
        tempRand2 = [];
      r.result = r.result.map((rs, i) => {
        let randName = Math.floor(Math.random() * names_np.length);
        while (tempRand1.includes(randName) && i > 0) {
          randName = Math.floor(Math.random() * names_np.length);
        }
        let randParty = Math.floor(Math.random() * 5);
        while (tempRand2.includes(randParty) && i > 0) {
          randParty = Math.floor(Math.random() * 5);
        }
        rs.party = randParty;
        rs.name_np = names_np[randName];
        rs.name_en = names_en[randName];
        rs.vote = Math.floor(Math.random() * 30000);
        tempRand1.push(randName);
        tempRand2.push(randParty);
        return rs;
      });
      if (i === 2) {
        r.elected = r.result.sort((a, b) => b.vote - a.vote)[0];
        r.declared = true;
      } else {
        r.elected = {};
        r.declared = false;
      }
      r.elected;
    });
    return d;
  });
  return p;
});

newData = {
  provinces: newData,
};

fs.writeFileSync(outFile, JSON.stringify(newData));
