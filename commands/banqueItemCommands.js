var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const BanqueExoShow = require('../banque_exo_show');

// Helper: insert/update the TEX root line at the beginning of the file.
async function insertLatexMagic(editor, rootFile) {
	const latexMagic = `% !TEX root = ${rootFile}.tex`;
	const lineCount = editor.document.lineCount;
	let existingMagicLine = -1;
	for (let i = 0; i < lineCount; i++) {
		const txt = editor.document.lineAt(i).text;
		if (txt.includes('% !TEX root')) {
			existingMagicLine = i;
			break;
		}
	}

	await editor.edit(editBuilder => {
		if (existingMagicLine >= 0) {
			const line = editor.document.lineAt(existingMagicLine);
			editBuilder.replace(line.range, latexMagic);
			if (existingMagicLine !== 0) {
				editBuilder.delete(line.rangeIncludingLineBreak);
				editBuilder.insert(new vscode.Position(0, 0), `${latexMagic}\n`);
			}
		} else {
			editBuilder.insert(new vscode.Position(0, 0), `${latexMagic}\n`);
		}
	});
}

function getExerciseRangeInDocument(document, exerciseLabel, exoEnvironment) {
	const text = document.getText();
	const escapedLabel = exerciseLabel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
	const envPattern = `\\\\begin\\{${exoEnvironment}\\}[^\n]*\\{${escapedLabel}\\}`;
	const regex = new RegExp(envPattern, 'g');
	let match = regex.exec(text);
	while (match) {
		const start = document.positionAt(match.index);
		const end = document.positionAt(match.index + match[0].length);
		return new vscode.Range(start, end);
	}
	return undefined;
}

async function openAndFetchExercise(doc, exoenvi, programmeBalise) {
	await vscode.commands.executeCommand('vscode.open', vscode.Uri.file(doc.filePath), { viewColumn: vscode.ViewColumn.One });
	const editor = vscode.window.activeTextEditor;
	if (!editor) {
		return undefined;
	}

	if (doc.contextValue === 'latex') {
		const text = editor.document.getText();
		const position = text.indexOf(programmeBalise);
		if (position >= 0) {
			const start = editor.document.positionAt(position);
			const end = editor.document.positionAt(position + programmeBalise.length);
			const range = new vscode.Range(start, end);
			editor.selection = new vscode.Selection(range.start, range.end);
			editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
		}
		return { editor };
	}

	const exoLabel = String(doc.rawLabel || doc.label || '').replace(/"/g, '');
	const range = getExerciseRangeInDocument(editor.document, exoLabel, exoenvi);
	if (range) {
		editor.selection = new vscode.Selection(range.start, range.end);
		editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
	} else {
		vscode.window.showWarningMessage(`Exercise "${exoLabel}" not found in ${path.basename(doc.filePath)}.`);
	}
	return { editor, exoLabel, range };
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
	vscode.commands.registerCommand('banque.fetch', async function (doc) {
		await openAndFetchExercise(doc, exoenvi, programmeBalise);
	});

	// FUNCTIONS OF VIEW - ITEM - EXERCICE INLINE //

	// command to compile an exercise separately
	const banqueCompile = vscode.commands.registerCommand('banque.compile', async function (document) {

		// string to search in the document
		const searchString = '\\begin{' + exoenvi + '}';

		// check if command called from the explorer context menu (document defined) or from the editor (document undefined)
		if (document === undefined) {
			var editor = vscode.window.activeTextEditor;
			if (!editor) {
				vscode.window.showInformationMessage('No active editor found.');
				return;
			}

			// declare the cursorPosition variable
			const cursorPosition = editor.selection.active;
			// find the first line before the cursor position that contains the string '\begin{exo}'
			let lineNumber = cursorPosition.line - 1;
			let lineText = lineNumber >= 0 ? editor.document.lineAt(lineNumber).text : '';
			while (lineNumber >= 0 && !lineText.includes(searchString)) {
				lineNumber--;
				lineText = lineNumber >= 0 ? editor.document.lineAt(lineNumber).text : '';
			}
			if (lineNumber < 0) {
				vscode.window.showWarningMessage(`No ${searchString} found before cursor.`);
				return;
			}
			// get second { character in line
			const start = lineText.indexOf('{', lineText.indexOf('{') + 1) + 1;
			// get last } character in line in case {} characters are present in exo title
			const end = lineText.lastIndexOf('}');
			var exo = lineText.substring(start, end);
			var FilePath = editor.document.fileName;
			var SourceFile = path.basename(FilePath);
		} else {
			// When invoked from tree item: fetch/highlight exercise in source file first.
			const fetched = await openAndFetchExercise(document, exoenvi, programmeBalise);
			if (!fetched || !fetched.editor) {
				vscode.window.showWarningMessage('Unable to open source file for selected exercise.');
				return;
			}
			var editor = fetched.editor;
			var exo = fetched.exoLabel || (document.rawLabel || document.label).replace(/"/g, '');
			var FilePath = document.filePath;
			var SourceFile = path.basename(FilePath);
		}

		// name of temporary latex exercise file
		const exercice_name = 'Exercice';
		const exercice = extensionPath + `/tmp/${exercice_name}`;
		await insertLatexMagic(editor, exercice);
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
