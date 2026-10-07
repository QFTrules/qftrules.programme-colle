"use strict";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
var vscode = require('vscode');
var child_process = require('child_process');
const fs = require('fs');
const path = require('path');
const TreeItem = require('./treeItem');

function prettifyLatexLabel(label) {
	if (!label) return label;
	let out = String(label);
	// Remove math delimiters for display in tree label.
	out = out.replace(/\$/g, '');
	// Simple LaTeX -> unicode replacements for readability.
	const replacements = [
		[/\\alpha/g, 'α'], [/\\beta/g, 'β'], [/\\gamma/g, 'γ'], [/\\delta/g, 'δ'],
		[/\\epsilon/g, 'ε'], [/\\theta/g, 'θ'], [/\\lambda/g, 'λ'], [/\\mu/g, 'μ'],
		[/\\omega/g, 'ω'], [/\\Omega/g, 'Ω'], [/\\pi/g, 'π'], [/\\sigma/g, 'σ'],
		[/\\times/g, '×'], [/\\cdot/g, '·'], [/\\to/g, '→'], [/\\infty/g, '∞'],
		[/\\leq/g, '≤'], [/\\geq/g, '≥'], [/\\neq/g, '≠'], [/\\pm/g, '±'],
		[/\\approx/g, '≈'], [/\\Delta/g, 'Δ'], [/\\nabla/g, '∇']
	];
	for (const [re, sym] of replacements) {
		out = out.replace(re, sym);
	}
	// Flatten common wrappers.
	out = out.replace(/\\mathrm\{([^}]*)\}/g, '$1');
	out = out.replace(/\\text\{([^}]*)\}/g, '$1');
	out = out.replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, '($1)/($2)');
	out = out.replace(/[{}]/g, '');
	out = out.replace(/\s+/g, ' ').trim();
	return out;
}

function GetTypeExo(label, filepath) {
	// filepath is undefined for items in programme de colle
	if (typeof filepath === 'undefined') {
		return ['undefined','undefined'];
	}

	// if no error, returns the info about the exercise
	const fileContent = fs.readFileSync(filepath, 'utf8');
	const lines = fileContent.split('\n');
	for (let i = 0; i < lines.length; i++) {
		var line = lines[i];
		const m = line.match(/\\begin\{exo\}(?:\[([^\]]*)\])?(?:\[([^\]]*)\])?(?:\[([^\]]*)\])?\{([^}]*)\}/);
		if (m && m[4] === label) {
			// Signature in styles: [theme][difficulty][type]{label}
			const difficulty = (m[2] || '').trim();
			const typeExo = (m[3] || '').trim();
			return [typeExo, difficulty];
			}
		}
		return ['undefined','undefined'];
	}

