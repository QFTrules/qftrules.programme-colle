"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
Object.defineProperty(exports, "__esModule", { value: true });
// import { DepNodeProvider, Dependency } from './treeview';

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
			return [typeexo, difficulty];
			}
		}
		return '';
	}

// define action in the tree view
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

// define the properties of the tree items, notably the icons, descriptions, and the collapsible states
var TreeItem = /** @class */ (function (_super) {
	__extends(TreeItem, _super);
	function TreeItem(label, children, filePath, contextValue, collapsed) {
		// _this is used to keep the initial object this avaible in the constructor
		var _this = _super.call(this, label, children === undefined ? vscode.TreeItemCollapsibleState.None :
			vscode.TreeItemCollapsibleState.Expanded) || this;
			_this.children = children;
			_this.filePath = filePath;
			_this.contextValue = contextValue;

			// define the collapsible state of the tree items, expanded by default
			if (typeof collapsed === 'undefined') {
				_this.collapsibleState = vscode.TreeItemCollapsibleState.Expanded;
			} else {
				_this.collapsibleState = collapsed;
			}
			
			//  do not show the small arrow indicating the collapsed state for files (leaves of the tree)
			if (_this.contextValue === 'file' || _this.contextValue === 'pdf' || _this.contextValue === 'latex') {
				_this.collapsibleState = vscode.TreeItemCollapsibleState.None;
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
							light: path.join(__dirname, 'images', 'pencil_light.png'),
							dark: path.join(__dirname, 'images', 'pencil_dark.png')
						};
					} else {
						if (typeexo.includes('colle')) {
							_this.iconPath = {
								light: path.join(__dirname, 'images', 'chalkboard_light.png'),
								dark: path.join(__dirname, 'images', 'chalkboard_dark.png')
							};
						} else {
						_this.iconPath = {
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
									if (contextValue === 'folder' || contextValue === 'chapter') {
										_this.iconPath = {
											light: path.join(__dirname, 'images', 'default_folder_opened.svg'),
											dark: path.join(__dirname, 'images', 'default_folder_opened.svg')
										};
										} else {
										if (contextValue === 'pdf') {
											_this.iconPath = {
												light: path.join(__dirname, 'images', 'file_type_pdf.svg'),
												dark: path.join(__dirname, 'images', 'file_type_pdf.svg')
											};
										}
									}
								}
							}
						}
					}
				}
			}
		return _this;
	}

	return TreeItem;
}(vscode.TreeItem));


// define the data providers for the programme de colle panel
class ProgShow {
    constructor() {
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
					list_doc[j] = [...list_doc[j], documents[i].trim()];
					// list_doc[j] = [...list_doc[j], path.parse(documents[i].trim()).name];
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
				list_doc[i].map(function(filePath) {
					var filename = path.basename(filePath).toString();
					return new TreeItem(filename, undefined, filePath, 'latex', undefined);
				})
			);
		});

		var programme_colle_pdf = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Colles/PC/ -maxdepth 1 -type f -name "*_PC_Phy_colle.pdf"').toString().split('\n')[0];
		var programme_colle_pdf_basename = path.basename(programme_colle_pdf);
		this.data.push(new TreeItem(programme_colle_pdf_basename, undefined, programme_colle_pdf, 'pdf', undefined));

    }
    
	getTreeItem(element) {
		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Expanded);
		if (element.contextValue === 'pdf') {
			item.tooltip = "Ouvrir pdf";
			item.command = {
				command: 'vscode.open',
				arguments: [vscode.Uri.file(element.filePath), { viewColumn: vscode.ViewColumn.Beside }]
			};
		} else {
			if (element.contextValue === 'latex') {
				item.tooltip = "Modifier le fichier";
				item.command = {
					command: 'goto.exo',
					arguments: [element]
				};
			}
		}
		return item;
    };

    getChildren(element) {
        if (element === undefined) {
            return this.data;
        }
        return element.children;
    };

	// to refresh tree elements of the programme de colle
	onDidChangeTreeData(listener) {
		// Implement the onDidChangeTreeData method
		this.changeTreeDataListener = listener;
	};

	refresh() {
		// Call this method whenever you want to refresh the tree view
		if (this.changeTreeDataListener) {
			this.changeTreeDataListener();
		}
	};
};

// // define the data providers for the programme de colle panel
// var ProgShow = /** @class */ (function () {
//     function ProgShow() {
// 	// let disposable2 = vscode.commands.registerCommand('show.colle', function () {
// 		// The code you place here will be executed every time your command is executed

