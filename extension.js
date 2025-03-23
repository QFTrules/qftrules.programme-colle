// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
// const fsextra = require('fs-extra');
const path = require('path');
const ProgShow = require('./prog_show');
const BanqueExoShow = require('./banque_exo_show');
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


// insert the TEX root line at the beginning of the file
function insertLatexMagic(editor, rootFile) {
	// get text of the active editor
	const editorText = editor.document.getText();
	// define latex magic line
	const latex_magic = `% !TEX root = ${rootFile}.tex`;
	// add this line if not present at the beginning of the file
	if (editorText.includes(`% !TEX root `)) {
		editor.edit(editBuilder => {
			// get line number that contains the magic line
			const lineIndex = editorText.indexOf(latex_magic);
			const line = editor.document.lineAt(editor.document.positionAt(lineIndex).line);
			// delete the line
			editBuilder.delete(line.range);
			// insert the magic line at the beginning of the file
			// editBuilder.insert(new vscode.Position(0, 0), latex_magic);
		}).then(() => {
			editor.edit(editBuilder => {
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			});
		}
		);
	}  else {
		editor.edit(editBuilder => {
			editBuilder.insert(new vscode.Position(0, 0), latex_magic);
		});
	}
}

// Function to get the next Monday date for the programme de colle
function getNextMonday() {
	const today = new Date();
	const nextMonday = new Date(today.getTime() + ((7 - today.getDay()) % 7 +1) * 24 * 60 * 60 * 1000);
	const year = nextMonday.getFullYear();
	const month = String(nextMonday.getMonth() + 1).padStart(2, '0');
	var day = String(nextMonday.getDate()).padStart(2, '0');
	if (day.startsWith('0')) {
		var daynumber = day.substring(1);
	}
	else {
		var daynumber = day;
	}
	const dayOfWeek = nextMonday.toLocaleDateString('fr', { weekday: 'long' });
	const monthName = nextMonday.toLocaleDateString('fr', { month: 'long' });
	return [`${year}_${month}_${day}`,`"${dayOfWeek} ${daynumber} ${monthName} ${year}"`];
};

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
	// const mathpixCommand = vscode.workspace.getConfiguration('mathpix-pdf').get('mpxCommand');
	// const texPath = vscode.workspace.getConfiguration('mathpix-pdf').get('texPath');
	// const texArchives = vscode.workspace.getConfiguration('mathpix-pdf').get('texArchives');
	
	
	// BANQUE EXERCICES commands
	let copy = vscode.commands.registerCommand('banque.copy', function (document) {
		// Copy the document path to the clipboard
		let editor = vscode.window.activeTextEditor;
		if (editor) {
			// let document = editor.document;
			let position = editor.selection.active;
			// get name of file opened in editor
			const fileName = path.basename(editor.document.fileName);
			// if TD in fileName
			if (fileName.includes('TD') || fileName.includes('DS') || fileName.includes('DM')) {
				editor.edit(editBuilder => {
					editBuilder.insert(position, '\\Ex{' + document.label.replace(/"/g, '') + '}\n');
				});
			} else {
				if (fileName.includes('Colle')) {			
					editor.edit(editBuilder => {
						editBuilder.insert(position, document.label.replace(/"/g, ''));
					});
				} else {
					editor.edit(editBuilder => {
						editBuilder.insert(position, document.label.replace(/"/g, ''));
					});
				}
			}
		}
		}
	)

	// copy the latex file and use it as a source in an exercise latex document (TD, ...)
	let source = vscode.commands.registerCommand('banque.source', function (document) {
		// open the latex document in vscode
		let editor = vscode.window.activeTextEditor;
		if (editor) {
			// let document = editor.document;
			let position = editor.selection.active;
			editor.edit(editBuilder => {
				editBuilder.insert(position, '\\Source{' + path.basename(document.filePath) + '}\n');
			});
		}
	})

	// copy the latex file and use it as a source in an exercise latex document (TD, ...)
	let open = vscode.commands.registerCommand('banque.open', function (document) {
		// open the latex document in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath));
	})

	// fetch a string in a latex file, like exercise name of balise
	vscode.commands.registerCommand('banque.fetch', function (doc) {
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(doc.filePath), { viewColumn: vscode.ViewColumn.One }).then(() => {
			// Get the active text editor and string to search
			var editor = vscode.window.activeTextEditor;
			if (!editor) {
				return;
			}

			// determine the string to according to banque d'exercices or programme colle call
			if (doc.contextValue === 'latex') {
				var searchString = programmeBalise;
			} else {
				var searchString = '{' + doc.label + '}';
			}

			// first occurrence of string to search in the document
			var searchString = '{' + doc.label + '}';
			let document = editor.document;
			var text = document.getText();
			var position = text.indexOf(searchString);
			var startPosition = document.positionAt(position);
			var endPosition = document.positionAt(position + searchString.length);
			
			// check that the string \begin{exo} is also at the beginning of the line
			var line = document.lineAt(startPosition.line).text;
			while (!line.includes('{exo}')) {
					// look for next occurrence of searchString
					position = text.indexOf(searchString, position + 1);
					startPosition = document.positionAt(position);
					endPosition = document.positionAt(position + searchString.length);
					range = new vscode.Range(startPosition, endPosition);
					line = document.lineAt(startPosition.line).text;
				}
				
			// select the range and reveal it in the editor
			var range = new vscode.Range(startPosition, endPosition);
			editor.selection = new vscode.Selection(range.start, range.end);
			editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
		});
	})

	// fetch a string in a latex file, like exercise name of balise
	let fetch = vscode.commands.registerCommand('banque.fetch', function (doc) {
		// open document in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(doc.filePath), { viewColumn: vscode.ViewColumn.One });

		// Get the active text editor and string to search
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		

		let document = editor.document;
        var text = document.getText();
        var position = text.indexOf(searchString);

        if (position !== -1) {
            var startPosition = document.positionAt(position);
            var endPosition = document.positionAt(position + searchString.length);
            var range = new vscode.Range(startPosition, endPosition);
            editor.selection = new vscode.Selection(range.start, range.end);
			editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
        } else {
            // vscode.window.showInformationMessage('Exercice ou balise non trouvée.');
        }
	})

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

	// PROGRAMME DE COLLE commands

	// commande pour téléverser le programme de colle sur le cahier de prépa depuis title view : programme de colle
	let upload = vscode.commands.registerCommand('programme.upload', function () {

		// change icon
		vscode.commands.executeCommand('setContext', 'static', false);
		

		const nextTuesdayDate = getNextMonday()[0];
		const week = getNextMonday()[1];

		// console.log(nextTuesdayDate);
		let programme_colle_file = nextTuesdayDate + '_PC_Phy_colle.pdf';
		// vscode.window.showInformationMessage(pythonCommand + ' ' + __dirname + '/upload_programme_colle.py ' + collePath + ' ' + programme_colle_file + ' ' + week);
		child_process.execSync(pythonCommand + ' ' + __dirname + '/upload_programme_colle.py ' + collePath + ' ' + programme_colle_file + ' ' + week);
		// console.log(output);
		// vscode.window.showInformationMessage(output);
		vscode.window.showInformationMessage(programme_colle_file  + ' téléversé avec succès');

		// change icon
		vscode.commands.executeCommand('setContext', 'static', true);
	});

	// commande pour afficher pdf affiché dans le programme de colle
	let programme_pdf = vscode.commands.registerCommand('programme.pdf', function (document) {
		// define pdf file associated to latex document
		const pdfFile = document.filePath.replace(/\.[^/.]+$/, ".pdf");
		// open the pdf file in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(pdfFile), { viewColumn: vscode.ViewColumn.Two });
	});

	// commande pour enlever une balise de programme de colle dans un fichier latex
	let remove = vscode.commands.registerCommand('programme.remove', function (document) {
		const text = fs.readFileSync(document.filePath, 'utf8');
		const updatedText = text.replace(programmeBalise, '');
		fs.writeFileSync(document.filePath, updatedText, 'utf8');
	});

	// commande pour ajouter un fichier latex dans le type de documents
	// let add = vscode.commands.registerCommand('programme.add', function (typePath) {
	// 	// get the list of latex files in the folder "type"
	// 	const latex_files = child_process.execSync('find ' + typePath + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n').pop();
	// 	// find 
	// });


	// commande pour téléverser le programme de colle sur le cahier de prépa depuis title view : programme de colle
	let uploading = vscode.commands.registerCommand('programme.uploading', function () {
		// empty function to change the icon when programme de colle uploading
	});

	// commande pour compiler le programme de colle depuis title view : programme de colle
	let compile = vscode.commands.registerCommand('programme.compile', function () {
		const programme_colle_file = child_process.execSync('bash ' + __dirname + '/build_programme_colle.sh ' + collePath + ' ' + styPath + ' ' + pythonCommand + ' ' + __dirname).toString();
		vscode.window.showInformationMessage(programme_colle_file  + ' compilé avec succès', { timeout: 1 });
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(path.join(collePath.trim(),programme_colle_file.trim())), { viewColumn: vscode.ViewColumn.Two });
	});

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
	let build = vscode.commands.registerCommand('programme.build', function () {
		vscode.commands.executeCommand('programme.compile');
		vscode.commands.executeCommand('programme.upload');
	});

	// register data providers
	// var programme_colle = new ProgShow();
	// const banque_exercices = new BanqueExoShow();
	// vscode.window.registerTreeDataProvider('programme-colle', programme_colle);
	// vscode.window.registerTreeDataProvider('banque-exercices', banque_exercices);

	// commands to refresh the data providers
	let programme_refresh = vscode.commands.registerCommand('programme.refresh', () => {
		const programme_colle = new ProgShow();
		vscode.window.registerTreeDataProvider('programme-colle', programme_colle);
	});

	// refresh banque view
	vscode.commands.registerCommand('banque.refresh', () => {
		const banque_exercices = new BanqueExoShow();
		vscode.window.registerTreeDataProvider('banque-exercices', banque_exercices);
	});
	
	let suggestions_refresh = vscode.commands.registerCommand('suggestions.refresh', () => {
		vscode.commands.executeCommand('banque.refresh');
	});

	// generate the tree data at extension startup
	vscode.commands.executeCommand('programme.refresh');
	vscode.commands.executeCommand('banque.refresh');

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

	// command to send file in the editor to the flash drive
	let send = vscode.commands.registerCommand('flash.send', function () {
		// get the active text editor
		// vscode.window.showInformationMessage(`copié sur la clé USB`);
		let editor = vscode.window.activeTextEditor;
		// get the active text editor

		// check if an editor is active
		// if (editor) {
		// 	// get the file path of the active document
		// 	const filePath = editor.document.fileName;
		// 	vscode.window.showInformationMessage(`Current PDF file: ${filePath}`);
		// } else {
		// 	vscode.window.showErrorMessage('No active editor found');
		// }
		// if (!editor) {
		// 	return;
		// }
		// if doc is defined, use it as the document
		// if (doc) {
			// get the file path of the active document
			// var filePath = doc.filePath;
		// } else {
			// get the file path of the active document
		var filePath = editor.document.fileName;
		// }

		// if doc is pdf, then send only this document to the flash drive
		// if (filePath.endsWith('.pdf')) {
		// 	// find any folder in /media/ that could match a USB flash drive - replaces variable "flashDrive" defined in settings.json
		// 	findFlashDrive().then(flashDrive => {
		// 		console.log('Flash Drive:', flashDrive);
		// 		// add / character if not present at the end of the string
		// 		const printDirectory = path.join(flashDrive, 'print');
		// 		// check if the print directory exists
		// 		if (!fs.existsSync(printDirectory)) {
		// 			// send error message
		// 			vscode.window.showErrorMessage(`No print directory found in ${flashDrive}`);
		// 			return;
		// 		}
		// 		// copy the file to the flash drive with the new file extension
		// 		const fileName = path.basename(filePath);
		// 		const destinationPath = path.join(printDirectory, fileName);
		// 		fs.copyFileSync(filePath, destinationPath);
		// 		// show information message
		// 		vscode.window.showInformationMessage(`${fileName} copied to ${printDirectory}`);
		// 	});
		// 	return;
		// }
		// get the file path
		// const filePath = editor.document.fileName;
		// change the file extension to .pdf
		const pdfFilePath = filePath.replace(/\.[^/.]+$/, ".pdf");
		const pdfFilePath_soluce = filePath.replace(/\.[^/.]+$/, "_soluce.pdf");
		const pdfFilePath_bilan = filePath.substring(0, filePath.indexOf('_')) + '_bilan.pdf';
		const pdfFilePath_fiche = filePath.replace(/\.[^/.]+$/, "_fiche.pdf");

		// find any folder in /media/ that could match a USB flash drive - replaces variable "flashDrive" defined in settings.json
		// var flashDrive = fs.readdirSync('/media/').map(name => path.join('/media/', name)).find(f => fs.lstatSync(f).isDirectory());
		// var flashDrive = child_process.execSync('find /media/ -mindepth 2 -maxdepth 2 -type d').toString().split('\n').pop();
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
		// vscode.window.showInformationMessage(flashDrive);

		// check if the destination path is a directory
		// if (fs.existsSync(flashDrive) && fs.lstatSync(flashDrive).isDirectory()) {
		// 	// copy the file to the flash drive with the new file extension
		// 	const fileName = path.basename(pdfFilePath);
		// 	const destinationPath = path.join(flashDrive, fileName);
		// 	fs.copyFileSync(pdfFilePath, destinationPath);
		// 	// show information message
		// 	vscode.window.showInformationMessage(`${fileName} copied to ${flashDrive}`);
		// 	// check if the soluce file exists
		// 	if (fs.existsSync(pdfFilePath_soluce)) {
		// 		// copy the soluce file to the flash drive with the new file extension
		// 		const soluceFileName = path.basename(pdfFilePath_soluce);
		// 		const soluceDestinationPath = path.join(flashDrive, soluceFileName);
		// 		fs.copyFileSync(pdfFilePath_soluce, soluceDestinationPath);
		// 		// show information message
		// 		vscode.window.showInformationMessage(`${soluceFileName} copied to ${flashDrive}`);
		// 	}
		// 	if (fs.existsSync(pdfFilePath_bilan)) {
		// 		// copy the bilan file to the flash drive with the new file extension
		// 		const bilanFileName = path.basename(pdfFilePath_bilan);
		// 		const bilanDestinationPath = path.join(flashDrive, bilanFileName);
		// 		fs.copyFileSync(pdfFilePath_bilan, bilanDestinationPath);
		// 		// show information message
		// 		vscode.window.showInformationMessage(`${bilanFileName} copied to ${flashDrive}`);
		// 	}
		// } else {
		// 	vscode.window.showErrorMessage('Invalid destination path');
		// }
	});

	// command to compile an exercise separately
	let compile_exercise = vscode.commands.registerCommand('banque.compile', function (document) {
		
		// vscode.window.showInformationMessage(document.filePath);
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		
		// string to search in the document
		const searchString = '\\begin{' + exoenvi +'}';

		// check if command called from the explorer context menu or from the editor (document undefined)
		if (document === undefined) {
			// declare the cursorPosition variable
			const cursorPosition = editor.selection.active;
			// find the first line before the cursor position that contains the string '\begin{exo}'
			let lineNumber = cursorPosition.line - 1;
			let lineText = editor.document.lineAt(lineNumber).text;
			while (lineNumber >= 0 && !lineText.includes(searchString)) {
				lineNumber--;
				lineText = editor.document.lineAt(lineNumber).text;
			}
			// get second { character in line
			const start = lineText.indexOf('{', lineText.indexOf('{') + 1) + 1;
			// get last } caracter in line in case {} characters are present in exo title
			const end = lineText.lastIndexOf('}');
			var exo = lineText.substring(start, end);
			var FilePath = editor.document.fileName;
			var SourceFile = path.basename(FilePath);
		} else {
			var exo = document.label.replace(/"/g, '');
			var FilePath = document.filePath;
			var SourceFile = path.basename(FilePath);
			// vscode.window.showInformationMessage(exo, document.filePath);
			// vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath)).then(() => {
			// 	// just pass
			// }
			// );
		}

		// name of temporary latex exercise file
		const exercice_name = 'Exercice'
		const exercice = __dirname + `/tmp/${exercice_name}`;
		// insert the TEX root line at the beginning of the file
		insertLatexMagic(editor, exercice);
		// create the exercise latex file
		const template = `%&Exercice\n%\\input{TDappli.sty}\n%\\Soluce\n% \\endofdump\n\\begin{document}\n\\Source{${SourceFile}}\n\\Ex{${exo}}\n\\end{document}`;
		fs.writeFileSync(exercice + '.tex', template);
		// compile and open the exercise
		vscode.commands.executeCommand('latex-workshop.build', {rootFile:FilePath, recipe:'pdflatex'}).then(() => {
			// message to show that the exercise has been compiled
			vscode.window.showInformationMessage(`Exercice « ${exo} » compilé avec succès.`);
			// open tab
			vscode.commands.executeCommand('latex-workshop.tab');
		});
	});

	// command to reveal an exercise in tree view
	let reveal_exercise = vscode.commands.registerCommand('banque.reveal', function () {
		
		// vscode.window.showInformationMessage(document.filePath);
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
	
		// vscode.window.showInformationMessage(folderName, fileName);

		// get label of exercise from current mouse position
		const cursorPosition = editor.selection.active;
		const editorText = editor.document.getText();
		// find the first line before the cursor position that contains the string '\begin{exo}'
		let lineNumber = cursorPosition.line;
		let lineText = editor.document.lineAt(lineNumber).text;
		
		// get document filename and folder name 
		if (lineText.includes('begin{Exocolle}') || editorText.includes('\\Source')) { // Source
			// exo
			var startexo = lineText.indexOf('{', lineText.indexOf('{') + 1) + 1;
			var endexo = lineText.lastIndexOf('}');
			var exo = lineText.substring(startexo, endexo);
			// fileName
			const sourceIndex = editorText.indexOf('\\Source{');
			var start = sourceIndex + ('\\Source{').length;
			var end = editorText.indexOf('.tex}', start);
			var fileName = editorText.substring(start, end);
			var folderName = 'undefined';
		}
		else { // Source en argument de \Ex[]{}
			// exo 
			var startexo = lineText.indexOf('{') + 1;
			var endexo = lineText.lastIndexOf('}');
			var exo = lineText.substring(startexo, endexo);
			// fileName
			var start = lineText.indexOf('[') +1;
			var end = lineText.indexOf(']');
			var fileName = lineText.substring(start, end);
			var folderName = 'undefined';
		}
		// vscode.window.showInformationMessage(fileName, folderName, exo);
		// hihglight the exercise in the editor
		vscode.commands.executeCommand('extension.selectCurlyBrackets', {label: exo});

		const banque_exercices = new BanqueExoShow();
		const TreeView = vscode.window.createTreeView('banque-exercices', { treeDataProvider: banque_exercices });
		const item = banque_exercices.getTreeItemByLabel(folderName,fileName,exo);
		// vscode.window.showInformationMessage(item.label);
		TreeView.reveal(item, {focus: true, select: true, expand: true});
	});

	// command to build a QCM for a given chapter
	let test = vscode.commands.registerCommand('flash.test', function () {
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
		child_process.execSync(`python3 ${__dirname}/build_QCM.py ${cours} ${destination}`, (error, stdout, stderr) => {
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
		// open the test file in vscode
		// const outdir = vscode.workspace.getConfiguration('latex-workshop').get('latex.outDir');
		// vscode.workspace.getConfiguration('latex-workshop').update('latex.outDir', __dirname + '/tmp');
		// vscode.workspace.openTextDocument(fichier).then((document) => {
			// vscode.window.showTextDocument(document);
			// compile the test file
			//  open the file QCM.tex in vscode
		// vscode.window.showInformationMessage(`auto-multiple-choice prepare --mode=s ${destination}`);
		// child_process.execSync(`auto-multiple-choice prepare --mode=s ${destination}`, { stdio: 'ignore' });
		vscode.commands.executeCommand('flash.amc');
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(destination));

		// copy tex file to local folder
		// const folder = path.dirname(cours);
		// // get basename of cours
		// const coursName = path.basename(cours); 
		// const destination_save = folder + '/QCM_' + coursName;
		// fs.copyFileSync(destination, destination_save);
		// now execute amc command
		// vscode.commands.executeCommand('flash.amc', destination);
	});

	// command to compile using auto-multiple-choice
	let amc = vscode.commands.registerCommand('flash.amc', function () {
		// get the active text editor
		child_process.exec(`auto-multiple-choice`);
		// let editor = vscode.window.activeTextEditor;
		// if (!editor) {
		// 	return;
		// }
		// // get destination file if undefined
		// if (destination === undefined) {
		// 	var destination = '/' + editor.document.fileName;
		// } else {
		// 	var destination = String(destination).replace("file://", "");
		// }
		// // deal with [ and ] characters in destination path
		// destination = destination.replace('%5B', '[').replace('%5D', ']');
		// destination = destination.replace('%5B', '[').replace('%5D', ']');
		// vscode.window.showInformationMessage(destination);
		// try {
		// 	child_process.execSync(`auto-multiple-choice prepare --mode=s ${destination}`, { stdio: 'ignore' });
		// } catch (error) {
		// 	// Handle the error silently
		// 	vscode.window.showErrorMessage(`Error: ${error.message}`);
		// }
		// // open file sujet.pdf on vscode on right panel o
		// vscode.commands.executeCommand('vscode.open', vscode.Uri.file(destination.replace('.tex','_filtered-sujet.pdf') )
		// , { viewColumn: vscode.ViewColumn.Two });
	});

	// // command to compile using auto-multiple-choice
	// let amc = vscode.commands.registerCommand('flash.amc', function (destination) {
	// 	// get the active text editor
	// 	let editor = vscode.window.activeTextEditor;
	// 	if (!editor) {
	// 		return;
	// 	}
	// 	// get destination file if undefined
	// 	if (destination === undefined) {
	// 		var destination = '/' + editor.document.fileName;
	// 	} else {
	// 		var destination = String(destination).replace("file://", "");
	// 	}
	// 	// deal with [ and ] characters in destination path
	// 	destination = destination.replace('%5B', '[').replace('%5D', ']');
	// 	destination = destination.replace('%5B', '[').replace('%5D', ']');
	// 	vscode.window.showInformationMessage(destination);
	// 	try {
	// 		child_process.execSync(`auto-multiple-choice prepare --mode=s ${destination}`, { stdio: 'ignore' });
	// 	} catch (error) {
	// 		// Handle the error silently
	// 		vscode.window.showErrorMessage(`Error: ${error.message}`);
	// 	}
	// 	// open file sujet.pdf on vscode on right panel o
	// 	vscode.commands.executeCommand('vscode.open', vscode.Uri.file(destination.replace('.tex','_filtered-sujet.pdf') )
	// 	, { viewColumn: vscode.ViewColumn.Two });
	// });

	// command to apply the bash script 

	// command to build fiche colle
	let fiche_colle = vscode.commands.registerCommand('flash.fiche_colle', function () {
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

		// vscode.window.showInformationMessage(`Next Tuesday: ${NextTuesday}`);
		// vscode.window.showInformationMessage(`Next next Tuesday: ${NextnextTuesday}`);

		// get the file path
		const colle_file = editor.document.fileName;
		const fiche_pdf = colle_file.replace('.tex', '_fiche.pdf');
		// get directory
		// const fileDirname = path.dirname(colle_file);
		// get basename
		// const fileBasename = path.basename(latex);
		// execute the bash script
		// get the fiche.tex path 
		const fiche_latex = __dirname + '/templates/Fiche.tex';
		// get tmp path
		const tmp_tex = __dirname + '/tmp/Fiche_tmp_simple.tex';
		child_process.execSync(`python ${__dirname}/scripts/build-fiche-colle.py ${colle_file} ${NextTuesday} ${NextnextTuesday} ${fiche_latex} ${tmp_tex}`);
		// vscode.commands.executeCommand('latex-workshop.build', {rootFile:tmp_tex}).then(() => {
		// get first recipe listed in the latex settings
		// var recipe = vscode.workspace.getConfiguration('latex-workshop').get('latex.tools')[0].args.toString();
		// replace substring %DOC% by tmp_tex
		// var recipe = recipe.replace('%DOC%', tmp_tex);
		// var recipe = `pdflatex -interaction=nonstopmode -shell-escape -output-directory ${__dirname}/tmp`;
		// vscode.window.showInformationMessage(fiche_pdf);
		// child_process.execSync(`latexmk ${recipe} -output-directory=${__dirname}/tmp`, () => { 
		compileLatex(tmp_tex);
		// find \Count{#1} in the file and copy pdf files as many times as value of #1
		const tmp_pdf = tmp_tex.replace('.tex', '.pdf');
		const count = fs.readFileSync(colle_file).toString().match(/\\Count{(\d+)}/)[1];
		// vscode.window.showInformationMessage(count);
		
		copyPdf(tmp_pdf, count);
		fs.renameSync(tmp_pdf, fiche_pdf);
		
		// child_process.execSync(`${recipe} ${tmp_tex}`);
		// rename fiche file
		// move pdf file
		// move fiche file to fileDirname folder
		// fs.renameSync(fiche_pdf, fileDirname + '/' + path.basename(fiche_pdf));
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(fiche_pdf), { viewColumn: vscode.ViewColumn.Two });
		// });
		// insert magic command 
		// const latex_magic = `% !TEX root = ${tmp_tex}\n`;
		// add latex_magic as first line of the file
		// var editorText = editor.document.getText();
		// if (editorText.includes(`% !TEX root `)) {
		// 	editor.edit(editBuilder => {
		// 		editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
		// 		editBuilder.insert(new vscode.Position(0, 0), latex_magic);
		// 	}).then(() => {
		// 		// run latex-workshop build command
		// 		vscode.commands.executeCommand('latex-workshop.build').then(() => {
		// 			// rename fiche file
		// 			fs.renameSync(tmp_tex.replace('.tex', '.pdf'), fiche_pdf);
		// 			// move fiche file to fileDirname folder
		// 			fs.renameSync(fiche_pdf, fileDirname + '/' + path.basename(fiche_pdf));
		// 			// open the fiche pdf in vscode in the right panel
		// 			vscode.commands.executeCommand('vscode.open', vscode.Uri.file(fiche_pdf), { viewColumn: vscode.ViewColumn.Two });
		// 			// remove latex command
		// 			editor.edit(editBuilder => {
		// 				editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
		// 			});
		// 	});
		// });
		// } else {
		// 	editor.edit(editBuilder => {
		// 		editBuilder.insert(new vscode.Position(0, 0), latex_magic);
		// 	}).then(() => {
		// 		// run latex-workshop build command
		// 		vscode.commands.executeCommand('latex-workshop.build').then(() => {
		// 			// rename fiche file
		// 			fs.renameSync(tmp_tex.replace('.tex', '.pdf'), fiche_pdf);
		// 			// move fiche file to fileDirname folder
		// 			fs.renameSync(fiche_pdf, fileDirname + '/' + path.basename(fiche_pdf));
		// 			// open the fiche pdf in vscode in the right panel
		// 			vscode.commands.executeCommand('vscode.open', vscode.Uri.file(fiche_pdf), { viewColumn: vscode.ViewColumn.Two });
		// 			// remove latex command
		// 			editor.edit(editBuilder => {
		// 				editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
		// 			});
		// 		});
		// 	});
		// }
			// show the output
			// get basename of fiche
			const basename = path.basename(fiche_pdf);
			vscode.window.showInformationMessage(`${basename} généré avec succès`);
	});

	// command to see the soluce version of tex file
	let view_soluce = vscode.commands.registerCommand('flash.view_soluce', function () {
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
	let soluce = vscode.commands.registerCommand('flash.soluce', function () {
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
		child_process.execSync(`python3 ${__dirname}/build-soluce.py ${latex} ${today}`, () => {
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
	context.subscriptions.push(copy);
	context.subscriptions.push(open);	
	context.subscriptions.push(go);
	context.subscriptions.push(fetch);
	context.subscriptions.push(upload);
	context.subscriptions.push(uploading);
	context.subscriptions.push(compile);
	context.subscriptions.push(build);
	context.subscriptions.push(programme_refresh);
	// context.subscriptions.push(banque_refresh);
	// context.subscriptions.push(convert);
	context.subscriptions.push(send);
	context.subscriptions.push(compile_exercise);
	context.subscriptions.push(source);
	context.subscriptions.push(test);
	context.subscriptions.push(amc);
	context.subscriptions.push(soluce);
	context.subscriptions.push(reveal_exercise);
	context.subscriptions.push(suggestions_refresh);
	context.subscriptions.push(view_soluce);
	context.subscriptions.push(compile_bilan_DS);
	context.subscriptions.push(fiche_colle);
	context.subscriptions.push(programme_pdf);
	context.subscriptions.push(remove);

	// call here all commands necessary at launch
	vscode.commands.executeCommand('banque.refresh');

}

// This method is called when your extension is deactivated
function deactivate() {}

	
// export modules
module.exports = {
	activate,
	deactivate
}