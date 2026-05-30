// The module 'vscode' contains the VS Code extensibility API

// import { tmpdir } from 'os';

// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
// const fsextra = require('fs-extra');
const path = require('path');
const ProgShow = require('./prog_show');
const BanqueExoShow = require('./banque_exo_show');
const { registerProgrammeTreeCommands } = require('./commands/programmeTreeCommands');
const { registerBanqueTreeCommands } = require('./commands/banqueTreeCommands');
const { registerBanqueItemCommands } = require('./commands/banqueItemCommands');
// const GetTypeExo = BanqueExoShow.GetTypeExo;
// const pdfjsLib = require('pdfjs-dist');
// const pdfWriter = require('pdfwriter');

// set the boolean variables to change icon when uploading programme de colle
vscode.commands.executeCommand('setContext', 'static', true);

// AUXILIARY FUNCTIONS //

// find all subdirectories, WHATEVER THE DEPTH, within directory basePath, which are called dirName
// function findDirectories(basePath, dirName) {
//     let results = [];
//     const items = fs.readdirSync(basePath, { withFileTypes: true });

//     for (const item of items) {
//         if (item.isDirectory()) {
// 			var fullPath = basePath + item.name + '/';
//             // var fullPath = path.join(basePath, item.name);
// 			if (item.name.includes(dirName)) {
// 				results.push(fullPath);
// 			}
//             results = results.concat(findDirectories(fullPath, dirName));
	


//         }
//     }

//     return results;
// }

// AUXILIARY FUNCTIONS //

// find all subdirectories, WHATEVER THE DEPTH, within directory basePath that are called dirName
// function findDirectories(basePath, dirName) {
//     let results = [];
//     const items = fs.readdirSync(basePath, { withFileTypes: true });

//     for (const item of items) {
//         if (item.isDirectory()) {
// 			var fullPath = basePath + item.name + '/';
// 			if (item.name.includes(dirName)) {
// 				results.push(fullPath);
// 			}
//             results = results.concat(findDirectories(fullPath, dirName));
//         }
//     }

//     return results;
// }

// synchronous function to compile latex document
function compileLatex(filePath, outputDirectory = `${__dirname}/tmp`) {
	// define default recipe
	const recipe = `pdflatex -interaction=nonstopmode -shell-escape -output-directory ${outputDirectory}`;
	// compile the latex document synchronously
	child_process.execSync(`${recipe} ${filePath}`);
}

// function viewPdf(filePath, options = { viewColumn: vscode.ViewColumn.Two }) {
// 	// open the pdf file in vscode
// 	vscode.commands.executeCommand('vscode.open', vscode.Uri.file(filePath), options);
// }

// synchronous function to copy one pdf into several copies of itself 
function copyPdf(filePath, copies = 1) {
	for (let i = 0; i < copies; i++) {
		// copy filePath into filePath_copy_i.pdf
		fs.copyFileSync(filePath, `${filePath}_copy_${i}.pdf`);
	}
	child_process.execSync(`pdftk ${filePath}_copy_*.pdf cat output ${filePath}`);
	// remove auxiliary pdf files
	for (let i = 0; i < copies; i++) {
		fs.unlinkSync(`${filePath}_copy_${i}.pdf`);
	}
} 

// asynchronous function to find the flash drive
async function findFlashDrive() {
    try {
		const files = await fs.promises.readdir('/media/eb/');
		for (const name of files) {
			const fullPath = path.join('/media/eb/', name);
			const stats = await fs.promises.lstat(fullPath);
			if (stats.isDirectory()) {
				return fullPath;
			}
		}
		// }
    } catch (error) {
        console.error('Error reading /media/ directory:', error);
    }
    return undefined;
}


