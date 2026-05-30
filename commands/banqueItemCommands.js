var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const BanqueExoShow = require('../banque_exo_show');

// Helper: insert the TEX root line at the beginning of the file
function insertLatexMagic(editor, rootFile) {
	const editorText = editor.document.getText();
	const latex_magic = `% !TEX root = ${rootFile}.tex`;
	if (editorText.includes(`% !TEX root `)) {
		editor.edit(editBuilder => {
			const lineIndex = editorText.indexOf(latex_magic);
			const line = editor.document.lineAt(editor.document.positionAt(lineIndex).line);
			editBuilder.delete(line.range);
		}).then(() => {
			editor.edit(editBuilder => {
				editBuilder.insert(new vscode.Position(0, 0), latex_magic);
			});
		});
	} else {
		editor.edit(editBuilder => {
			editBuilder.insert(new vscode.Position(0, 0), latex_magic);
		});
	}
}

function registerBanqueItemCommands(context, options) {
	const { exoenvi, explorerCommand, styPath, programmeBalise, extensionPath } = options;

	// BANQUE EXERCICES commands
	const copy = vscode.commands.registerCommand('banque.copy', function (document) {
		// Copy the document path to the clipboard
		let editor = vscode.window.activeTextEditor;
		if (editor) {
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
	});

	// FUNCTIONS OF VIEW - ITEM - THEME //
	// copy the latex file and use it as a source in an exercise latex document (TD, ...)
	vscode.commands.registerCommand('banque.source', function (document) {
		// open the latex document in vscode
		let editor = vscode.window.activeTextEditor;
		if (editor) {
			let position = editor.selection.active;
			editor.edit(editBuilder => {
				editBuilder.insert(position, '\\Source{' + path.basename(document.filePath) + '}\n');
			});
		}
	});

	// copy the latex file and use it as a source in an exercise latex document (TD, ...)
	const open = vscode.commands.registerCommand('banque.open', function (document) {
		// open the latex document in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath));
	});

	// open the theme folder with latex chapter exercices in explorer
	vscode.commands.registerCommand('banque.folder', function (document) {
		const folderPath = document.filePath.replace(/\/[^\/]*$/, '/');
		child_process.exec(`${explorerCommand} ${folderPath}`);
	});

	vscode.commands.registerCommand('banque.addexo', function (document) {
		// open the latex document in vscode
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath)).then(() => {

			// define the text to insert at the end of the file, with the name of the exercise to edit and then highlight it
			const exo_begin = '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\\begin{' + exoenvi + '}[PC][1][colle]{';
			const exercec_name = 'Nom de l\'exercice}';
			const exo_end = '\\end{' + exoenvi + '}\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n';

			// get the active text editor and insert the text at the end of the file
			let editor = vscode.window.activeTextEditor;
			if (editor) {
				// move the cursor to the end of the file
				vscode.commands.executeCommand('cursorBottom').then(() => {
					editor.edit(editBuilder => {
						editBuilder.insert(new vscode.Position(editor.document.lineCount, 0), `\n${exo_begin}${exercec_name}\n${exo_end}\n`);
					}).then(() => {
						// find position of Nom de l'exercice and then highlight it
						let document = editor.document;
						var text = document.getText();
						var position = text.lastIndexOf(exercec_name);
						var startPosition = document.positionAt(position);
						var endPosition = document.positionAt(position + exercec_name.length);
						const range = new vscode.Range(startPosition, endPosition);
						editor.selection = new vscode.Selection(range.start, range.end);
						editor.revealRange(range, vscode.TextEditorRevealType.InCenter);
					});
				});
			}
		});
	});

	// fetch a string in a latex file, like exercise name or balise
	vscode.commands.registerCommand('banque.fetch', function (doc) {
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(doc.filePath), { viewColumn: vscode.ViewColumn.One }).then(() => {
			// Get the active text editor and string to search
			var editor = vscode.window.activeTextEditor;
			if (!editor) {
				return;
			}

			// determine the string according to banque d'exercices or programme colle call
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
	});

	// FUNCTIONS OF VIEW - ITEM - EXERCICE INLINE //

	// command to compile an exercise separately
	const banqueCompile = vscode.commands.registerCommand('banque.compile', function (document) {

		// string to search in the document
		const searchString = '\\begin{' + exoenvi + '}';

		// check if command called from the explorer context menu (document defined) or from the editor (document undefined)
		if (document === undefined) {
			var editor = vscode.window.activeTextEditor;
			if (!editor) {
				vscode.window.showInformationMessage('No active editor found.');
			}

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
			// get last } character in line in case {} characters are present in exo title
			const end = lineText.lastIndexOf('}');
			var exo = lineText.substring(start, end);
			var FilePath = editor.document.fileName;
			var SourceFile = path.basename(FilePath);
		} else {
			// open document.path
			vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath), { viewColumn: vscode.ViewColumn.One });
			var editor = vscode.window.activeTextEditor;
			var exo = document.label.replace(/"/g, '');
			var FilePath = document.filePath;
			var SourceFile = path.basename(FilePath);
		}

		// name of temporary latex exercise file
		const exercice_name = 'Exercice';
		const exercice = extensionPath + `/tmp/${exercice_name}`;
		insertLatexMagic(editor, exercice);
		// create the exercise latex file
		const template = `%&Exercice\n%\\input{${styPath}TDappli.sty}\n%\\Soluce\n% \\endofdump\n\\begin{document}\n\\Source{${SourceFile}}\n\\Ex{${exo}}\n\\end{document}`;
		fs.writeFileSync(exercice + '.tex', template);
		// compile and open the exercise
		vscode.commands.executeCommand('latex-workshop.build', { rootFile: FilePath, recipe: 'pdflatex' }).then(() => {
			// message to show that the exercise has been compiled
			vscode.window.showInformationMessage(`Exercice « ${exo} » compilé avec succès.`);
			// open tab
			vscode.commands.executeCommand('latex-workshop.tab');
		});
	});

	// FUNCTIONS ONLY USED AS KEYBINDINGS //

	// command to reveal an exercise in tree view
	const banqueReveal = vscode.commands.registerCommand('banque.reveal', function () {

		// get the active text editor
		let editor = vscode.window.activeTextEditor;
		if (!editor) {
		}

		// get label of exercise from current mouse position
		const cursorPosition = editor.selection.active;
		const editorText = editor.document.getText();
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
		} else { // Source en argument de \Ex[]{}
			// exo
			var startexo = lineText.indexOf('{') + 1;
			var endexo = lineText.lastIndexOf('}');
			var exo = lineText.substring(startexo, endexo);
			// fileName
			var start = lineText.indexOf('[') + 1;
			var end = lineText.indexOf(']');
			var fileName = lineText.substring(start, end);
			var folderName = 'undefined';
		}
		// highlight the exercise in the editor
		vscode.commands.executeCommand('extension.selectCurlyBrackets', { label: exo });

		const banque_exercices = new BanqueExoShow();
		const TreeView = vscode.window.createTreeView('banque-exercices', { treeDataProvider: banque_exercices });
		const item = banque_exercices.getTreeItemByLabel(folderName, fileName, exo);
		TreeView.reveal(item, { focus: true, select: true, expand: true });
	});

	context.subscriptions.push(copy, open, banqueCompile, banqueReveal);
}

module.exports = { registerBanqueItemCommands };