// 		// LIST OF SETTINGS VARIABLES
// 		// const collepath = vscode.workspace.getConfiguration('Programme-de-colle').get('collepath');
// 		// const stypath = vscode.workspace.getConfiguration('Programme-de-colle').get('stypath');
// 		// const pythoncommand = vscode.workspace.getConfiguration('Programme-de-colle').get('Python-command');
// 		// const programmebalise = vscode.workspace.getConfiguration('Programme-de-colle').get('Programme-balise');

// 		// Get the active text editor
// 		var editor = vscode.window.activeTextEditor;
// 		if (!editor) {
// 			return;
// 		}

		

// 		// Access the directory where extension.js is located
// 		const extensionDir = __dirname;

// 		// Decompose the output string into a list of words
// 		// var output = show_programme_colle();
// 		var output = child_process.execSync('bash ' + extensionDir + '/show_programme_colle_java.sh').toString();
// 		var words = output.split(':');
// 		// remove the first element of the words array
// 		words.shift();
// 		const type_colle = words.filter((_, index) => index % 2 == 0);
// 		// Define a list variable with the same length as contenu
// 		// Initialize an empty list
// 		// let all_basenames = [];
// 		// let all_documents = [];
// 		// let output_message = ['Cours : '];
// 		const type_doc = [
// 			'Cours' ,
// 			'TD',
// 			'DM',
// 			'DS',
// 			'TP',
// 		];
// 		var list_doc = type_doc.map(function() {
// 			return [];
// 		});
// 		// const separator = ' | ';
// 		for (let j = 0; j < type_colle.length; j++) {
// 			var documents = words[2*j+1].trim().split(',');
// 			// Loop through the contenu array to keep only the basename of the paths
// 			if (documents.length !== 1) {
// 				// if (j !== 0) {
// 					// output_message = [...output_message, separator, type_colle[j], ' : '];
// 				// }
// 				for (let i = 0; i < documents.length-1; i++) {
// 					list_doc[j] = [...list_doc[j], documents[i].trim()];
// 					// list_doc[j] = [...list_doc[j], path.parse(documents[i].trim()).name];
// 					// all_basenames.push(path.parse(documents[i].trim()).name);
// 					// output_message.push(path.parse(documents[i].trim()).name);
// 					// if (i !== documents.length-2) {
// 						// output_message = [...output_message, ', '];
// 						// }
// 				}
// 			} else {
// 				// Pass
// 			}
// 		}



// 		// / Concatenate the strings of the list all_documents
// 		// const concatenatedDocuments = output_message.join('')
// 		// });
// 		this.data = type_doc.map(function(basename, i) {
// 			return new TreeItem(basename,
// 				list_doc[i].map(function(filePath) {
// 					var filename = path.basename(filePath).toString();
// 					return new TreeItem(filename, undefined, filePath, 'latex', undefined);
// 				})
// 			);
// 		});

// 		var programme_colle_pdf = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Colles/PC/ -maxdepth 1 -type f -name "*_PC_Phy_colle.pdf"').toString().split('\n')[0];
// 		var programme_colle_pdf_basename = path.basename(programme_colle_pdf);
// 		this.data.push(new TreeItem(programme_colle_pdf_basename, undefined, programme_colle_pdf, 'pdf', undefined));

//     }
//     ProgShow.prototype.getTreeItem = function (element) {
// 		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Expanded);
// 		if (element.contextValue === 'pdf') {
// 			item.tooltip = "Ouvrir pdf";
// 			item.command = {
// 				command: 'vscode.open',
// 				arguments: [vscode.Uri.file(element.filePath), { viewColumn: vscode.ViewColumn.Beside }]
// 			};
// 		} else {
// 			if (element.contextValue === 'latex') {
// 				item.tooltip = "Modifier le fichier";
// 				item.command = {
// 					command: 'goto.exo',
// 					arguments: [element]
// 				};
// 			}
// 		}
// 		return item;
//     };

//     ProgShow.prototype.getChildren = function (element) {
//         if (element === undefined) {
//             return this.data;
//         }
//         return element.children;
//     };

// 	// to refresh tree elements of the programme de colle
// 	ProgShow.prototype.onDidChangeTreeData = function (listener) {
// 		// Implement the onDidChangeTreeData method
// 		this.changeTreeDataListener = listener;
// 	};

// 	ProgShow.prototype.refresh = function () {
// 		// Call this method whenever you want to refresh the tree view
// 		if (this.changeTreeDataListener) {
// 			this.changeTreeDataListener();
// 		}
// 	};
//     return ProgShow;
// }());