// Function to get the next Monday date for the programme de colle
// function getNextMonday() {
// 	const today = new Date();
// 	const nextMonday = new Date(today.getTime() + ((7 - today.getDay()) % 7 +1) * 24 * 60 * 60 * 1000);
// 	const year = nextMonday.getFullYear();
// 	const month = String(nextMonday.getMonth() + 1).padStart(2, '0');
// 	var day = String(nextMonday.getDate()).padStart(2, '0');
// 	if (day.startsWith('0')) {
// 		var daynumber = day.substring(1);
// 	}
// 	else {
// 		var daynumber = day;
// 	}
// 	const dayOfWeek = nextMonday.toLocaleDateString('fr', { weekday: 'long' });
// 	const monthName = nextMonday.toLocaleDateString('fr', { month: 'long' });
// 	return [`${year}_${month}_${day}`,`"${dayOfWeek} ${daynumber} ${monthName} ${year}"`];
// };

// ------------------------------ //

/**
 * @param {vscode.ExtensionContext} context
*/
function activate(context) {
	// Use the console to output diagnostic information (console.log) and errors (console.error)
	console.log('Congratulations, your extension "show-programme-colle" is now active!');

	// remove all files in /tmp directory
	// fs.readdir(__dirname + '/tmp', (err, files) => {
	// 	if (err) throw err;
	// 	for (const file of files) {
	// 		fs.unlink(path.join(__dirname + '/tmp', file), err => {
	// 			if (err) throw err;
	// 		});
	// 	}
	// });
	
	// get the user setting variables
	const collePath = vscode.workspace.getConfiguration('programme-colle').get('collePath');
	const styPath = vscode.workspace.getConfiguration('programme-colle').get('styPath');
	const pythonCommand = vscode.workspace.getConfiguration('programme-colle').get('pythonCommand');
	const programmeBalise = vscode.workspace.getConfiguration('programme-colle').get('programmeBalise');
	const exoenvi = vscode.workspace.getConfiguration('banque-exercices').get('exerciceEnvironment');
	const explorerCommand = vscode.workspace.getConfiguration('banque-exercices').get('explorerCommand');
	const cpgePath = vscode.workspace.getConfiguration('programme-colle').get('cpgePath');
	const mdPath = vscode.workspace.getConfiguration('programme-colle').get('mdPath');
	// const mathpixCommand = vscode.workspace.getConfiguration('mathpix-pdf').get('mpxCommand');
	// const texPath = vscode.workspace.getConfiguration('mathpix-pdf').get('texPath');
	// const texArchives = vscode.workspace.getConfiguration('mathpix-pdf').get('texArchives');
	
	
	// Banque item commands are now registered in ./commands/banqueItemCommands.js

	
	//  SUGGESTIONS commands
	let go = vscode.commands.registerCommand('suggestions.go', function () {
		// open an exercise listed in the file /tmp/exercices-sans-difficulte.txt

		// Read the contents of the file
		const exercice_liste = __dirname + '/tmp/exercices-sans-difficulte.txt';
		// let fileContent;
		var fileContent = fs.readFileSync(exercice_liste, 'utf8');
		// try {
		// } catch (error) {
		// 	if (error.code === 'ENOENT') {
		// 		// File does not exist, create it
		// 		fs.writeFileSync(exercice_liste, '', 'utf8');
		// 		fileContent = '';
		// 	} else {
		// 		// Other error occurred, handle it accordingly
		// 		console.error(error);
		// 	}
		// }

		// vscode.window.showInformationMessage('Ouverture de ' + exercice_liste);
		const lines = fileContent.split('\n');
		var [filePath, exo] = lines[0].split(':');
		var exo = exo.toString().trim();
		exo = `{${exo}}`;

		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.workspace.onDidOpenTextDocument(() => {});
		}

		// vscode.window.showInformationMessage('Ouverture de ' + filePath, exo);
		// open the latex document in vscode
		// if (filePath !== vscode.window.activeTextEditor.document.uri.fsPath) {
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(filePath));
			// Your code here
					// search for the exo in the file
		
		let document = editor.document;
		var text = document.getText();
		var position = text.indexOf(exo);
		if (position !== -1) {
			var startPosition = document.positionAt(position);
			var endPosition = document.positionAt(position + exo.length);
			var range = new vscode.Range(startPosition, endPosition);
			editor.selection = new vscode.Selection(range.start, range.end);
			editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
		} else {
			// vscode.window.showInformationMessage('String not found');
		}
		// refresh list of exercises without difficulty, does not work
		// new BanqueExoShow();
	}
	)

	// -----------------------------------
	// FLASH COMMANDS //
	// -----------------------------------

	let colle_qcours = vscode.commands.registerCommand('flash.colle_qcours', function () {
		// apply build_colle.py to latex document
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// get the file and folder paths
		const filePath = editor.document.fileName;
		const folderPath = path.dirname(filePath);

		// find file in folder that starts with " programme- " and ends with ".pdf"
		let programmeFile = fs.readdirSync(folderPath).find(file => file.startsWith("programme-") && file.endsWith(".pdf"));

		vscode.window.showInformationMessage('Fichier programme de colle trouvé : ' + programmeFile);
		// generate the questions de cours using build_colle.py
		vscode.window.showInformationMessage('Génération des questions de cours pour ' + filePath + '...');
		child_process.execSync(pythonCommand + ` ${__dirname}/scripts/build_colle.py ` + programmeFile + ' ' + filePath, { cwd: folderPath });

		// reload the LATEX document in the editor
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(filePath), { viewColumn: vscode.ViewColumn.One });

		// show success message
		vscode.window.showInformationMessage('Questions de cours générées avec succès.');
	})

	// commande pour créer markdown document associé à un fichier latex ouvert dans l'éditeur
	vscode.commands.registerCommand('flash.md', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// get the file path
		const filePath = editor.document.fileName;
		// apply compile-md.py to the file path to create the md file
		const mdname = child_process.execSync(pythonCommand + ` /home/eb/qftrules.github.io/compile-md.py ` + filePath).toString().trim();
		vscode.window.showInformationMessage('Markdown généré : ' + mdname);
		// open the md file in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(mdname), { viewColumn: vscode.ViewColumn.Two });
	});
	
	// PROGRAMME DE COLLE commands

	// commande pour téléverser le programme de colle sur le cahier de prépa depuis title view : programme de colle
	// let upload = vscode.commands.registerCommand('programme.upload', function () {

	// 	// change icon
	// 	vscode.commands.executeCommand('setContext', 'static', false);

	// 	const nextTuesdayDate = getNextMonday()[0];
	// 	const week = getNextMonday()[1];

	// 	let programme_colle_file = nextTuesdayDate + '_PC_Phy_colle.pdf';
	// 	child_process.execSync(pythonCommand + ' ' + __dirname + '/upload_programme_colle.py ' + collePath + ' ' + programme_colle_file + ' ' + week);
	// 	vscode.window.showInformationMessage(programme_colle_file  + ' téléversé avec succès');

	// 	// change icon
	// 	vscode.commands.executeCommand('setContext', 'static', true);
	// });

	// Programme tree commands are now registered in ./commands/programmeTreeCommands.js

	// commande pour compiler bilan-DS.sh à partir d'un fichier .ods ouvert dans l'éditeur
	let compile_bilan_DS = vscode.commands.registerCommand('flash.compile_bilan_DS', function () {
		// get the active text editor
		let editor = vscode.window.tabGroups.activeTabGroup.activeTab.input;
		if (!editor) {
			return;
		}
		// get the file path
		const ods = editor.uri.fsPath;
		// const ods = editor.document.fileName;
		//  show message
		vscode.window.showInformationMessage('Compilation du bilan de ' + ods + '...');
		// vscode.window.showInformationMessage('bash ' + __dirname + '/scripts/build-bilanDS.sh ' + ods + ' ' + __dirname);
		const bilanDS = child_process.execSync('bash ' + __dirname + '/scripts/build-bilanDS.sh ' + ods + ' ' + __dirname).toString();
		// child_process.execSync('bash ' + __dirname + '/scripts/build-bilanDS.sh ' + ods + ' ' + __dirname, (error, stdout, stderr) => {
		// 	if (error) {
		// 		// Display an error message if the bash program encounters an error
		// 		vscode.window.showErrorMessage(`Error: ${error.message} | ${stderr}`);
		// 		return;
		// 	}
			// Continue with the following lines of code
			// ...
		vscode.window.showInformationMessage(ods + ' compilé avec succès');
		// get first substring of ods before _ underscore
		// const bilanDS = ods.substring(0, ods.indexOf('_')) + '_bilanDS.pdf';
		// open file bilanDS.pdf in vscode on right panel
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(bilanDS), { viewColumn: vscode.ViewColumn.Two });
		// });
	});


	// commande pour compiler et téléverser le programme de colle depuis title view : programme de colle
	// let build = vscode.commands.registerCommand('programme.build', function () {
	// 	vscode.commands.executeCommand('programme.compile');
	// 	vscode.commands.executeCommand('programme.upload');
	// });

	const programme_colle = new ProgShow();
	registerProgrammeTreeCommands(context, {
		programmeBalise,
		collePath,
		styPath,
		pythonCommand,
		cpgePath,
		mdPath,
		programmeProvider: programme_colle,
	});

	let suggestions_refresh = vscode.commands.registerCommand('suggestions.refresh', () => {
		vscode.commands.executeCommand('banque.refresh');
	});

	// register provider once; subsequent refreshes update this instance
	vscode.window.registerTreeDataProvider('programme-colle', programme_colle);


	// command to send file in the editor to the flash drive
	let send = vscode.commands.registerCommand('flash.send', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		var filePath = editor.document.fileName;
		const pdfFilePath = filePath.replace(/\.[^/.]+$/, ".pdf");
		const pdfFilePath_soluce = filePath.replace(/\.[^/.]+$/, "_soluce.pdf");
		const pdfFilePath_soluce_only = filePath.replace(/\.[^/.]+$/, "_soluce_only.pdf");
		const pdfFilePath_bilan = filePath.substring(0, filePath.indexOf('_')) + '_bilan.pdf';
		const pdfFilePath_fiche = filePath.replace(/\.[^/.]+$/, "_fiche.pdf");

		// find any folder in /media/ that could match a USB flash drive - replaces variable "flashDrive" defined in settings.json
		findFlashDrive().then(flashDrive => {
			console.log('Flash Drive:', flashDrive);
			// find the print subdirectory in directory flashDrive

			// add / character if not present at the end of the string
			const printDirectory = path.join(flashDrive, 'print');
			// check if the print directory exists
			if (!fs.existsSync(printDirectory)) {
				// send error message
				vscode.window.showErrorMessage(`No print directory found in ${flashDrive}`);
				return;
			}

			// copy the file to the flash drive with the new file extension
			const fileName = path.basename(pdfFilePath);
			const destinationPath = path.join(printDirectory, fileName);
			fs.copyFileSync(pdfFilePath, destinationPath);
			// show information message
			vscode.window.showInformationMessage(`${fileName} copied to ${printDirectory}`);

			// check if the fiche colle exists
			if (fs.existsSync(pdfFilePath_fiche)) {
				// copy the fiche file to the flash drive with the new file extension
				const ficheFileName = path.basename(pdfFilePath_fiche);
				const ficheDestinationPath = path.join(printDirectory, ficheFileName);
				fs.copyFileSync(pdfFilePath_fiche, ficheDestinationPath);
				// show information message
				vscode.window.showInformationMessage(`${ficheFileName} copied to ${printDirectory}`);
			}

			// check if the soluce file exists
			if (fs.existsSync(pdfFilePath_soluce)) {
				// copy the soluce file to the flash drive with the new file extension
				const soluceFileName = path.basename(pdfFilePath_soluce);
				const soluceDestinationPath = path.join(printDirectory, soluceFileName);
				fs.copyFileSync(pdfFilePath_soluce, soluceDestinationPath);
				// show information message
				vscode.window.showInformationMessage(`${soluceFileName} copied to ${printDirectory}`);
			}
			
			// check if the soluce_only file exists
			if (fs.existsSync(pdfFilePath_soluce_only)) {
				// copy the soluce_only file to the flash drive with the new file extension
				const soluce_onlyFileName = path.basename(pdfFilePath_soluce_only);
				const soluce_onlyDestinationPath = path.join(printDirectory, soluce_onlyFileName);
				fs.copyFileSync(pdfFilePath_soluce_only, soluce_onlyDestinationPath);
				// show information message
				vscode.window.showInformationMessage(`${soluce_onlyFileName} copied to ${printDirectory}`);
			}

			// check if the bilan DS file exists
			if (fs.existsSync(pdfFilePath_bilan)) {
				// copy the bilan file to the flash drive with the new file extension
				const bilanFileName = path.basename(pdfFilePath_bilan);
				const bilanDestinationPath = path.join(printDirectory, bilanFileName);
				fs.copyFileSync(pdfFilePath_bilan, bilanDestinationPath);
				// show information message
				vscode.window.showInformationMessage(`${bilanFileName} copied to ${printDirectory}`);
			}
		});
	});

