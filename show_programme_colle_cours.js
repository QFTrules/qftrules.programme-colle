exports.show_programme_colle = function show_programme_colle() {
  // dates of the upcoming week
  const DAYCHECK = new Date().toISOString().split('T')[0];
  const numdaycheck = new Date(DAYCHECK).getDay();
  const sumMon = 8 - numdaycheck;
  const sumFri = 13 - numdaycheck;
  const NextMonday = new Date(new Date(DAYCHECK).getTime() + sumMon * 24 * 60 * 60 * 1000).toLocaleDateString('en-GB');
  const NextFriday = new Date(new Date(DAYCHECK).getTime() + sumFri * 24 * 60 * 60 * 1000).toLocaleDateString('en-GB');
  console.log(`Programme de colle du ${NextMonday} au ${NextFriday} :`);

  // change directory
  const fs = require('fs');
  const path = require('path');
  const directory = path.join(process.env.HOME, 'Dropbox/.latex/Commands');
  fs.readdir(directory, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      return;
    }
    // const ProgColle = "ProgrammeColle.tex";
    const list_cours = [];
    const list_TD = [];
    const list_DM = [];
    const list_DS = [];
    const list_TP = [];

    files.forEach((file) => {
      const filePath = path.join(directory, file);
      if (fs.statSync(filePath).isFile()) {
        if (file.endsWith('.tex') && !file.includes('TD') && !file.includes('Fig') && !file.includes('Doc')) {
          list_cours.push(filePath);
        } else if (file.includes('TD') && file.endsWith('.tex')) {
          list_TD.push(filePath);
        } else if (file.includes('DM') && file.endsWith('.tex')) {
          list_DM.push(filePath);
        } else if (file.includes('DS') && file.endsWith('.tex')) {
          list_DS.push(filePath);
        } else if (file.endsWith('.tex')) {
          list_TP.push(filePath);
        }
      }
    });

    // fetch program in all lecture files
    console.log("    Cours :");
    list_cours.forEach((filePath) => {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      if (fileContent.includes("\\ProgrammeColle")) {
        // const simple_fichier = path.basename(filePath, '.tex');
        console.log(`${filePath},`);
      }
    });
  });
}
