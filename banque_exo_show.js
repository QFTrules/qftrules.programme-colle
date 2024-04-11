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

// define data for the tree view
function generateTreeItems() {
	// list of themes
	const texPath = vscode.workspace.getConfiguration('mathpix-pdf').get('texPath');
	// const path_to_recueil = vscode.workspace.getConfiguration('banque-exercices').get("RecueilPath");
	// list all folders in the recueil directory
	const themes_list = fs.readdirSync(texPath).filter(file => fs.statSync(path.join(texPath, file)).isDirectory());
	// vscode.window.showInformationMessage('Liste des thèmes : ' + themes_list);
	// remove folders Figure, _fiches, etc.
	themes_list.splice(themes_list.indexOf('Figure'), 1);
	themes_list.splice(themes_list.indexOf('_fiches'), 1);
	themes_list.splice(themes_list.indexOf('Oraux'), 1);
	themes_list.splice(themes_list.indexOf('.git'), 1);
	themes_list.splice(themes_list.indexOf('Info'), 1);
	// vscode.window.showInformationMessage('Liste des thèmes : ' + themes_list);
	// const themes_list = [
	// 	'Mecanique',
	// 	'Thermo',
	// 	'Optique',
	// 	'Fluide',
	// 	'Ondes',
	// 	'Quantique'
	// ];

	const data = themes_list.map(function (theme) {
		// get the list of latex files for the theme 
		// vscode.window.showInformationMessage(theme);
		// vscode.window.showInformationMessage('find ' + texPath + theme + ' -maxdepth 1 -type f -name "*.tex"');
		var latex_files = child_process.execSync('find ' + texPath  + theme + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n');
		latex_files.pop();

		// remove the file that stores all exercices where the difficulty is not specified
		const suggestion_liste = __dirname + '/tmp/exercices-sans-difficulte.txt';
		if (fs.existsSync(suggestion_liste)) {
			fs.unlinkSync(suggestion_liste);
		}

		// return a tree item for each theme
		return new TreeItem(theme.toUpperCase(),
			latex_files.map(function (filePath) {
				var exercices = child_process.execSync('grep -E "\\\\\\\\begin{exo}" ' + filePath).toString().split('\n');
				exercices.pop();
				const basename = path.parse(filePath).name

				return new TreeItem(basename,
					exercices.map(function (exo) {
						var start = exo.indexOf('{', exo.indexOf('{') + 1) + 1;
						var end = exo.indexOf('}', exo.indexOf('}') + 1);
						var exo = exo.substring(start, end);
						var typeExo = GetTypeExo(exo, filePath)[0];
						var difficulty = GetTypeExo(exo, filePath)[1];
						if (difficulty === '') {
							// add this exercise to a file that stores all exercices where the difficulty is not specified
							// this will be used by the suggestions tree view panel
							fs.appendFileSync(suggestion_liste, filePath + ':' + exo + '\n');
						}
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

	return data;
}

// refresh suggestions at extension activation
// function suggestions_refresh() {
// 	// list of themes
// 	const themes_list = [
// 		'Thermo',
// 		'Fluide',
// 		'Ondes',
// 		'Optique',
// 		'Mecanique',
// 	]

// 	themes_list.forEach(function(theme) {
// 	// get the list of latex files for the theme 
// 	var latex_files = child_process.execSync('find ~/Dropbox/CPGE/Physique/Exercices/Recueil/' + theme + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n');
// 	latex_files.pop()

// 	// try to remove the file exercices-sans-difficulte.txt, pass if already removed
// 	try {
// 		fs.unlinkSync(__dirname + '/tmp/exercices-sans-difficulte.txt');
// 	} catch (error) {
// 			// pass
// 		}

// 	// look for all chapters in each theme
// 	latex_files.forEach(function(chapter) {
// 			// fetch all exercise names in latex file basename
// 			var exercices = child_process.execSync('grep -E "\\\\\\\\begin{exo}" ' + chapter).toString().split('\n');
// 			exercices.pop();
// 			exercices.forEach(function(exo) {
// 					var start = exo.indexOf('{', exo.indexOf('{') + 1) + 1;
// 					var end = exo.indexOf('}', exo.indexOf('}') + 1);
// 					var exo =  exo.substring(start, end);
// 					// look if the difficulty is defined for each exercise
// 					// var typeExo = GetTypeExo(exo, filePath)[0];
// 					var difficulty = GetTypeExo(exo, chapter)[1];
// 					if (difficulty === '') {
// 							fs.appendFileSync(__dirname  + '/tmp/exercices-sans-difficulte.txt', chapter + ':' + exo + '\n');
// 						}
// 					});
// 				});
// 			});
// 		}

// define the data providers for the programme de colle panel
class BanqueExoShow {
    constructor() {
		
		// event emitter
		// this.onDidChangeTreeData = new vscode.EventEmitter();

		// Get the active text editor
		var editor = vscode.window.activeTextEditor;
		if (!editor) {
			return;
		}

		// Generate tree data
		this.data = generateTreeItems();
		
    }

	// define here the command to call when clicking on the tree items
	getTreeItem(element) {
		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Collapsed, element.typeExo, element.difficulty);
		if (element.contextValue === 'file') {
			item.tooltip = "Voir l'exercice";
			item.command = {
				command: 'banque.fetch',
				title: 'Ouvrir exercice',
				arguments: [element],
			}
		} 
		// if (element.contextValue === 'chapter') {
		// 	item.tooltip = "Ouvrir fichier latex";
		// 	item.command = {
		// 		command: 'vscode.open',
		// 		title: 'Ouvrir fichier latex',
		// 		arguments: [element.filePath],
		// 	}
		// } 
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

	// to refresh tree elements of the programme de colle
	// get onDidChangeTreeData() {
	// 	return this._onDidChangeTreeData && this._onDidChangeTreeData.event;
	// };

	// refresh() {
	// 	// update the data in your tree view
	// 	this.data = generateTreeItems();
	// 	// return this.data
	// 	// fire the event
	// 	// this.onDidChangeTreeData.fire();
	// };
};

module.exports = BanqueExoShow
	