// -----------------------------------
// BANQUE D'EXERCICES COMMANDS //
// -----------------------------------

	// FUNCTIONS OF VIEW - TITLE //
	// Banque tree commands are now registered in ./commands/banqueTreeCommands.js
	registerBanqueTreeCommands(context);

	// Banque item commands are now registered in ./commands/banqueItemCommands.js
	registerBanqueItemCommands(context, { exoenvi, explorerCommand, styPath, programmeBalise, extensionPath: __dirname });

	// banque.compile and banque.reveal are now registered in ./commands/banqueItemCommands.js

	// COMMANDS AT LAUNCH //
	vscode.window.registerTreeDataProvider('banque-exercices', new BanqueExoShow())
	// update_graphics_path();

	// command to build a QCM for a given chapter
	vscode.commands.registerCommand('flash.test', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// get the file path
		const cours = editor.document.fileName;
		const coursDir = path.dirname(cours);
		// write the test file
		const template = __dirname + '/templates/source.tex';
		// make directory QCM if not existent 
		// if (!fs.existsSync(coursDir + '/QCM')) {
		// 	fs.mkdirSync(coursDir + '/QCM');
		// }
		//  get theme letter and chapter number
		var theme = coursDir.substring(0,coursDir.lastIndexOf('/'));
		var theme = theme.substring(theme.lastIndexOf('/')+2,theme.lastIndexOf('/')+3);
		var chapter =  coursDir.substring(coursDir.lastIndexOf('/')+2,coursDir.lastIndexOf('/')+3);
		// vscode.window.showInformationMessage(theme + '-' + chapter);
		// destination folder
		var destination = '/home/eb/MC-Projects/QCM-PC-' + theme + '-' + chapter;
		if (!fs.existsSync(destination)) {
			fs.mkdirSync(destination);}
		//  copy template file to another name in the same directory
		fs.cpSync('/home/eb/MC-Projects/QCM-PC', destination, { recursive: true });
		// destination file
		var destination = destination + '/source.tex';
		fs.copyFileSync(template, destination);
		
		
		// build the interro file
		// fs.writeFileSync(template, '\\input{devoir.sty}\n\\begin{document}\n\\EnteteInter{06/10/2022}{1}\n\\begin{quest}\n');
		child_process.execSync(pythonCommand + ` ${__dirname}/build_QCM.py ${cours} ${destination}`, (error, stdout, stderr) => {
			if (error) {
				console.error(`Error: ${error.message}`);
				return;
			}
			if (stderr) {
				console.error(`stderr: ${stderr}`);
				return;
			}
			console.log(`stdout: ${stdout}`);
		});
		
		fs.appendFileSync(destination, '\\AMCaddpagesto{1}\n\\end{copieexamen}\n\\end{document}');
		vscode.commands.executeCommand('flash.amc');
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(destination));

	});

	// command to compile using auto-multiple-choice
	let amc = vscode.commands.registerCommand('flash.amc', function () {
		// get the active text editor
		child_process.exec(`auto-multiple-choice`);
	});

	// command to build fiche colle
	let flash_fiche_colle = vscode.commands.registerCommand('flash.fiche_colle', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		// get the Colle date
		const nextTuesday = new Date();
		nextTuesday.setDate(nextTuesday.getDate() + ((2 + 7 - nextTuesday.getDay()) % 7));
		const nextNextTuesday = new Date(nextTuesday);
		nextNextTuesday.setDate(nextTuesday.getDate() + 7);

		const NextTuesday = nextTuesday.toLocaleDateString('fr-FR');
		const NextnextTuesday = nextNextTuesday.toLocaleDateString('fr-FR');

		// get the file path
		const colle_file = editor.document.fileName;
		const fiche_pdf = colle_file.replace('.tex', '_fiche.pdf');
		const fiche_latex = __dirname + '/templates/Fiche.tex';
		// get tmp path
		const tmp_tex = __dirname + '/tmp/Fiche_tmp_simple.tex';
		child_process.execSync(pythonCommand + ` ${__dirname}/scripts/build-fiche-colle.py ${colle_file} ${NextTuesday} ${NextnextTuesday} ${fiche_latex} ${tmp_tex}`);
		compileLatex(tmp_tex);
		// find \Count{#1} in the file and copy pdf files as many times as value of #1
		const tmp_pdf = tmp_tex.replace('.tex', '.pdf');
		const count = fs.readFileSync(colle_file).toString().match(/\\Count{(\d+)}/)[1];
		copyPdf(tmp_pdf, count);
		fs.renameSync(tmp_pdf, fiche_pdf);
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(fiche_pdf), { viewColumn: vscode.ViewColumn.Two });
		// get basename of fiche
		const basename = path.basename(fiche_pdf);
		vscode.window.showInformationMessage(`${basename} généré avec succès`);
	});

	// command to see the soluce version of tex file
	let flash_view_soluce = vscode.commands.registerCommand('flash.view_soluce', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// get the file path
		const latex = editor.document.fileName;
		// get the pdf soluce file name 
		const soluce = latex.replace('.tex', '_soluce.pdf');
		// open the soluce pdf in vscode in the right panel
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(soluce), { viewColumn: vscode.ViewColumn.Two });
	});

	// command to build soluce for latex file
	let flash_soluce = vscode.commands.registerCommand('flash.soluce', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// get the file path
		const latex = editor.document.fileName;
		// get current day as a string in yyyy-mm-dd format
		const today = new Date().toISOString().slice(0, 10);
		// copy file to file_soluce.tex
		const corrige = latex.replace('.tex', '_soluce.tex');
		// fs.copyFileSync(latex, corrige);
		// apply $HOME/Dropbox/.latex/Commands/build-soluce.py
		child_process.execSync(pythonCommand + ` ${__dirname}/build-soluce.py ${latex} ${today}`, () => {
		});
		// build using latex-workshop
		// child_process.execSync(`pdflatex ${corrige}`, () => {});
		// define magic comment for root file
		const latex_magic = `% !TEX root = ${corrige}\n`;
		// add latex_magic as first line of the file
		var editorText = editor.document.getText();
		if (editorText.includes(`% !TEX root `)) {
			editor.edit(editBuilder => {
				editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			}).then(() => {
				// run latex-workshop build command
				vscode.commands.executeCommand('latex-workshop.build').then(() => {
					// clean all auxiliary files
					// vscode.commands.executeCommand('latex-workshop.clean');
					// open the soluce pdf in vscode	
					vscode.commands.executeCommand('latex-workshop.tab');
					// remove latex command
					editor.edit(editBuilder => {
						editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
					});
					// remove all auxiliary files like .aux, .log, .out, .synctex.gz
					const files = ['.synctex.gz','.tex'];
					files.forEach(file => {
						const auxFile = corrige.replace('.tex', file);
						if (fs.existsSync(auxFile)) {
							fs.unlinkSync(auxFile);
						}
					});
					// save the file
					editor.document.save();
				});
			});
		} else {
			editor.edit(editBuilder => {
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			}).then(() => {
				// run latex-workshop build command
				vscode.commands.executeCommand('latex-workshop.build').then(() => {
					// clean all auxiliary files
					// vscode.commands.executeCommand('latex-workshop.clean');
					// open the soluce pdf in vscode	
					vscode.commands.executeCommand('latex-workshop.tab').then(() => {
						// remove latex command
						editor.edit(editBuilder => {
							editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
						});
						// remove all auxiliary files like .aux, .log, .out, .synctex.gz
						// const files = ['.synctex.gz','.tex'];
						const files = ['.tex'];
						files.forEach(file => {
							const auxFile = corrige.replace('.tex', file);
							if (fs.existsSync
							(auxFile)) {
								fs.unlinkSync(auxFile);
							}
						});
						// save the file
						editor.document.save();
					});
				});
			});
		}
	});

	// command to build soluce for latex file
	vscode.commands.registerCommand('flash.soluce_only', function () {
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// get the file path
		const latex = editor.document.fileName;
		// get current day as a string in yyyy-mm-dd format
		const today = new Date().toISOString().slice(0, 10);
		// copy file to file_soluce.tex
		const corrige = latex.replace('.tex', '_soluce_only.tex');
		// fs.copyFileSync(latex, corrige);
		// apply $HOME/Dropbox/.latex/Commands/build-soluce.py
		child_process.execSync(pythonCommand + ` ${__dirname}/build-soluce_only.py ${latex} ${today}`, () => {
		});
		// build using latex-workshop
		// child_process.execSync(`pdflatex ${corrige}`, () => {});
		// define magic comment for root file
		const latex_magic = `% !TEX root = ${corrige}\n`;
		// add latex_magic as first line of the file
		var editorText = editor.document.getText();
		if (editorText.includes(`% !TEX root `)) {
			editor.edit(editBuilder => {
				editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			}).then(() => {
				// run latex-workshop build command
				vscode.commands.executeCommand('latex-workshop.build').then(() => {
					// clean all auxiliary files
					// vscode.commands.executeCommand('latex-workshop.clean');
					// open the soluce pdf in vscode	
					vscode.commands.executeCommand('latex-workshop.tab');
					// remove latex command
					editor.edit(editBuilder => {
						editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
					});
					// remove all auxiliary files like .aux, .log, .out, .synctex.gz
					const files = ['.synctex.gz','.tex'];
					files.forEach(file => {
						const auxFile = corrige.replace('.tex', file);
						if (fs.existsSync(auxFile)) {
							fs.unlinkSync(auxFile);
						}
					});
					// save the file
					editor.document.save();
				});
			});
		} else {
			editor.edit(editBuilder => {
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			}).then(() => {
				// run latex-workshop build command
				vscode.commands.executeCommand('latex-workshop.build').then(() => {
					// clean all auxiliary files
					// vscode.commands.executeCommand('latex-workshop.clean');
					// open the soluce pdf in vscode	
					vscode.commands.executeCommand('latex-workshop.tab').then(() => {
						// remove latex command
						editor.edit(editBuilder => {
							editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
						});
						// remove all auxiliary files like .aux, .log, .out, .synctex.gz
						// const files = ['.synctex.gz','.tex'];
						const files = ['.tex'];
						files.forEach(file => {
							const auxFile = corrige.replace('.tex', file);
							if (fs.existsSync
							(auxFile)) {
								fs.unlinkSync(auxFile);
							}
						});
						// save the file
						editor.document.save();
					});
				});
			});
		}
	});
	
	// now push these functions to the context
	context.subscriptions.push(go);
	// context.subscriptions.push(fetch);
	// context.subscriptions.push(upload);
	// context.subscriptions.push(build);
	context.subscriptions.push(send);
	context.subscriptions.push(test);
	context.subscriptions.push(amc);
	context.subscriptions.push(suggestions_refresh);
	context.subscriptions.push(compile_bilan_DS);
	context.subscriptions.push(flash_soluce);
	// context.subscriptions.push(flash_amc);
	context.subscriptions.push(flash_fiche_colle);
	context.subscriptions.push(flash_view_soluce);
	context.subscriptions.push(colle_qcours);
	// context.subscriptions.push(convert);
	// context.subscriptions.push(flash_soluce_only);

	// call here all commands necessary at launch
	vscode.window.registerTreeDataProvider('banque-exercices', new BanqueExoShow());
	programme_colle.refresh();

}

