"use strict";

const vscode = require('vscode');
const BanqueExoShow = require('../banque_exo_show');

function registerBanqueTreeCommands(context, options = {}) {
	const banqueProvider = options.banqueProvider;

	const banqueRefresh = vscode.commands.registerCommand('banque.refresh', () => {
		if (banqueProvider) {
			// Refresh the existing provider without losing search state
			banqueProvider.refresh();
		}
	});

	const banqueCollapse = vscode.commands.registerCommand('banque.collapse', () => {
		// Collapse all items in the tree view recursively
		vscode.commands.executeCommand('workbench.view.extension.banque-exercices');
		vscode.commands.executeCommand('list.collapseAll');
	});

	context.subscriptions.push(banqueRefresh, banqueCollapse);
}

module.exports = {
	registerBanqueTreeCommands,
};