// define the data providers for the programme de colle panel
class BanqueExoShow {
    constructor() {

		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

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
			// remove the file that stores all exercices where the difficulty is not specified
			fs.unlinkSync(__dirname + '/tmp/exercices-sans-difficulte.txt');

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
							var difficulty = GetTypeExo(exo, filePath)[1]
							if (difficulty !== '1' || difficulty !== '2' || difficulty !== '3') {
								// add this exercise to a file that stores all exercices where the difficulty is not specified
								fs.appendFileSync(__dirname  + '/tmp/exercices-sans-difficulte.txt', filePath + ':' + exo + '\n');
								// vscode.window.showInformationMessage('Exercice sans difficulté : ' + exo + ' dans ' + filePath);
							}
							// const exo_short = (exo.slice(0, 25) + "...").toString();
							return new TreeItem(exo, undefined, filePath, 'file');
						}),
						filePath,
						'chapter',
						undefined
					);
				}),
				undefined,
				'folder',
				undefined
			);
		});
    }

	// define here the command to call when clicking on the tree items
	getTreeItem(element) {
		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Collapsed);
		if (element.contextValue === 'file') {
			item.tooltip = "Voir l'exercice";
			item.command = {
				command: 'goto.exo',
				title: 'Ouvrir exercice',
				arguments: [element]
			}
		} 
		return item;
	};

    getChildren(element) {
        if (element === undefined) {
            return this.data;
        }
        return element.children;
    };

	resolveTreeItem(item) {
		item.tooltip = item.filePath;
		return item;
	};
};

// define the data providers for the banque d'exercices panel
// var BanqueExoShow = /** @class */ (function () {
//     function BanqueExoShow() {

// 		// Get the active text editor
// 		var editor = vscode.window.activeTextEditor;
// 		if (!editor) {
// 			return;
// 		}

// 		// Decompose the output string into a list of words
// 		const themes_list = [
// 			'Thermo',
// 			'Fluide',
// 			'Ondes',
// 			'Optique',
// 			'Mecanique',
// 		]
// 		this.data = themes_list.map(function(theme) {
// 			// get the list of latex files for the theme 
// 			var latex_files = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Recueil/' + theme + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n');
// 			// remove the last element which is an empty string
// 			latex_files.pop();
// 			// remove the file that stores all exercices where the difficulty is not specified
// 			fs.unlinkSync(__dirname + '/tmp/exercices-sans-difficulte.txt');

// 			// return a tree item for each theme
// 			return new TreeItem(theme.toUpperCase(), 
// 				latex_files.map(function(filePath) {
// 					// get the latex filepath
// 					const basename = path.parse(filePath).name
// 					// var filePath = path.join('~/Dropbox/CPGE/Physique/Exercices/Recueil/', theme, basename + '.tex');
// 					var exercices = child_process.execSync('grep -E "\\\\\\\\begin{exo}" ' + filePath).toString().split('\n');
// 					exercices = exercices.map(function(exo) {
// 						var start = exo.indexOf('{', exo.indexOf('{') + 1) + 1;
// 						var end = exo.indexOf('}', exo.indexOf('}') + 1);
// 						return exo.substring(start, end);
// 					});
// 					// remove the last element which is an empty string
// 					exercices.pop();
// 					return new TreeItem(basename,
// 						exercices.map(function(exo) {
// 							var difficulty = GetTypeExo(exo, filePath)[1]
// 							if (difficulty !== '1' || difficulty !== '2' || difficulty !== '3') {
// 								// add this exercise to a file that stores all exercices where the difficulty is not specified
// 								fs.appendFileSync(__dirname  + '/tmp/exercices-sans-difficulte.txt', filePath + ':' + exo + '\n');
// 								// vscode.window.showInformationMessage('Exercice sans difficulté : ' + exo + ' dans ' + filePath);
// 							}
// 							// const exo_short = (exo.slice(0, 25) + "...").toString();
// 							return new TreeItem(exo, undefined, filePath, 'file');
// 						}),
// 						filePath,
// 						'chapter',
// 						undefined
// 					);
// 				}),
// 				undefined,
// 				'folder',
// 				undefined
// 			);
// 		});
//     }

// 	// define here the command to call when clicking on the tree items
// 	BanqueExoShow.prototype.getTreeItem = function (element) {
// 		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Collapsed);
// 		if (element.contextValue === 'file') {
// 			item.tooltip = "Voir l'exercice";
// 			item.command = {
// 				command: 'goto.exo',
// 				title: 'Ouvrir exercice',
// 				arguments: [element]
// 			}
// 		} 
// 		return item;
// 	};

//     BanqueExoShow.prototype.getChildren = function (element) {
//         if (element === undefined) {
//             return this.data;
//         }
//         return element.children;
//     };

// 	BanqueExoShow.prototype.resolveTreeItem = function (item) {
// 		item.tooltip = item.filePath;
// 		return item;
// 	};

//     return BanqueExoShow;
// }());

module.exports = ProgShow;
module.exports = BanqueExoShow;