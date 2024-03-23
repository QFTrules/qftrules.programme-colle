"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const ProgShow = require('./prog_show');
const BanqueExoShow = require('./banque_exo_show');

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

/**
 * @param {vscode.ExtensionContext} context
*/
function activate(context) {
	// Use the console to output diagnostic information (console.log) and errors (console.error)
	console.log('Congratulations, your extension "show-programme-colle" is now active!');
	
	// set the boolean variables for when clauses
	vscode.commands.executeCommand('setContext', 'static', true);

	// get the user setting variables
	const collePath = vscode.workspace.getConfiguration('Programme-de-colle').get('collepath');
	const styPath = vscode.workspace.getConfiguration('Programme-de-colle').get('stypath');
	const pythonCommand = vscode.workspace.getConfiguration('Programme-de-colle').get('Python-command');
	const programmeBalise = vscode.workspace.getConfiguration('Programme-de-colle').get('Programme-balise');
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	// let disposable = vscode.commands.registerCommand('test.colle', function () {
	// 	// The code you place here will be executed every time your command is executed


	// 	// Get the active text editor
	// 	var editor = vscode.window.activeTextEditor;
	// 	if (!editor) {
	// 		return;
	// 	}

	// 	// Access the directory where extension.js is located
    //     const extensionDir = __dirname;

	// 	// Decompose the output string into a list of words
	// 	// var output = show_programme_colle();
	// 	var output = child_process.execSync('bash ' + extensionDir + '/show_programme_colle_java.sh').toString();
	// 	var words = output.split(':');
	// 	// remove the first element of the words array
	// 	words.shift();
	// 	const type_colle = words.filter((_, index) => index % 2 == 0);
	// 	// Define a list variable with the same length as contenu
	// 	// Initialize an empty list
	// 	let all_basenames = [];
	// 	let all_documents = [];
	// 	let output_message = ['Cours : '];
	// 	// const type_colle = [
	// 	// 	'Cours : ',
	// 	// 	'TD : ',
	// 	// 	'DM : ',
	// 	// 	'DS : ',
	// 	// 	'TP : ',
	// 	// ];
	// 	const separator = ' | ';
	// 	for (let j = 0; j < type_colle.length; j++) {
	// 		var documents = words[2*j+1].trim().split(',');
	// 		// Loop through the contenu array to keep only the basename of the paths
	// 		if (documents.length !== 1) {
	// 			if (j !== 0) {
	// 				output_message = [...output_message, separator, type_colle[j], ' : '];
	// 			}
	// 			for (let i = 0; i < documents.length-1; i++) {
	// 				all_documents.push(documents[i].trim())
	// 				all_basenames.push(path.parse(documents[i].trim()).name);
	// 				output_message.push(path.parse(documents[i].trim()).name);
	// 				if (i !== documents.length-2) {
	// 					output_message = [...output_message, ', '];
	// 					}
	// 			}
	// 		} else {
	// 			// Pass
	// 		}
	// 	}

	// 	// / Concatenate the strings of the list all_documents
	// 	const concatenatedDocuments = output_message.join('')

	// 	// FIRST VERSION : Type of doc and then documents as subsequent messages : too long !
	// 	vscode.window.showInformationMessage(concatenatedDocuments, { modal: false }, 'Téléverser', ...type_colle)
	// 		.then(selection => {
	// 			// loop through the words array
	// 			for (let i = 0; i < words.length; i++) {	
	// 				// react if button clicked
	// 				const commandName = `programme-de-colle.buttonSelection${i}`;
	// 				vscode.commands.registerCommand(commandName, function () {
	// 					// If the button words[i] is clicked
	// 					if (selection === words[i]) {
	// 						// Define a list variable with the same length as contenu
	// 						var documents = words[i+1].trim().split(',');
	// 						// Define a list variable with the same length as contenu
	// 						const documents_basename = new Array(documents.length);
	// 						// Loop through the contenu array to keep only the basename of the paths
	// 						for (let i = 0; i < documents.length; i++) {
	// 							documents_basename[i] = path.parse(documents[i].trim()).name;
	// 						}
							
	// 						// show a message box to choose the document to modify
	// 						vscode.window.showInformationMessage('Sélectionner le ' + words[i] + ' à modifier', { modal: false }, 'Passer', ...documents_basename)
	// 						.then(selection => {
	// 							// loop through the words array
	// 							for (let i = 0; i < documents_basename.length; i++) {	
	// 								// Handle the button click
	// 								if (selection === documents_basename[i]) {
	// 									// Add your code here
	// 									// open the latex document in vscode
	// 									const fichier = documents[i].trim();
	// 									vscode.commands.executeCommand('vscode.open',vscode.Uri.file(fichier.trim()));
	// 									child_process.execSync(pythonCommand + ' ' + extensionDir + '/search-within-file_java.py ' + documents[i].trim() + ' "' + programmeBalise + '"');
	// 									// loop to call again the main message box
	// 									// vscode.commands.executeCommand(commandName);
	// 								}
	// 							}
	// 						});
	// 					}
	// 				});
	// 				// Call or activate the command using commandName
	// 				vscode.commands.executeCommand(commandName);
	// 			}

	// 			// Téléverser sur cahier de prépa
	// 			if (selection === 'Téléverser') {
	// 				output = child_process.execSync('bash ' + extensionDir + '/build_programme_colle_java.sh ' + collePath + ' ' + styPath + ' ' + pythonCommand).toString();
	// 				// output = child_process.execSync('/home/eb/anaconda3/bin/python3 /home/eb/Dropbox/.latex/Commands/upload_programme_colle.py').toString();
	// 				vscode.window.showInformationMessage(output, 'OK')
	// 				.then()
	// 			}
	// 		});
	// 	});

	vscode.commands.registerCommand('copy.exo', function (document) {
		// Copy the document path to the clipboard
		// child_process.execSync(`echo ${document} | xclip -selection clipboard`);
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

	// let disposable2 = vscode.commands.registerCommand('copy.exo', function (document) {
	// 	// Copy the document path to the clipboard
	// 	// child_process.execSync(`echo ${document} | xclip -selection clipboard`);
	// 	let editor = vscode.window.activeTextEditor;
	// 	if (editor) {
	// 		// let document = editor.document;
	// 		let position = editor.selection.active;
	// 		editor.edit(editBuilder => {
	// 			editBuilder.insert(position, document.label.replace(/"/g, ''));
	// 		});
	// 	}
	// 	}
	// )


	let disposable2bis = vscode.commands.registerCommand('open.latex', function (document) {
		// open the latex document in vscode
		// vscode.commands.executeCommand('vscode.open',vscode.Uri.file(document.filePath));
		// open the latex document in vscode
		// vscode.commands.executeCommand('vscode.open', vscode.Uri.file(document.filePath));
		// Add the string '\Source{' + document.filePath + '}\n' to the current editor
		let editor = vscode.window.activeTextEditor;
		if (editor) {
			// let document = editor.document;
			let position = editor.selection.active;
			editor.edit(editBuilder => {
				editBuilder.insert(position, '\\Source{' + path.basename(document.filePath) + '}\n');
			});
		}
	})

	let disposable3bis = vscode.commands.registerCommand('fetch.exo', function () {
		// open an exercise listed in the file /tmp/exercices-sans-difficulte.txt

		// Read the contents of the file
		const fileContent = fs.readFileSync(__dirname + '/tmp/exercices-sans-difficulte.txt', 'utf8');
		const lines = fileContent.split('\n');
		var [filePath, exo] = lines[0].split(':');
		var exo = exo.toString().trim();
		// vscode.window.showInformationMessage('Ouverture de ' + filePath, exo);
		// open the latex document in vscode
		vscode.commands.executeCommand('vscode.open',vscode.Uri.file(filePath));
		
		// search for the exo in the file
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

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
            vscode.window.showInformationMessage('String not found');
        }
			// child_process.execSync(pythoncommand + ' ' + __dirname + '/search-within-file_java.py ' + filePath + ' "' + exo + '"');
		}
	)



	let disposable3 = vscode.commands.registerCommand('goto.exo', function (doc) {
		// open document in vscode
		// vscode.window.showInformationMessage('Ouverture de ' + document.filePath, '\\\\\\\\ProgrammeColle');
		vscode.commands.executeCommand('vscode.open',vscode.Uri.file(doc.filePath));

		// The code you place here will be executed every time your command is executed
		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		if (doc.contextValue === 'latex') {
			var searchString = '\\ProgrammeColle';
			// vscode.window.showInformationMessage('Searching for ' + searchString + ' in ' + doc.filePath);
		} else {
			var searchString = '{' + doc.label + '}';
		}
		// Search for the string "doc.label" within the document
		// var searchString = '{' + docstring + '}';
		// vscode.window.showInformationMessage('Searching for ' + searchString + ' in ' + doc.filePath);
		// var searchOptions = {
		// 	matchCase: false,
		// 	matchWholeWord: true,
		// 	// Add any other search options here
		// };

		let document = editor.document;
        var text = document.getText();
        var position = text.indexOf(searchString);

        if (position !== -1) {
            var startPosition = document.positionAt(position);
            var endPosition = document.positionAt(position + searchString.length);
            var range = new vscode.Range(startPosition, endPosition);
            editor.selection = new vscode.Selection(range.start, range.end);
			editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
			
			// try to run the code again to select the searchstring, does not work, needs double click.
			// var text = document.getText();
			// var position = text.indexOf(searchString);
			// var startPosition = document.positionAt(position);
            // var endPosition = document.positionAt(position + searchString.length);
            // var range = new vscode.Range(startPosition, endPosition);
            // editor.selection = new vscode.Selection(range.start, range.end);
			// editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
        } else {
            vscode.window.showInformationMessage('Exercice ou balise non trouvée.');
        }
		// var searchRange = new vscode.Range(0, 0, doc.lineCount, 0);
		// editor.selection = new vscode.Selection(searchRange.start, searchRange.end);
		// editor.revealRange(searchRange, vscode.TextEditorRevealType.InCenter);
		// vscode.commands.executeCommand('editor.action.
		// ', {
		// 	query: searchString,
		// 	triggerSearch: true,
		// 	matchCase: false,
		// 	matchWholeWord: true,
		// 	isRegex: false,
		// 	filesToInclude: doc.filePath,
		// 	filesToExclude: '',
		// 	useExcludeSettingsAndIgnoreFiles: true,
		// });
		// vscode.commands.executeCommand('editor.action.nextMatchFindAction', searchString);

			// The code you place here will be executed every time your command is executed
		// Get the active text editor
		// var editor = vscode.window.activeTextEditor;
		// if (!editor) {
		// 	return;
		// }
		// Search for the string "test" within the document
		// var searchString = doc.label;
		// vscode.window.showInformationMessage('Searching for ' + searchString + ' in ' + doc.filePath);
		// var searchOptions = {
		// 	matchCase: false,
		// 	matchWholeWord: true,
		// 	// Add any other search options here
		// };
		// var searchRange = new vscode.Range(0, 0, doc.lineCount, 0);
		// var searchResults = doc.getText().match(new RegExp(searchString, 'g'));
		// then go the position of the first instance of searchresults in the file given by filepath



		// vscode.commands.executeCommand('workbench.action.findInFiles', {
		// 	query: searchString,
		// 	triggerSearch: true,
		// 	matchCase: false,
		// 	matchWholeWord: true,
		// 	isRegex: false,
		// 	filesToInclude: doc.filePath,
		// 	filesToExclude: '',
		// 	useExcludeSettingsAndIgnoreFiles: true,
		// });
		
		// Process the search results
		// if (searchResults) {
		// 	// Iterate over each search result
		// 	for (var i = 0; i < searchResults.length; i++) {
		// 		var searchResult = searchResults[i];
		// 		// Do something with each search result
		// 		console.log("Found at line " + (searchResult.range.start.line + 1) + ", column " + (searchResult.range.start.character + 1));
		// 	}
		// } else {
		// 	console.log("No matches found");
		// }

		}
	)


	// commande pour téléverser le programme de colle sur le cahier de prépa depuis title view : programme de colle
	let disposable4 = vscode.commands.registerCommand('upload.colle', function () {

		// change icon
		vscode.commands.executeCommand('setContext', 'static', false);
		

		const nextTuesdayDate = getNextMonday()[0];
		const week = getNextMonday()[1];

		// console.log(nextTuesdayDate);
		let programme_colle_file = nextTuesdayDate + '_PC_Phy_colle.pdf';
		// vscode.window.showInformationMessage(programme_colle_file);
		// // Read the contents of the collepath directory
		// fs.readdir(collepath, (err, files) => {
		// 	if (err) {
		// 		console.error(err);
		// 		return;
		// 	}
			
		// 	// Loop through each file in the directory
		// 	for (const file of files) {
		// 		vscode.window.showInformationMessage(file);
		// 		// Check if the file is of type pdf and contains the string '_PC_Phy_colle.pdf'
		// 		if (file.endsWith('_PC_Phy_colle.pdf')) {
		// 			// Set the programme_colle_file variable to the file path
		// 			programme_colle_file = file;
		// 			break; // Stop the loop if a matching file is found
		// 		}
		// 	}
		// });

		// Continue with the rest of your code...
		// vscode.window.showInformationMessage(pythoncommand +  ' ' + __dirname + '/upload_programme_colle.py ' + collepath + ' ' + programme_colle_file + ' ' + week);

		child_process.execSync(pythonCommand + ' ' + __dirname + '/upload_programme_colle.py ' + collePath + ' ' + programme_colle_file + ' ' + week).toString();
		vscode.window.showInformationMessage(programme_colle_file  + ' téléversé avec succès');

		// change icon
		vscode.commands.executeCommand('setContext', 'static', true);
		// const output = child_process.execSync('bash ' + __dirname + '/build_programme_colle_java.sh ' + collepath + ' ' + stypath + ' ' + pythoncommand + ' ' + __dirname).toString();
		// vscode.window.showInformationMessage(output, 'OK')
	});

	// commande pour compiler le programme de colle depuis title view : programme de colle
	let disposable5 = vscode.commands.registerCommand('compile.colle', function () {
		const programme_colle_file = child_process.execSync('bash ' + __dirname + '/build_programme_colle.sh ' + collePath + ' ' + styPath + ' ' + pythonCommand + ' ' + __dirname).toString();
		vscode.window.showInformationMessage(programme_colle_file  + ' compilé avec succès', { timeout: 1 });
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(path.join(collePath.trim(),programme_colle_file.trim())), { viewColumn: vscode.ViewColumn.Beside });
	});



	// commande pour compiler et téléverser le programme de colle depuis title view : programme de colle
	let disposable6 = vscode.commands.registerCommand('build.colle', function () {
		vscode.commands.executeCommand('compile.colle');
		vscode.commands.executeCommand('upload.colle');
		// first compile the programme de colle
		// let programme_colle_file = child_process.execSync('bash ' + __dirname + '/build_programme_colle.sh ' + collepath + ' ' + stypath + ' ' + pythoncommand + ' ' + __dirname).toString();
		// vscode.window.showInformationMessage(programme_colle_file + ' compilé avec succès');
		// then upload the programme de colle
		// const week = getNextMonday()[1];
		// vscode.window.showInformationMessage(pythoncommand +  ' ' + __dirname + '/upload_programme_colle.py ' + collepath + ' ' + programme_colle_file + ' ' + week);
		// const output = child_process.execSync(pythoncommand +  ' ' + __dirname + '/upload_programme_colle.py ' + collepath + ' ' + programme_colle_file + ' ' + week).toString();
		// vscode.window.showInformationMessage(output)
	});


	// Make these functions active
	// context.subscriptions.push(disposable);
	// context.subscriptions.push(disposable2);
	context.subscriptions.push(disposable2bis);
	context.subscriptions.push(disposable3);
	context.subscriptions.push(disposable3bis);
	context.subscriptions.push(disposable4);
	context.subscriptions.push(disposable5);
	context.subscriptions.push(disposable6);

	// register data providers
	const programme_colle = new ProgShow();
	vscode.window.registerTreeDataProvider('programme-colle', programme_colle);
	vscode.window.registerTreeDataProvider('package-banque', new BanqueExoShow());
	// vscode.commands.registerCommand('programme-colle.refresh', () => {
			// vscode.commands.executeCommand('show.colle');
			// programme_colle.refresh();
	// });
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}