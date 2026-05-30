"use strict";

const vscode = require('vscode');
const BanqueExoShow = require('../banque_exo_show');

function registerBanqueTreeCommands(context) {
	const banqueRefresh = vscode.commands.registerCommand('banque.refresh', () => {
		vscode.commands.executeCommand('workbench.action.files.saveAll').then(() => {
			vscode.window.registerTreeDataProvider('banque-exercices', new BanqueExoShow());
		});
	});

	const banqueCollapse = vscode.commands.registerCommand('banque.collapse', () => {
		// Step-by-step collapse: repeatedly collapse one level on the focused tree.
		vscode.commands.executeCommand('workbench.view.extension.banque-exercices');
		vscode.commands.executeCommand('list.collapse');
	});

	context.subscriptions.push(banqueRefresh, banqueCollapse);
}

module.exports = {
	registerBanqueTreeCommands,
};
