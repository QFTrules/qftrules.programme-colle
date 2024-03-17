// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
// const fs = require('fs');
const path = require('path');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "show-programme-colle" is now active!');
	
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('test.helloWorld', function () {
		// The code you place here will be executed every time your command is executed
		
		// vscode.window.showInformationMessage('test');
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		// Decompose the output string into a list of words
		var output = child_process.execSync('bash /home/eb/Dropbox/.latex/Commands/show_programme_colle.sh').toString();
		var words = output.split(':');
		// var entete = words[0].trim();
		// Access the first element of the words array
		// var firstWord = words[0].trim();
		// var substringBeforeColon = firstWord.substring(0, firstWord.indexOf(':'));
		// var firstTwoSubstrings = firstWord.split(':')[0] + ':' + firstWord.split(':')[1];
		

		// Define the directory path
		// const directoryPath = '/home/eb/Dropbox/CPGE/Physique/';
		// vscode.window.showInformationMessage(directoryPath);
		// vscode.window.showInformationMessage(firstWord);

		// remove the first element of the words array
		words.shift();

		// vscode.window.showInformationMessage(output, { modal: false }, 'Téléverser', firstWord)
		// Display a message box to the user
		// vscode.window.showInformationMessage('test');

		const oddIndexedWords = words.filter((_, index) => index % 2 == 0);
		// Define a list variable with the same length as contenu
		// Initialize an empty list
		let all_basenames = [];
		let all_documents = [];
		for (let j = 0; j < oddIndexedWords.length; j++) {
			var documents = words[j+1].trim().split(',');
			// Loop through the contenu array to keep only the basename of the paths
			for (let i = 0; i < documents.length; i++) {
				all_documents.push(documents[i].trim())
				all_basenames.push(path.parse(documents[i].trim()).name);
			}
		}
		vscode.window.showInformationMessage('test');


		// FIRST VERSION : Type of doc and then documents as subsequent messages : too long !
		// vscode.window.showInformationMessage(output, { modal: false }, 'Téléverser', ...oddIndexedWords)
		// 	.then(selection => {
		// 		// loop through the words array
		// 		for (let i = 0; i < words.length; i++) {	
		// 			// react if button clicked
		// 			if (selection === words[i]) {
		// 				// Handle the "Modifier" button click
		// 				// Add your code here
		// 				// Read the contents of the directory
		// 				// fs.readdir(directoryPath, (err, files) => {
		// 				// 	if (err) {
		// 				// 		console.error(err);
		// 				// 		return;
		// 				// 	}

		// 					// Find the file with the desired filename
		// 					// const desiredFile = files.find(file => file === `${words[i]}.tex`);
		// 					// vscode.window.showInformationMessage('File' + words[i] + '.tex' + 'found');

		// 					// if (desiredFile) {
		// 					//     const filePath = path.join(directoryPath, desiredFile);
		// 					// vscode.window.showInformationMessage(words[i+1]);
		// 				var documents = words[i+1].trim().split(',');
		// 				// Define a list variable with the same length as contenu
		// 				const documents_basename = new Array(documents.length);
		// 				// Loop through the contenu array to keep only the basename of the paths
		// 				for (let i = 0; i < documents.length; i++) {
		// 					documents_basename[i] = path.parse(documents[i].trim()).name;
		// 				}

		// 				vscode.window.showInformationMessage('Sélectionner le ' + words[i] + ' à modifier', { modal: false }, 'Passer', ...documents_basename)
		// 					.then(selection => {
		// 						// loop through the words array
		// 						for (let i = 0; i < documents_basename.length; i++) {	
		// 							// Handle the button click
		// 							if (selection === documents_basename[i]) {
		// 								// Add your code here
		// 								// open the latex document in vscode
		// 								vscode.commands.executeCommand('vscode.open',vscode.Uri.file(documents[i].trim()));

		// 								// fetch the switch command \ProgrammeColle
		// 								child_process.execSync('/home/eb/anaconda3/bin/python3 /home/eb/Dropbox/.latex/Commands/search-within-file.py ' + documents[i].trim() + ' "\\ProgrammeColle"');
		// 							}
		// 						}
		// 					});
		// 					//     child_process.execSync('code ' + words[i]);
		// 					// vscode.commands.executeCommand('vscode.open',vscode.Uri.file(words[i]));
		// 					// } else {
		// 					//     console.log(`File ${words[i]}.tex not found.`);
		// 					// }
		// 				// });
		// 			}
		// 		}
		// 		// Téléverser sur cahier de prépa
		// 		if (selection === 'Téléverser') {
		// 			output = child_process.execSync('bash /home/eb/Dropbox/.latex/Commands/upload_programme_colle.sh').toString();
		// 			vscode.window.showInformationMessage(output);
		// 		}
		// 	});

		vscode.window.showInformationMessage('', { modal: false }, 'Téléverser', ...all_basenames)

				
		// // SECOND VERSION : documents directly accessible : shorter
		// vscode.window.showInformationMessage('', { modal: false }, 'Téléverser', ...all_basenames)
		// 	.then(selection => {
		// 		// loop through the words array
		// 		for (let i = 0; i < all_basenames.length; i++) {	
		// 			// react if button clicked
		// 			if (selection === all_basenames[i]) {
		// 				// Add your code here
		// 				// open the latex document in vscode
		// 				vscode.commands.executeCommand('vscode.open',vscode.Uri.file(all_documents[i]));

		// 				// fetch the switch command \ProgrammeColle
		// 				child_process.execSync('/home/eb/anaconda3/bin/python3 /home/eb/Dropbox/.latex/Commands/search-within-file.py ' + documents[i].trim() + ' "\\ProgrammeColle"');
		// 			}
		// 		}
		// 		// Téléverser sur cahier de prépa
		// 		if (selection === 'Téléverser') {
		// 			output = child_process.execSync('bash /home/eb/Dropbox/.latex/Commands/upload_programme_colle.sh').toString();
		// 			vscode.window.showInformationMessage(output);
		// 		}
		// 	});
		

		// // VERSION with options
		// vscode.window.showQuickPick(all_basenames, { placeHolder: 'Select a document to modify' })
		// 	.then(selection => {
		// 		if (selection) {
		// 			// Handle the selected option
		// 			console.log('Selected option:', selection);
		// 		} else {
		// 			// Handle the cancellation
		// 			console.log('No option selected');
		// 		}
		// 	});
			

		// End of the function
		});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
