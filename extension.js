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

	let disposable3 = vscode.commands.registerCommand('goto.exo', function (doc) {
		// open document in vscode
		vscode.commands.executeCommand('vscode.open',vscode.Uri.file(doc.filePath));

		// The code you place here will be executed every time your command is executed
		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}
		// Search for the string "doc.label" within the document
		var searchString = '{' + doc.label + '}';
		// vscode.window.showInformationMessage('Searching for ' + searchString + ' in ' + doc.filePath);
		// var searchOptions = {
		// 	matchCase: false,
		// 	matchWholeWord: true,
		// 	// Add any other search options here
		// };

		let document = editor.document;
        let text = document.getText();
        let position = text.indexOf(searchString);

        if (position !== -1) {
            let startPosition = document.positionAt(position);
            let endPosition = document.positionAt(position + searchString.length);
            let range = new vscode.Range(startPosition, endPosition);
            editor.selection = new vscode.Selection(range.start, range.end);
			editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
        } else {
            vscode.window.showInformationMessage('String not found');
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

	let disposable4 = vscode.commands.registerCommand('push.colle', function () {
		child_process.execSync('bash ' + __dirname + '/build_programme_colle_java.sh ' + collepath + ' ' + stypath + ' ' + pythoncommand).toString();
	});


	// Make these functions active
	context.subscriptions.push(disposable);
	context.subscriptions.push(disposable2);
	context.subscriptions.push(disposable3);
	context.subscriptions.push(disposable4);
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
const fs = require('fs');
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

		// this.data.push(new TreeItem('', undefined, undefined, undefined, {
		// 	command: 'command:push.colle',
		// 	title: 'Your message here',
		// 	tooltip: 'Your message here',
		// 	contextValue: 'message'
		// }));

	
		// this.data.push(new TreeItem('Téléverser', undefined, undefined, 'push.colle', {
		// 	command: 'push.colle',
		// 	title: 'Téléverser',
		// 	tooltip: 'Téléverser',
		// 	// iconPath: {
		// 	// 	light: path.join(__filename, '..', 'resources', 'light', 'upload.svg'),
		// 	// 	dark: path.join(__filename, '..', 'resources', 'dark', 'upload.svg')
		// 	// },
		// 	contextValue: 'push.colle'
		// }));
		
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

function GetTypeExo(label, filepath) {
	// filepath in undefined for items in programme de colle
	if (typeof filepath === 'undefined') {
		return '';
	}
	
	// if no error, returns the info about the exercise
	const fileContent = fs.readFileSync(filepath, 'utf8');
	const lines = fileContent.split('\n');
	for (let i = 0; i < lines.length; i++) {
		if (lines[i].includes(label)) {
			// get the type of exercise (python, devoir, ...)
			var startIndex = lines[i].lastIndexOf('[') + 1;
			var endIndex = lines[i].lastIndexOf(']');
			const typeexo = lines[i].substring(startIndex, endIndex);
			// get the difficulty of the exercise (on, two, three stars)
			var startIndex = lines[i].indexOf('[', lines[i].indexOf('[') + 1) + 1;
			var endIndex = lines[i].indexOf(']', lines[i].indexOf(']') + 1);
			const difficulty = lines[i].substring(startIndex, endIndex);
			// return the type of exercise and its difficulty
			return [typeexo, difficulty];
		}
	}
	return '';
}

var TreeItem = /** @class */ (function (_super) {
	__extends(TreeItem, _super);
	function TreeItem(label, children, filePath, contextValue, collapsed) {
		var _this = _super.call(this, label, children === undefined ? vscode.TreeItemCollapsibleState.None :
			vscode.TreeItemCollapsibleState.Expanded) || this;
		_this.children = children;
		_this.filePath = filePath;
		_this.contextValue = contextValue;
		if (typeof collapsed === 'undefined') {
			_this.collapsibleState = vscode.TreeItemCollapsibleState.Expanded;
		} else {
			_this.collapsibleState = collapsed;
		}

		// get the type of exercise and its difficulty
		var typeexo = GetTypeExo(label, filePath)[0]
		var difficulty = GetTypeExo(label, filePath)[1]
		_this.description = _this.contextValue === 'file' ? '★'.repeat(difficulty) : '';

		// define context-specific icons for banque-exercices
		if (_this.contextValue === 'file') {
			if (typeexo.includes('python')) {
				_this.iconPath = {
					light: path.join(__dirname, 'images', 'file_type_python.svg'),
					dark: path.join(__dirname, 'images', 'file_type_python.svg')
				};
			} else {
				if (typeexo.includes('TD')) {
					_this.iconPath = {
						light: path.join(__dirname, 'images', 'paper_light.png'),
						dark: path.join(__dirname, 'images', 'paper_dark.png')
					};
				} else {
					if (typeexo.includes('colle')) {
						_this.iconPath = {
							// light: path.join(__dirname, 'images', 'chalk_light.png'),
							// dark: path.join(__dirname, 'images', 'chalk_dark.png')
							light: path.join(__dirname, 'images', 'pencil_light.png'),
							dark: path.join(__dirname, 'images', 'pencil_dark.png')
						};
					} else {
					_this.iconPath = {
						// light: path.join(__dirname, 'images', 'default_file.svg'),
						// dark: path.join(__dirname, 'images', 'default_file.svg')
						light: path.join(__dirname, 'images', 'paper_light.png'),
						dark: path.join(__dirname, 'images', 'paper_dark.png')
					};
					}
				}
			}
		// define specific icon for programme-colle	
		} else {
			if (label === 'Cours') {
				_this.iconPath = {
					light: path.join(__dirname, 'images', 'chalkboard_light.png'),
					dark: path.join(__dirname, 'images', 'chalkboard_dark.png')
				};
			} else {
				if (label === 'TD') {
					_this.iconPath = {
						light: path.join(__dirname, 'images', 'pencil_light.png'),
						dark: path.join(__dirname, 'images', 'pencil_dark.png')
					};
				} else {
					if (label === 'DM') {
						_this.iconPath = {
							light: path.join(__dirname, 'images', 'house_light.png'),
							dark: path.join(__dirname, 'images', 'house_dark.png')
						};
					} else {
						if (label === 'TP') {
							_this.iconPath = {
								light: path.join(__dirname, 'images', 'flask_light.png'),
								dark: path.join(__dirname, 'images', 'flask_dark.png')
							};
						} else {
							if (label === 'DS') {
								_this.iconPath = {
									light: path.join(__dirname, 'images', 'paper_light.png'),
									dark: path.join(__dirname, 'images', 'paper_dark.png')
								};
							} else {
								if (contextValue === 'folder') {
									_this.iconPath = {
										light: path.join(__dirname, 'images', 'default_folder_opened.svg'),
										dark: path.join(__dirname, 'images', 'default_folder_opened.svg')
									};
								}
							}
						}
					}
				}
			}
		}
		// test to add action on item click
		// _this.command = {
		// 		title: "Ouvrir exercice",
		// 		command: "goto.exo", 
		// 		arguments: [filePath]
		// 	};
		return _this;
	}

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
		const themes_list = [
			'Thermo',
			'Fluide',
			'Ondes',
			'Optique',
			'Mecanique',
		]
		this.data = themes_list.map(function(theme) {
			// get the list of latex files for the theme 
			var latex_files = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Recueil/' + theme + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n');
			// remove the last element which is an empty string
			latex_files.pop();
			// get only the basename of filenames
			// latex_files = latex_files.map(function(filename) {
			// 	return path.parse(filename).name;
			// });

			// return a tree item for each theme
			return new TreeItem(theme.toUpperCase(), 
				latex_files.map(function(filePath) {
					// get the latex filepath
					const basename = path.parse(filePath).name
					// var filePath = path.join('~/Dropbox/CPGE/Physique/Exercices/Recueil/', theme, basename + '.tex');
					var exercices = child_process.execSync('grep -E "\\\\\\\\begin{exo}" ' + filePath).toString().split('\n');
					exercices = exercices.map(function(exo) {
						var start = exo.indexOf('{', exo.indexOf('{') + 1) + 1;
						var end = exo.indexOf('}', exo.indexOf('}') + 1);
						return exo.substring(start, end);
					});
					// remove the last element which is an empty string
					exercices.pop();
					return new TreeItem(basename,
						exercices.map(function(exo) {
							// const exo_short = (exo.slice(0, 25) + "...").toString();
							return new TreeItem(exo, undefined, filePath, 'file');
						}),
						filePath,
						'folder',
					);
				}),
				undefined,
				'folder',
			);
		});
		// new TreeItem('COURS', [
		// 	new TreeItem('Ford', [new TreeItem('Fiesta'), new TreeItem('Focus'), new TreeItem('Mustang')]),
		// 	new TreeItem('BMW', [new TreeItem('320'), new TreeItem('X3'), new TreeItem('X5')])
		// ])];
    }

	BanqueExoShow.prototype.getTreeItem = function (element) {
		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Collapsed);
		if (element.contextValue === 'file') {
			item.tooltip = "Voir l'exercice";
			item.command = {
				command: 'goto.exo',
				title: 'Ouvrir exercice',
				arguments: [element]
			};
		}
		return item;
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


// function textEllipsis(str, maxLength, { side = "end", ellipsis = "..." } = {}) {
// 	if (str.length > maxLength) {
// 	  switch (side) {
// 		case "start":
// 		  return ellipsis + str.slice(-(maxLength - ellipsis.length));
// 		case "end":
// 		default:
// 		  return str.slice(0, maxLength - ellipsis.length) + ellipsis;
// 	  }
// 	}
// 	return str;
//   }

// register data providers
vscode.window.registerTreeDataProvider('programme-colle', new ProgShow());
vscode.window.registerTreeDataProvider('package-banque', new BanqueExoShow());
