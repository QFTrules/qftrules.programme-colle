// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
// const fs = require('fs');
// const { execSync } = require('child_process');
const path = require('path');

// Import the function show_programme_colle from the file show_programme_colle_cours.js
// import {show_programme_colle} from "./show_programme_colle_cours.js"

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "show-programme-colle" is now active!');
	
	// LIST OF SETTINGS VARIABLES
	const collepath = vscode.workspace.getConfiguration('Programme-de-colle').get('collepath');
	const stypath = vscode.workspace.getConfiguration('Programme-de-colle').get('stypath');
	const pythoncommand = vscode.workspace.getConfiguration('Programme-de-colle').get('Python-command');
	const programmebalise = vscode.workspace.getConfiguration('Programme-de-colle').get('Programme-balise');
	
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('test.colle', function () {
		// The code you place here will be executed every time your command is executed


		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		// Access the directory where extension.js is located
        const extensionDir = __dirname;

		// Decompose the output string into a list of words
		// var output = show_programme_colle();
		var output = child_process.execSync('bash ' + extensionDir + '/show_programme_colle_java.sh').toString();
		var words = output.split(':');
		// remove the first element of the words array
		words.shift();
		const type_colle = words.filter((_, index) => index % 2 == 0);
		// Define a list variable with the same length as contenu
		// Initialize an empty list
		let all_basenames = [];
		let all_documents = [];
		let output_message = ['Cours : '];
		// const type_colle = [
		// 	'Cours : ',
		// 	'TD : ',
		// 	'DM : ',
		// 	'DS : ',
		// 	'TP : ',
		// ];
		const separator = ' | ';
		for (let j = 0; j < type_colle.length; j++) {
			var documents = words[2*j+1].trim().split(',');
			// Loop through the contenu array to keep only the basename of the paths
			if (documents.length !== 1) {
				if (j !== 0) {
					output_message = [...output_message, separator, type_colle[j], ' : '];
				}
				for (let i = 0; i < documents.length-1; i++) {
					all_documents.push(documents[i].trim())
					all_basenames.push(path.parse(documents[i].trim()).name);
					output_message.push(path.parse(documents[i].trim()).name);
					if (i !== documents.length-2) {
						output_message = [...output_message, ', '];
						}
				}
			} else {
				// Pass
			}
		}

		// / Concatenate the strings of the list all_documents
		const concatenatedDocuments = output_message.join('')

		// FIRST VERSION : Type of doc and then documents as subsequent messages : too long !
		vscode.window.showInformationMessage(concatenatedDocuments, { modal: false }, 'Téléverser', ...type_colle)
			.then(selection => {
				// loop through the words array
				for (let i = 0; i < words.length; i++) {	
					// react if button clicked
					const commandName = `programme-de-colle.buttonSelection${i}`;
					vscode.commands.registerCommand(commandName, function () {
						// If the button words[i] is clicked
						if (selection === words[i]) {
							// Define a list variable with the same length as contenu
							var documents = words[i+1].trim().split(',');
							// Define a list variable with the same length as contenu
							const documents_basename = new Array(documents.length);
							// Loop through the contenu array to keep only the basename of the paths
							for (let i = 0; i < documents.length; i++) {
								documents_basename[i] = path.parse(documents[i].trim()).name;
							}
							
							// show a message box to choose the document to modify
							vscode.window.showInformationMessage('Sélectionner le ' + words[i] + ' à modifier', { modal: false }, 'Passer', ...documents_basename)
							.then(selection => {
								// loop through the words array
								for (let i = 0; i < documents_basename.length; i++) {	
									// Handle the button click
									if (selection === documents_basename[i]) {
										// Add your code here
										// open the latex document in vscode
										const fichier = documents[i].trim();
										vscode.commands.executeCommand('vscode.open',vscode.Uri.file(fichier.trim()));
										child_process.execSync(pythoncommand + ' ' + extensionDir + '/search-within-file_java.py ' + documents[i].trim() + ' "' + programmebalise + '"');
										// loop to call again the main message box
										// vscode.commands.executeCommand(commandName);
									}
								}
							});
						}
					});
					// Call or activate the command using commandName
					vscode.commands.executeCommand(commandName);
				}

				// Téléverser sur cahier de prépa
				if (selection === 'Téléverser') {
					output = child_process.execSync('bash ' + extensionDir + '/build_programme_colle_java.sh ' + collepath + ' ' + stypath + ' ' + pythoncommand).toString();
					// output = child_process.execSync('/home/eb/anaconda3/bin/python3 /home/eb/Dropbox/.latex/Commands/upload_programme_colle.py').toString();
					vscode.window.showInformationMessage(output, 'OK')
					.then()
				}
			});
		});

	let disposable2 = vscode.commands.registerCommand('copy.exo', function (document) {
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

	// Make this function active
	context.subscriptions.push(disposable);
	context.subscriptions.push(disposable2);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}

// define action in the tree view
"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var vscode = require("vscode");
// import * as fs from 'fs';
// import * as path from 'path';
var ProgShow = /** @class */ (function () {
    function ProgShow() {
	// let disposable2 = vscode.commands.registerCommand('show.colle', function () {
		// The code you place here will be executed every time your command is executed

		// LIST OF SETTINGS VARIABLES
		// const collepath = vscode.workspace.getConfiguration('Programme-de-colle').get('collepath');
		// const stypath = vscode.workspace.getConfiguration('Programme-de-colle').get('stypath');
		// const pythoncommand = vscode.workspace.getConfiguration('Programme-de-colle').get('Python-command');
		// const programmebalise = vscode.workspace.getConfiguration('Programme-de-colle').get('Programme-balise');

		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		// Access the directory where extension.js is located
		const extensionDir = __dirname;

		// Decompose the output string into a list of words
		// var output = show_programme_colle();
		var output = child_process.execSync('bash ' + extensionDir + '/show_programme_colle_java.sh').toString();
		var words = output.split(':');
		// remove the first element of the words array
		words.shift();
		const type_colle = words.filter((_, index) => index % 2 == 0);
		// Define a list variable with the same length as contenu
		// Initialize an empty list
		// let all_basenames = [];
		// let all_documents = [];
		// let output_message = ['Cours : '];
		const type_doc = [
			'Cours' ,
			'TD',
			'DM',
			'DS',
			'TP',
		];
		var list_doc = type_doc.map(function() {
			return [];
		});
		// const separator = ' | ';
		for (let j = 0; j < type_colle.length; j++) {
			var documents = words[2*j+1].trim().split(',');
			// Loop through the contenu array to keep only the basename of the paths
			if (documents.length !== 1) {
				// if (j !== 0) {
					// output_message = [...output_message, separator, type_colle[j], ' : '];
				// }
				for (let i = 0; i < documents.length-1; i++) {
					list_doc[j] = [...list_doc[j], path.parse(documents[i].trim()).name];
					// all_basenames.push(path.parse(documents[i].trim()).name);
					// output_message.push(path.parse(documents[i].trim()).name);
					// if (i !== documents.length-2) {
						// output_message = [...output_message, ', '];
						// }
				}
			} else {
				// Pass
			}
		}



		// / Concatenate the strings of the list all_documents
		// const concatenatedDocuments = output_message.join('')
		// });
		this.data = type_doc.map(function(basename, i) {
			return new TreeItem(basename,
				list_doc[i].map(function(filename) {
					return new TreeItem(filename);
				})
			);
		});
		// new TreeItem('COURS', [
		// 	new TreeItem('Ford', [new TreeItem('Fiesta'), new TreeItem('Focus'), new TreeItem('Mustang')]),
		// 	new TreeItem('BMW', [new TreeItem('320'), new TreeItem('X3'), new TreeItem('X5')])
		// ])];
    }
    ProgShow.prototype.getTreeItem = function (element) {
        return element;
    };
    ProgShow.prototype.getChildren = function (element) {
        if (element === undefined) {
            return this.data;
        }
        return element.children;
    };
    return ProgShow;
}());

// access tree item whatever the data provider
// var TreeItem = /** @class */ (function (_super) {
//     __extends(TreeItem, _super);
//     function TreeItem(label, children) {
//         var _this = _super.call(this, label, children === undefined ? vscode.TreeItemCollapsibleState.None :
//             vscode.TreeItemCollapsibleState.Expanded) || this;
//         _this.children = children;
//         return _this;
//     }
//     return TreeItem;
// }(vscode.TreeItem));

var TreeItem = /** @class */ (function (_super) {
	__extends(TreeItem, _super);
	function TreeItem(label, children, filePath, contextValue) {
		var _this = _super.call(this, label, children === undefined ? vscode.TreeItemCollapsibleState.None :
			vscode.TreeItemCollapsibleState.Expanded) || this;
		_this.children = children;
		_this.filePath = filePath;
		_this.contextValue = contextValue;
		return _this;
	}

	// // Add missing semicolon at the end of the constructor definition
	// TreeItem.prototype.constructor = function(label) {
	// 	_super.call(this, label);
	// 	this.command = {
	// 		title: "Show error",
	// 		command: "copy.exo",
	// 		arguments: [label]
	// 	};
	// };
	return TreeItem;
}(vscode.TreeItem));

var BanqueExoShow = /** @class */ (function () {
    function BanqueExoShow() {
	// let disposable2 = vscode.commands.registerCommand('show.colle', function () {
		// The code you place here will be executed every time your command is executed

		// LIST OF SETTINGS VARIABLES
		// const collepath = vscode.workspace.getConfiguration('Programme-de-colle').get('collepath');
		// const stypath = vscode.workspace.getConfiguration('Programme-de-colle').get('stypath');
		// const pythoncommand = vscode.workspace.getConfiguration('Programme-de-colle').get('Python-command');
		// const programmebalise = vscode.workspace.getConfiguration('Programme-de-colle').get('Programme-balise');

		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		// Access the directory where extension.js is located
		// const extensionDir = __dirname;

		// Decompose the output string into a list of words
		var latex_files = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Recueil/Thermo -maxdepth 1 -type f -name "*.tex"').toString().split('\n');
		// remove the last element which is an empty string
		latex_files.pop();
		// get only the basename of filenames
		latex_files = latex_files.map(function(filename) {
			return path.parse(filename).name;
		});
		this.data = latex_files.map(function(basename) {
			var filePath = path.join('/home/eb/Dropbox/CPGE/Physique/Exercices/Recueil/Thermo', basename + '.tex');
			var exercices = child_process.execSync('grep -E "\\\\\\\\begin{exo}" ' + filePath).toString().split('\n');
			exercices = exercices.map(function(exo) {
				var start = exo.indexOf('{', exo.indexOf('{') + 1) + 1;
				var end = exo.indexOf('}', exo.indexOf('}') + 1);
				return exo.substring(start, end);
			});
			// remove the last element which is an empty string
			exercices.pop();
			// var exercices = ['exo1', 'exo2', 'exo3']
			// now display all exercices in a subtree
			// exercices = exercices.split('\n');
			// exercices = exercices.map(function(exo) {
			// 	return exo.replace('\\begin{exo}', '');
			// }
			// );
			
			// const icon = vscode.Uri.file(__dirname + '/images/default_folder_opened.svg').toString();
			return new TreeItem(basename, 
				exercices.map(function(exo) {
					return new TreeItem(exo, undefined, filePath, 'file');
				}), 
				filePath
			);
			// return new TreeItem(basename);
		});
		// new TreeItem('COURS', [
		// 	new TreeItem('Ford', [new TreeItem('Fiesta'), new TreeItem('Focus'), new TreeItem('Mustang')]),
		// 	new TreeItem('BMW', [new TreeItem('320'), new TreeItem('X3'), new TreeItem('X5')])
		// ])];
    }

    BanqueExoShow.prototype.getTreeItem = function (element) {
        // return element;
		// var item = new TreeItem(element.label, element.children, element.filePath);
		// element.command = {
		// 	command: 'copy.exo',
		// 	title: 'Copy Exercise Name',
		// 	arguments: [element.label]
		// };
		return element;
    };
    BanqueExoShow.prototype.getChildren = function (element) {
        if (element === undefined) {
            return this.data;
        }
        return element.children;
    };

	BanqueExoShow.prototype.resolveTreeItem = function (item) {
		item.tooltip = item.filePath;
		return item;
	};

    return BanqueExoShow;
}());
// var TreeItem = /** @class */ (function (_super) {
//     __extends(TreeItem, _super);
//     function TreeItem(label, children) {
//         var _this = _super.call(this, label, children === undefined ? vscode.TreeItemCollapsibleState.None :
//             vscode.TreeItemCollapsibleState.Expanded) || this;
//         _this.children = children;
//         return _this;
//     }
//     return TreeItem;
// }(vscode.TreeItem));

// register data providers
vscode.window.registerTreeDataProvider('programme-colle', new ProgShow());
vscode.window.registerTreeDataProvider('package-banque', new BanqueExoShow());
