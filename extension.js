"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const ProgShow = require('./prog_show');
const BanqueExoShow = require('./banque_exo_show');
// const GetTypeExo = BanqueExoShow.GetTypeExo;
// const pdfjsLib = require('pdfjs-dist');
// const pdfWriter = require('pdfwriter');

// set the boolean variables to change icon when uploading programme de colle
vscode.commands.executeCommand('setContext', 'static', true);

// Function to get the next Monday date for the programme de colle
function getNextMonday() {
	const today = new Date();
	const nextMonday = new Date(today.getTime() + (7 - today.getDay() + 1) * 24 * 60 * 60 * 1000);
	const year = nextMonday.getFullYear();
	const month = String(nextMonday.getMonth() + 1).padStart(2, '0');
	const day = String(nextMonday.getDate()).padStart(2, '0');
	const dayOfWeek = nextMonday.toLocaleDateString('fr', { weekday: 'long' });
	const monthName = nextMonday.toLocaleDateString('fr', { month: 'long' });
	return [`${year}_${month}_${day}`,`"${dayOfWeek} ${day} ${monthName} ${year}"`];
};

// // register the completion item provider for latex documents
// vscode.languages.registerCompletionItemProvider('latex', {
	
	// 	provideCompletionItems() {
		
		
		// 		// a simple completion item which inserts `Hello World!`
		// 		const simpleCompletion = new vscode.CompletionItem('Hello World!');
		
		// 		// a completion item that inserts its text as snippet,
		// 		// the `insertText`-property is a `SnippetString` which will be
		// 		// honored by the editor.
		// 		const snippetCompletion = new vscode.CompletionItem('Good part of the day');
		// 		snippetCompletion.insertText = new vscode.SnippetString('Good ${1|morning,afternoon,evening|}. It is ${1}, right?');
		// 		const docs = new vscode.MarkdownString("Inserts a snippet that lets you select [link](x.ts).");
		// 		snippetCompletion.documentation = docs;
		// 		docs.baseUri = vscode.Uri.parse('http://example.com/a/b/c/');
		
		// 		// a completion item that can be accepted by a commit character,
		// 		// the `commitCharacters`-property is set which means that the completion will
		// 		// be inserted and then the character will be typed.
		// 		const commitCharacterCompletion = new vscode.CompletionItem('console');
		// 		commitCharacterCompletion.commitCharacters = ['.'];
		// 		commitCharacterCompletion.documentation = new vscode.MarkdownString('Press `.` to get `console.`');
		
		// 		// a completion item that retriggers IntelliSense when being accepted,
		// 		// the `command`-property is set which the editor will execute after 
		// 		// completion has been inserted. Also, the `insertText` is set so that 
		// 		// a space is inserted after `new`
		// 		const commandCompletion = new vscode.CompletionItem('new');
		// 		commandCompletion.kind = vscode.CompletionItemKind.Keyword;
		// 		commandCompletion.insertText = 'new ';
		// 		commandCompletion.command = { command: 'editor.action.triggerSuggest', title: 'Re-trigger completions...' };
		
		// 		// return all completion items as array
		// 		return [
			// 			simpleCompletion,
			// 			snippetCompletion,
			// 			commitCharacterCompletion,
			// 			commandCompletion
			// 		];
			// 	}
			// });
			
			// vscode.languages.registerCompletionItemProvider(
				// 	'latex',
				// 	{
					// 		provideCompletionItems(document, position) {
						// 			const lineText = document.lineAt(position.line).text;
						// 			const linePrefix = lineText.slice(0, position.character);
						// 			const lineSuffix = lineText.slice(position.character);
						
						// 			// Check if the cursor is surrounded by {}
						// 			if (linePrefix.endsWith('\Ex{') && lineSuffix.startsWith('}')) {
							// 				// Return your completion items here
							// 				return [
								// 					new vscode.CompletionItem('item1'),
								// 					new vscode.CompletionItem('item2'),
								// 					new vscode.CompletionItem('item3')
								// 				];
								// 			}
								
								// 			return undefined;
								// 		}
								// 	},
								// 	'{' // triggered whenever a '{' is being typed
								// );
								
								
// function suggestions_refresh() {

// 	// list of themes
// 	const themes_list = [
// 					'Thermo',
// 					'Fluide',
// 					'Ondes',
// 					'Optique',
// 					'Mecanique',
// 				]

// 	themes_list.forEach(function(theme) {
// 			// get the list of latex files for the theme 
// 			var latex_files = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Recueil/' + theme + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n').pop();
	
// 			vscode.window.showInformationMessage(latex_files);
// 			// try to remove the file exercices-sans-difficulte.txt, pass if already removed
// 			try {
// 					fs.unlinkSync(__dirname + '/tmp/exercices-sans-difficulte.txt');
// 				} catch (error) {
// 						// pass
// 					}
			