// define data for the tree view
function generateTreeItems() {
	const startTime = Date.now();
	BanqueExoShow.log(`[START] generateTreeItems`);
	// list of themes
	const texPath = vscode.workspace.getConfiguration('mathpix-pdf').get('texPath');
	// list all folders in the recueil directory
	var themes_list = fs.readdirSync(texPath).filter(file => fs.statSync(path.join(texPath, file)).isDirectory());
	// list all folders in the recueil directory and remove the ones excluded
	const exclude = ['.vscode','Figure','Figures'];
	var themes_list = themes_list.filter(theme => !exclude.includes(theme));
	// exclude themes that start with an underscore
	themes_list = themes_list.filter(theme => !theme.startsWith('_'));

	const result = themes_list.map(function (theme) {
		const themeStart = Date.now();
		BanqueExoShow.log(`  [START] theme: ${theme}`);
		const folderPath = path.join(texPath, theme.trim(), '/');

		// get the list of latex files for the theme
		const findStart = Date.now();
		BanqueExoShow.log(`    [START] find files for ${theme}`);
		var latex_files = child_process.execSync('find ' + texPath  + theme + ' -maxdepth 1 -type f -name "*.tex"').toString().split('\n');
		BanqueExoShow.log(`    [END] find files: ${Date.now() - findStart}ms (${latex_files.length - 1} files)`);
		latex_files.pop();

		// remove the file that stores all exercices where the difficulty is not specified
		const suggestion_liste = __dirname + '/tmp/exercices-sans-difficulte.txt';
		if (fs.existsSync(suggestion_liste)) {
			fs.unlinkSync(suggestion_liste);
		}

		// return a tree item for each theme with lazy-loaded chapters
		const themeItem = new TreeItem(theme.toUpperCase(),
			latex_files.map(function (filePath) {
				const basename = path.parse(filePath).name;
				// Create chapter item WITHOUT exercises (lazy loading)
				return new TreeItem(basename, undefined, filePath, 'chapter',
					vscode.TreeItemCollapsibleState.Collapsed, undefined, undefined, basename, theme.toUpperCase());
			}),
			folderPath, 'folder', undefined, undefined, undefined, undefined, theme.toUpperCase());

		BanqueExoShow.log(`  [END] theme: ${Date.now() - themeStart}ms`);
		return themeItem;
	});

	// return data;
	BanqueExoShow.log(`[END] generateTreeItems: ${Date.now() - startTime}ms`);
	return result;
}

// define the data providers for the programme de colle panel
class BanqueExoShow {
	static sortMode = 'file';
	static outputChannel = null;
	static cache = {}; // filepath -> {mtime, exercises}

	static log(message) {
		if (BanqueExoShow.outputChannel) {
			BanqueExoShow.outputChannel.appendLine(message);
		}
		console.log(message);
	}

	static getExercises(filePath) {
		const stats = fs.statSync(filePath);
		const cached = BanqueExoShow.cache[filePath];

		if (cached && cached.mtime === stats.mtimeMs) {
			return cached.exercises;
		}

		const grepStart = Date.now();
		var exercices = child_process.execSync('grep -E "\\\\\\begin{exo}" ' + filePath.toString()).toString().split('\n');
		exercices.pop();
		BanqueExoShow.log(`      [grep] ${path.parse(filePath).name}: ${Date.now() - grepStart}ms (cached: ${!!cached})`);

		BanqueExoShow.cache[filePath] = { mtime: stats.mtimeMs, exercises: exercices };
		return exercices;
	}

