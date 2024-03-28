"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const ProgShow = require('./prog_show');
const BanqueExoShow = require('./banque_exo_show');
// const pdfjsLib = require('pdfjs-dist');
// const pdfWriter = require('pdfwriter');

// set the boolean variables for when clauses
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
	fs.readdir(__dirname + '/tmp', (err, files) => {
		if (err) throw err;
		for (const file of files) {
			fs.unlink(path.join(__dirname + '/tmp', file), err => {
				if (err) throw err;
			});
		}
	});
	
	// get the user setting variables
	const collePath = vscode.workspace.getConfiguration('programme-colle').get('collePath');
	const styPath = vscode.workspace.getConfiguration('programme-colle').get('styPath');
	const pythonCommand = vscode.workspace.getConfiguration('programme-colle').get('pythonCommand');
	const programmeBalise = vscode.workspace.getConfiguration('programme-colle').get('programmeBalise');
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
			editor.edit(editBuilder => {
				editBuilder.insert(position, document.label.replace(/"/g, ''));
			});
		}
		}
	)

	// copy the latex file and use it as a source in an exercise latex document (TD, ...)
	let open = vscode.commands.registerCommand('banque.source', function (document) {
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

	// fetch a string in a latex file, like exercise name of balise
	let fetch = vscode.commands.registerCommand('banque.fetch', function (doc) {
		// open document in vscode
		vscode.commands.executeCommand('vscode.open',vscode.Uri.file(doc.filePath));

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
		// refresh list of exercises without difficulty
		new BanqueExoShow();
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
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(path.join(collePath.trim(),programme_colle_file.trim())), { viewColumn: vscode.ViewColumn.Beside });
	});



	// commande pour compiler et téléverser le programme de colle depuis title view : programme de colle
	let build = vscode.commands.registerCommand('programme.build', function () {
		vscode.commands.executeCommand('programme.compile');
		vscode.commands.executeCommand('programme.upload');
	});

	// register data providers
	const programme_colle = new ProgShow();
	const banque_exercices = new BanqueExoShow();
	vscode.window.registerTreeDataProvider('programme-colle', programme_colle);
	vscode.window.registerTreeDataProvider('banque-exercices', banque_exercices);

	// commands to refresh the data providers
	let refresh = vscode.commands.registerCommand('programme.refresh', () => {
			programme_colle.refresh();
	});

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
		if (editor) {
			// get the file path of the active document
			const filePath = editor.document.fileName;
			vscode.window.showInformationMessage(`Current PDF file: ${filePath}`);
		} else {
			vscode.window.showErrorMessage('No active editor found');
		}
		// if (!editor) {
		// 	return;
		// }
		// get the file path
		const filePath = editor.document.fileName;
		vscode.window.showInformationMessage(`copié sur la clé USB`);
		// check if the destination path is a directory
		if (fs.existsSync(flashDrive) && fs.lstatSync(flashDrive).isDirectory()) {
			// copy the file to the flash drive
			const fileName = path.basename(filePath);
			const destinationPath = path.join(flashDrive, fileName);
			fs.copyFileSync(filePath, destinationPath);
			// show information message
		} else {
			vscode.window.showErrorMessage('Invalid destination path');
		}
	});

	// compile to compile an exercise separately
	let compile_exercise = vscode.commands.registerCommand('banque.compile', function (document = undefined) {
		
		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		
		// check if command called from the explorer context menu or from the editor (document undefined)
		if (document === undefined) {
			// declare the cursorPosition variable
			const cursorPosition = editor.selection.active;
			// find the first line before the cursor position that contains the string '\begin{exo}'
			let lineNumber = cursorPosition.line - 1;
			let lineText = editor.document.lineAt(lineNumber).text;
			while (lineNumber >= 0 && !lineText.includes('\\begin{exo}')) {
				lineNumber--;
				lineText = editor.document.lineAt(lineNumber).text;
			}
			const start = lineText.indexOf('{', lineText.indexOf('{') + 1) + 1;
			const end = lineText.indexOf('}', lineText.indexOf('}') + 1);
			var exo = lineText.substring(start, end);
		} else {
			var exo = document.label.replace(/"/g, '');
		}

		// insert the TEX root line at the beginning of the file
		const editorText = editor.document.getText();
		const exercice = 'Exercice'
		const latex_magic = `% !TEX root = ${__dirname}/tmp/${exercice}.tex\n`;
		if (!editorText.includes(`% !TEX root = ${__dirname}/tmp`)) {
			editor.edit(editBuilder => {
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			});
		}

		// get the basename with extension of current latex file 
		if (document === undefined) {
			var fileName = path.basename(editor.document.fileName);
		} else {	
			var fileName = path.basename(document.filePath);
		}

		// write a new template latex file in directory tmp 
		const template = `\\input{TD.sty}\n\\begin{document}\n\\Source{${fileName}}\n\\Ex{${exo}}\n\\end{document}`;
		fs.writeFileSync(__dirname + `/tmp/${exercice}.tex`, template);
		// compile the template file and open when finished
		vscode.commands.executeCommand('latex-workshop.build').then(() => {
			vscode.commands.executeCommand('latex-workshop.tab');
		});
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
	context.subscriptions.push(refresh);
	// context.subscriptions.push(convert);
	context.subscriptions.push(send);
	context.subscriptions.push(compile_exercise);

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