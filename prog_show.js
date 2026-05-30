"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const path = require('path');
const TreeItem = require('./treeItem');
const cpgePath = vscode.workspace.getConfiguration('programme-colle').get('cpgePath');
const collePath = vscode.workspace.getConfiguration('programme-colle').get('collePath');
const mdPath = vscode.workspace.getConfiguration('programme-colle').get('mdPath');
// Object.defineProperty(exports, "__esModule", { value: true });

// define the data providers for the programme de colle panel
class ProgShow {
    constructor() {
		this._onDidChangeTreeData = new vscode.EventEmitter();
		this.data = this.buildData();
    }

	buildData() {
		const extensionDir = __dirname;
		const output = child_process.execSync('bash ' + extensionDir + '/show_programme_colle_java.sh ' + cpgePath).toString();
		const words = output.split(':');
		words.shift();
		const type_colle = words.filter((_, index) => index % 2 === 0);
		const type_doc = ['Cours', 'TD', 'DM', 'DS', 'TP'];
		const list_doc = type_doc.map(function() {
			return [];
		});

		for (let j = 0; j < type_colle.length; j++) {
			const block = words[2 * j + 1] || '';
			const documents = block.trim().split(',');
			if (documents.length !== 1) {
				for (let i = 0; i < documents.length - 1; i++) {
					const filePath = documents[i].trim();
					if (filePath.length > 0) {
						list_doc[j] = [...list_doc[j], filePath];
					}
				}
			}
		}

		const data = type_doc.map(function(basename, i) {
			return new TreeItem(basename,
				list_doc[i].map(function(filePath) {
					const filename = path.basename(filePath).toString();
					return new TreeItem(filename, undefined, filePath, 'latex', undefined);
				})
			);
		});

		const programme_colle_pdf = child_process.execSync('find ' + collePath + ' -maxdepth 1 -type f -name "*_PC_Phy_colle.pdf"').toString().split('\n')[0];
		if (programme_colle_pdf) {
			const programme_colle_pdf_basename = path.basename(programme_colle_pdf);
			data.push(new TreeItem(programme_colle_pdf_basename, undefined, programme_colle_pdf, 'pdf', undefined));
		}

		const programme_colle_md = child_process.execSync('find ' + mdPath + ' -maxdepth 1 -type f -name "*_PC_Phy_colle.md"').toString().split('\n')[0];
		if (programme_colle_md) {
			const programme_colle_md_basename = path.basename(programme_colle_md);
			data.push(new TreeItem(programme_colle_md_basename, undefined, programme_colle_md, 'md', undefined));
		}

		return data;
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
				item.tooltip = "Ouvrir tex";
				item.command = {
					command: 'vscode.open',
					arguments: [vscode.Uri.file(element.filePath), { viewColumn: vscode.ViewColumn.One }]
				};
			} else if (element.contextValue === 'md') {
				item.tooltip = "Ouvrir markdown";
				item.command = {
					command: 'vscode.open',
					arguments: [vscode.Uri.file(element.filePath), { viewColumn: vscode.ViewColumn.Beside }]
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
		this.data = this.buildData();
		this._onDidChangeTreeData && this._onDidChangeTreeData.fire();
	};
};

module.exports = ProgShow;