	static loadExercises(chapterItem) {
		const filePath = chapterItem.filePath;
		const basename = chapterItem.label;
		const theme = chapterItem.theme;
		const suggestion_liste = __dirname + '/tmp/exercices-sans-difficulte.txt';

		const exerciceLines = BanqueExoShow.getExercises(filePath);

		return exerciceLines.map(function (exoLine) {
			const parsed = exoLine.match(/\\begin\{exo\}(?:\[([^\]]*)\])?(?:\[([^\]]*)\])?(?:\[([^\]]*)\])?\{([^}]*)\}/);
			const isCommented = /^\s*%/.test(exoLine);
			var exo = parsed ? parsed[4].trim() : '';
			const typeExo = parsed ? (parsed[3] || '').trim() : 'undefined';
			const difficulty = parsed ? (parsed[2] || '').trim() : 'undefined';

			if (!exo) {
				var start = exoLine.indexOf('{', exoLine.indexOf('{') + 1) + 1;
				var end = exoLine.indexOf('}', exoLine.indexOf('}') + 1);
				exo = exoLine.substring(start, end);
			}
			if (difficulty === '') {
				fs.appendFileSync(suggestion_liste, filePath + ':' + exo + '\n');
			}
			const displayExo = prettifyLatexLabel(exo);
			const exoItem = new TreeItem(displayExo, undefined, filePath, 'file', undefined, typeExo, difficulty, basename, theme, isCommented);
			exoItem.rawLabel = exo;
			return exoItem;
		});
	}

	static sortItems(items, mode) {
		const sortStart = Date.now();
		if (!items || items.length === 0) return items;
		const sorted = [...items];

		if (mode === 'alpha') {
			sorted.sort((a, b) => a.label.localeCompare(b.label));
		} else if (mode === 'type') {
			sorted.sort((a, b) => {
				const typeA = a.typeExo || 'undefined';
				const typeB = b.typeExo || 'undefined';
				return typeA.localeCompare(typeB);
			});
		} else if (mode === 'difficulty') {
			sorted.sort((a, b) => parseInt(b.difficulty || '0') - parseInt(a.difficulty || '0'));
		}

		BanqueExoShow.log(`sortItems(mode=${mode}, items=${items.length}): ${Date.now() - sortStart}ms`);
		return sorted;
	}

    constructor() {
		this.data = generateTreeItems();
    }

	// define here the command to call when clicking on the tree items
	getTreeItem(element) {
		var item = new TreeItem(element.label, element.children, element.filePath, element.contextValue, vscode.TreeItemCollapsibleState.Collapsed, element.typeExo, element.difficulty, element.chapter, element.theme, element.isCommented);
		item.rawLabel = element.rawLabel || element.label;
		if (element.contextValue === 'file') {
			item.tooltip = `Voir l'exercice (${element.typeExo || 'undefined'})`;
			item.command = {
				command: 'banque.fetch',
				title: 'Ouvrir exercice',
				arguments: [element],
			}
		}
		return item;
	};

    getChildren(element) {
        if (element === undefined) {
            return this.data;
        }

		// Lazy load exercises for chapters
		if (element.contextValue === 'chapter' && !element.children) {
			const loadStart = Date.now();
			BanqueExoShow.log(`  [LAZY] loading chapter ${element.label}...`);
			element.children = BanqueExoShow.loadExercises(element);
			BanqueExoShow.log(`  [LAZY] loaded ${element.children.length} exercises in ${Date.now() - loadStart}ms`);
		}

		// Apply sorting to exercise items
		if (element.contextValue === 'chapter' && element.children) {
			const sortStart = Date.now();
			const result = BanqueExoShow.sortItems(element.children, BanqueExoShow.sortMode);
			BanqueExoShow.log(`getChildren(${element.label}): ${Date.now() - sortStart}ms`);
			return result;
		}

        return element.children;
    };

	getParent(element) {
		// get the parent of the tree item with the given label
		const treeItems = this.data;
		for (let i = 0; i < treeItems.length; i++) {
			if (treeItems[i].label === element.label) {
				return undefined;
			}
			var parent1 = treeItems[i];
			for (let j = 0; j < parent1.children.length; j++) {
				if (parent1.children[j].label === element.label) {
					return parent1;
				}
				var parent2 = parent1.children[j];
				if (parent2.children) {
					for (let k = 0; k < parent2.children.length; k++) {
						if (parent2.children[k].label === element.label) {
							return parent2;
						}
					}
				}
			}
		}
	}

	getTreeItemByLabel(folderName,filename,label) {
		// get the tree item with the given label
		const treeItems = this.data;
		for (let i = 0; i < treeItems.length; i++) {
			if (folderName === 'undefined' || treeItems[i].label.trim() === folderName.toUpperCase().trim())  {
				var node1 = treeItems[i];
				for (let j = 0; j < node1.children.length; j++) {
					if (node1.children[j].label === filename) {
						var node2 = node1.children[j];
						// Load exercises if not already loaded
						if (!node2.children) {
							node2.children = BanqueExoShow.loadExercises(node2);
						}
						for (let k = 0; k < node2.children.length; k++) {
							const exoLabel = node2.children[k].rawLabel || node2.children[k].label;
							if (exoLabel === label) {
								return node2.children[k];
							}
						}
					}
				}
			}
		}
	}

	resolveTreeItem(item) {
		item.tooltip = item.filePath;
		return item;
	};
};

module.exports = BanqueExoShow
module.exports.GetTypeExo = GetTypeExo