// This method is called when your extension is deactivated
function deactivate() {}

	
// export modules
module.exports = {
	activate,
	deactivate
}


// WORK IN PROGRESS //

	// // command in the explorer context menu to convert pdf to latex	
	// let convert = vscode.commands.registerCommand('mathpix-pdf.convert', function (uri) {
	// 	// The code you place here will be executed every time your command is executed
	// 	const fileName = path.basename(uri.toString());
	// 	const fileDirectory = path.dirname(uri.toString().replace("file://", ""));
		
	// 	// Prompt the user for the pages range
	// 	vscode.window.showInputBox({ placeHolder: 'Enter the pages range (e.g. 1, 1-5, or 2-end)' }).then(range => {
	// 		if (range) {
	// 			vscode.window.showQuickPick(texArchives, { placeHolder: 'Enter the tex archive to store the exercise (e.g. dynapoint.tex)' }).then(texFile => {
	// 				if (texFile) {
	// 					// Run the bash program on the active file
	// 					// vscode.window.showInformationMessage(`Converting pages ${range} of ${fileName} to latex...`);
	// 					// decode the string
	// 					const pageRange = range.split('-');
	// 					const startPage = pageRange[0];
	// 					const endPage = pageRange[1] || 'end';

	// 					// Read the PDF file using a library like pdfjs-dist

	// 					const fileData = fs.readFileSync(`${fileDirectory}/${fileName}`);
	// 					const loadingTask = pdfjsLib.getDocument(fileData);

	// 					loadingTask.promise.then((pdf) => {
	// 						const totalPages = pdf.numPages;

	// 						// Calculate the actual page numbers based on the range
	// 						const startPageNumber = parseInt(startPage);
	// 						const endPageNumber = endPage === 'end' ? totalPages : parseInt(endPage);

	// 						// Validate the page numbers
	// 						if (startPageNumber <= 0 || startPageNumber > totalPages || endPageNumber <= 0 || endPageNumber > totalPages || startPageNumber > endPageNumber) {
	// 							vscode.window.showErrorMessage('Invalid page range');
	// 							return;
	// 						}

	// 						// Extract the pages using pdfjs-dist
	// 						const pagesToExtract = [];
	// 						for (let i = startPageNumber; i <= endPageNumber; i++) {
	// 							pagesToExtract.push(i);
	// 						}

	// 						const writer = new pdfWriter.PDFWriter();

	// 						const outputFile = `${fileDirectory}/file_to_convert.pdf`;
	// 						const outputStream = fs.createWriteStream(outputFile);

	// 						pdf.copyPagesInto(pagesToExtract, writer);
	// 						writer.pipe(outputStream);
	// 						writer.end();

	// 						vscode.window.showInformationMessage(`Pages ${startPage}-${endPage} extracted successfully`);
	// 					}).catch((error) => {
	// 						vscode.window.showErrorMessage(`Error: ${error.message}`);
	// 					});
	// 					// child_process.execSync(decodeURI(`pdftk ${fileDirectory}/${fileName} cat ${range} output "${fileDirectory}/file_to_convert.pdf"`));
	// 					// const commande = decodeURI(__dirname + `/mathpix_pdf_to_latex.sh ${fileName} ${fileDirectory} "${texPath}${texFile}" ${range}`, 'utf-8'); 
	// 					// vscode.window.showInformationMessage(commande);
	// 					// child_process.execSync(commande, (error, stdout, stderr) => {
	// 					// 	if (error) {
	// 					// 		// Display an error message if the bash program encounters an error
	// 					// 		vscode.window.showErrorMessage(`Error: ${error.message} | ${stderr}`);
	// 					// 		return;
	// 					// 	}
	// 					// });
	// 					// child_process.exec(decodeURI(mathpixCommand + ` convert ${fileDirectory}/file_to_convert.pdf ${fileDirectory}/file_to_convert.tex`), (error, stderr) => {
	// 					// 	if (error) {
	// 					// 		// Display an error message if the bash program encounters an error
	// 					// 		vscode.window.showErrorMessage(`Error: ${error.message} | ${stderr}`);
	// 					// 		return;
	// 					// 	}
	// 					// });
	// 				}
	// 			});
	// 		}
	// 	});
	// });