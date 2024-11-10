"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const path = require('path');
const TreeItem = require('./treeItem');
// Object.defineProperty(exports, "__esModule", { value: true });

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

		// pdf du programme de colle
		var programme_colle_pdf = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Colles/PC/ -maxdepth 1 -type f -name "*_PC_Phy_colle.pdf"').toString().split('\n')[0];
		var programme_colle_pdf_basename = path.basename(programme_colle_pdf);
		this.data.push(new TreeItem(programme_colle_pdf_basename, undefined, programme_colle_pdf, 'pdf', undefined));

		// define the event when tree data change
		this._onDidChangeTreeData = new vscode.EventEmitter();
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
					command: 'banque.fetch',
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
	get onDidChangeTreeData() {
		return this._onDidChangeTreeData && this._onDidChangeTreeData.event;
	};

	refresh() {
		this._onDidChangeTreeData && this._onDidChangeTreeData.fire();
	};
};

module.exports = ProgShow;