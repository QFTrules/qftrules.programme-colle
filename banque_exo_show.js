"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const TreeItem = require('./treeItem');
// Object.defineProperty(exports, "__esModule", { value: true });
// import { DepNodeProvider, Dependency } from './treeview';

function GetTypeExo(label, filepath) {
	// filepath is undefined for items in programme de colle
	if (typeof filepath === 'undefined') {
		return ['undefined','undefined'];
	}
	
	// if no error, returns the info about the exercise
	const fileContent = fs.readFileSync(filepath, 'utf8');
	const lines = fileContent.split('\n');
	for (let i = 0; i < lines.length; i++) {
		if (lines[i].includes(label)) {
			// get the type of exercise (python, devoir, ...)
			var startIndex = lines[i].lastIndexOf('[') + 1;
			var endIndex = lines[i].lastIndexOf(']');
			const typeExo = lines[i].substring(startIndex, endIndex);
			// get the difficulty of the exercise (on, two, three stars)
			var startIndex = lines[i].indexOf('[', lines[i].indexOf('[') + 1) + 1;
			var endIndex = lines[i].indexOf(']', lines[i].indexOf(']') + 1);
			const difficulty = lines[i].substring(startIndex, endIndex);
			return [typeExo, difficulty];
			}
		}
		return ['undefined','undefined'];
	}

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
							var typeExo = GetTypeExo(exo, filePath)[0];
							var difficulty = GetTypeExo(exo, filePath)[1];
							if (difficulty !== '1' || difficulty !== '2' || difficulty !== '3') {
								// add this exercise to a file that stores all exercices where the difficulty is not specified
								// this will be used by the suggestions tree view panel
								fs.appendFileSync(__dirname  + '/tmp/exercices-sans-difficulte.txt', filePath + ':' + exo + '\n');
							}
							// // create a simple completion provider item
							// const completionItem = new vscode.CompletionItem(exo);
							// completionItem.insertText = exo;
							// completionItem.documentation = 'This is a sample completion item';
							// // register the completion item provider for latex language
							// vscode.languages.registerCompletionItemProvider({ language: 'latex' }, {
							// 	triggerCharacters: ['\\Ex{'],
							// 	provideCompletionItems() {
							// 		// vscode.commands.executeCommand('editor.action.triggerSuggest');
							// 		// return the completion item
							// 		return [completionItem];
							// 	}
							// });
							return new TreeItem(exo, undefined, filePath, 'file', undefined, typeExo, difficulty);
						}),
						filePath,
						'chapter'
					);
				}),
				undefined,
				'folder'
			);
		});
    }

	// define here the command to call when clicking on the tree items
	getTreeItem(element) {
		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Collapsed, element.typeExo, element.difficulty);
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

module.exports = BanqueExoShow;