// 					// look for all chapters in each theme
// 					latex_files.forEach(function(chapter) {
// 							// fetch all exercise names in latex file basename
// 							var exercices = child_process.execSync('grep -E "\\\\\\\\begin{exo}" ' + chapter).toString().split('\n').pop();
// 							exercices.forEach(function(exo) {
// 									var start = exo.indexOf('{', exo.indexOf('{') + 1) + 1;
// 									var end = exo.indexOf('}', exo.indexOf('}') + 1);
// 									var exo =  exo.substring(start, end);
// 									// look if the difficulty is defined for each exercise
// 									// var typeExo = GetTypeExo(exo, filePath)[0];
// 									var difficulty = GetTypeExo(exo, chapter)[1];
// 									if (difficulty !== '1' || difficulty !== '2' || difficulty !== '3') {
// 											fs.appendFileSync(__dirname  + '/tmp/exercices-sans-difficulte.txt', chapter + ':' + exo + '\n');
// 										}
// 									});
// 								});
// 							});
// 						}
						
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
	const flashDrive = vscode.workspace.getConfiguration('flash').get('flashDrive');
	
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
	let fetch = vscode.commands.registerCommand('banque.fetch', function (doc) {
		// open document in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(doc.filePath), { viewColumn: vscode.ViewColumn.One });

		// Get the active text editor and string to search
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		if (doc.contextValue === 'latex') {
			var searchString = programmeBalise;
		} else {
			var searchString = '{' + doc.label + '}';
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
		child_process.execSync(pythonCommand + ' ' + __dirname + '/upload_programme_colle.py ' + collePath + ' ' + programme_colle_file + ' ' + week).toString();
		vscode.window.showInformationMessage(programme_colle_file  + ' téléversé avec succès');

		// change icon
		vscode.commands.executeCommand('setContext', 'static', true);
	});

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

	
	let banque_refresh = vscode.commands.registerCommand('banque.refresh', () => {
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
		// get the file path
		const filePath = editor.document.fileName;
		// change the file extension to .pdf
		const pdfFilePath = filePath.replace(/\.[^/.]+$/, ".pdf");
		const pdfFilePath_soluce = filePath.replace(/\.[^/.]+$/, "_soluce.pdf");
		const pdfFilePath_bilan = filePath.substring(0, filePath.indexOf('_')) + '_bilan.pdf';
		// check if the destination path is a directory
		if (fs.existsSync(flashDrive) && fs.lstatSync(flashDrive).isDirectory()) {
			// copy the file to the flash drive with the new file extension
			const fileName = path.basename(pdfFilePath);
			const destinationPath = path.join(flashDrive, fileName);
			fs.copyFileSync(pdfFilePath, destinationPath);
			// show information message
			vscode.window.showInformationMessage(`${fileName} copied to ${flashDrive}`);
			// check if the soluce file exists
			if (fs.existsSync(pdfFilePath_soluce)) {
				// copy the soluce file to the flash drive with the new file extension
				const soluceFileName = path.basename(pdfFilePath_soluce);
				const soluceDestinationPath = path.join(flashDrive, soluceFileName);
				fs.copyFileSync(pdfFilePath_soluce, soluceDestinationPath);
				// show information message
				vscode.window.showInformationMessage(`${soluceFileName} copied to ${flashDrive}`);
			}
			if (fs.existsSync(pdfFilePath_bilan)) {
				// copy the bilan file to the flash drive with the new file extension
				const bilanFileName = path.basename(pdfFilePath_bilan);
				const bilanDestinationPath = path.join(flashDrive, bilanFileName);
				fs.copyFileSync(pdfFilePath_bilan, bilanDestinationPath);
				// show information message
				vscode.window.showInformationMessage(`${bilanFileName} copied to ${flashDrive}`);
			}
		} else {
			vscode.window.showErrorMessage('Invalid destination path');
		}
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
		} else {
			var exo = document.label.replace(/"/g, '');
			// vscode.window.showInformationMessage(exo, document.filePath);
			vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath)).then(() => {
				// just pass
			}
			);
		}

		// name of temporary latex exercise file
		const exercice = 'Exercice'

		// get the basename with extension of current latex file 
		// if (document === undefined) {
			// insert the TEX root line at the beginning of the file
		const editorText = editor.document.getText();
		const latex_magic = `% !TEX root = ${__dirname}/tmp/${exercice}.tex\n`;
		if (editorText.includes(`% !TEX root `)) {
			editor.edit(editBuilder => {
				editBuilder.delete(new vscode.Range(new vscode.Position(0, 0), new vscode.Position(1, 0)));
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			}).then(() => {});
		} else {
			editor.edit(editBuilder => {
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			}).then(() => {});
		}
		// if (!editorText.includes(`% !TEX root = ${__dirname}/tmp`)) {
		// 	editor.edit(editBuilder => {
		// 			editBuilder.insert(new vscode.Position(0, 0), latex_magic);
		// 		}).then(() => {
		// 			//  just pass
		// 	});
		// }
		var filePath = editor.document.fileName;
		var fileName = path.basename(editor.document.fileName);
		// } else {	
			// var fileName = path.basename(document.filePath);
		// }

		// write a new template latex file in directory tmp 
		// const template = `\\input{TD.sty}\n\\begin{document}\n\\Source{${fileName}}\n\\Ex{${exo}}\n\\end{document}`;
		// const template = `\\input{TD.sty}\n\\Soluce\n\\begin{document}\n\\Source{${fileName}}\n\\Ex{${exo}}\n\\end{document}`;
		const template = `%&Exercice\n% \\input{TDappli.sty}\n% \\endofdump\n\\Soluce\n\\begin{document}\n\\Source{${fileName}}\n\\Ex{${exo}}\n\\end{document}`;
		fs.writeFileSync(__dirname + `/tmp/${exercice}.tex`, template);
		// compile the template file and open when finished
		vscode.commands.executeCommand('latex-workshop.build', {rootFile:filePath}).then(() => {
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
		var chapter = coursDir.substring(coursDir.lastIndexOf('/') + 1);
		const theme = chapter.substring(chapter.lastIndexOf('/') + 1).substring(1, 2);
		var chapter = chapter.substring(1, 2);
		// .substring(2, 3);
		// vscode.window.showInformationMessage(theme + '-' + chapter);
		// const destination = '/home/eb/MC-Projects/QCM-PC/QCM.tex';
		// make directory if not existent
		var destination = '/home/eb/MC-Projects/QCM-PC-' + theme + '-' + chapter;
		if (!fs.existsSync(destination)) {
			fs.mkdirSync(destination);}
		//  copy template file to another name in the same directory
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
		child_process.execSync(`auto-multiple-choice prepare --mode=s ${destination}`, { stdio: 'ignore' });
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
		child_process.execSync(`auto-multiple-choice`);
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
	context.subscriptions.push(banque_refresh);
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

	// use banque compile ones to initialize tmp/Exercice.tex
	// vscode.commands.executeCommand('banque.compile');

	// // register the completion item provider for latex documents
	// let complet1 = vscode.languages.registerCompletionItemProvider('latex', {

	// 	provideCompletionItems() {


	// 		// a simple completion item which inserts `Hello World!`
	// 		const simpleCompletion = new vscode.CompletionItem('Hello World!');

	// 		// a completion item that inserts its text as snippet,
	// 		// the `insertText`-property is a `SnippetString` which will be
	// 		// honored by the editor.
	// 		const snippetCompletion = new vscode.CompletionItem('Good part of the day');
	// 		snippetCompletion.insertText = new vscode.SnippetString('Good ${1|morning,afternoon,evening|}. It is ${1}, right?');
	// 		const docs = new vscode.MarkdownString("Inserts a snippet that lets you select [link](x.ts).");
	// 		snippetCompletion.documentation = docs;
	// 		docs.baseUri = vscode.Uri.parse('http://example.com/a/b/c/');

	// 		// a completion item that can be accepted by a commit character,
	// 		// the `commitCharacters`-property is set which means that the completion will
	// 		// be inserted and then the character will be typed.
	// 		const commitCharacterCompletion = new vscode.CompletionItem('console');
	// 		commitCharacterCompletion.commitCharacters = ['.'];
	// 		commitCharacterCompletion.documentation = new vscode.MarkdownString('Press `.` to get `console.`');

	// 		// a completion item that retriggers IntelliSense when being accepted,
	// 		// the `command`-property is set which the editor will execute after 
	// 		// completion has been inserted. Also, the `insertText` is set so that 
	// 		// a space is inserted after `new`
	// 		const commandCompletion = new vscode.CompletionItem('new');
	// 		commandCompletion.kind = vscode.CompletionItemKind.Keyword;
	// 		commandCompletion.insertText = 'new ';
	// 		commandCompletion.command = { command: 'editor.action.triggerSuggest', title: 'Re-trigger completions...' };

	// 		// return all completion items as array
	// 		return [
	// 			simpleCompletion,
	// 			snippetCompletion,
	// 			commitCharacterCompletion,
	// 			commandCompletion
	// 		];
	// 	}
	// });

	// let complet2 = vscode.languages.registerCompletionItemProvider(
	// 	'latex',
	// 	{
	// 		provideCompletionItems(document, position) {

	// 			// get all text until the `position` and check if it reads `console.`
	// 			// and if so then complete if `log`, `warn`, and `error`
	// 			const linePrefix = document.lineAt(position).text.slice(0, position.character);
	// 			if (!linePrefix.endsWith('console.')) {
	// 				return undefined;
	// 			}

	// 			return [
	// 				new vscode.CompletionItem('log', vscode.CompletionItemKind.Method),
	// 				new vscode.CompletionItem('warn', vscode.CompletionItemKind.Method),
	// 				new vscode.CompletionItem('error', vscode.CompletionItemKind.Method),
	// 			];
	// 		}
	// 	},
	// 	'.' // triggered whenever a '.' is being typed
	// );

	// context.subscriptions.push(complet1, complet2);

}

// This method is called when your extension is deactivated
function deactivate() {}

	
// export modules
module.exports = {
	activate,
	deactivate
}