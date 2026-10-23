const vscode = require('vscode');
const BanqueExoShow = require('../banque_exo_show');

class BanqueWebViewProvider {
	constructor(banqueProvider) {
		this.banqueProvider = banqueProvider;
		this._view = undefined;
		this._expandedItems = new Set();
		this._currentSearchQuery = '';
		this._exerciseMap = new Map(); // Map exercise index to exercise object
	}

	resolveWebviewView(webviewView, context, _token) {
		this._view = webviewView;
		webviewView.webview.options = {
			enableScripts: true,
			localResourceRoots: []
		};
		webviewView.webview.html = this.getHtmlContent();
		this.setWebviewMessageListener(webviewView.webview);

		// Initial render
		setTimeout(() => {
			this.updateTree();
		}, 100);
	}

	setWebviewMessageListener(webview) {
		webview.onDidReceiveMessage((message) => {
			console.log('[BanqueWebView] Received message from webview:', message.type);
			switch (message.type) {
				case 'search':
					console.log('[BanqueWebView] Search with query:', message.query);
					this.handleSearch(message.query);
					break;
				case 'toggleExpand':
					console.log('[BanqueWebView] Toggle expand:', message.itemId);
					this.toggleExpand(message.itemId);
					break;
				case 'openExercise':
					console.log('[BanqueWebView] Open exercise:', message.exerciseIndex);
					{
						const exercise = this.getExercise(message.exerciseIndex);
						if (exercise) {
							this.openExercise(exercise);
						}
					}
					break;
			}
		});
	}

	handleSearch(query) {
		console.log(`[BanqueWebView] Search triggered: "${query}"`);
		this._currentSearchQuery = query;
		this._expandedItems.clear();

		if (query.trim() === '') {
			this.banqueProvider.clearSearchResults();
		} else {
			const results = this.banqueProvider.searchExercises(query);
			this.banqueProvider.setSearchResults(results, query);
			// Auto-expand themes and chapters in search mode
			if (results.length > 0) {
				results.forEach(theme => {
					this._expandedItems.add(`theme-${theme.label}`);
					if (theme.children) {
						theme.children.forEach(chapter => {
							this._expandedItems.add(`chapter-${theme.label}-${chapter.label}`);
						});
					}
				});
			}
		}

		this.updateTree();
	}

	toggleExpand(itemId) {
		console.log(`[BanqueWebView] Toggle expand: ${itemId}`);
		if (this._expandedItems.has(itemId)) {
			this._expandedItems.delete(itemId);
		} else {
			this._expandedItems.add(itemId);
		}
		this.updateTree();
	}

	openExercise(exercise) {
		// Trigger the banque.fetch command
		vscode.commands.executeCommand('banque.fetch', exercise);
	}

	storeExercise(index, exercise) {
		this._exerciseMap.set(index.toString(), exercise);
	}

	getExercise(index) {
		return this._exerciseMap.get(index.toString());
	}

	updateTree() {
		if (!this._view) {
			console.warn('[BanqueWebView] View not yet initialized, retrying in 100ms');
			setTimeout(() => this.updateTree(), 100);
			return;
		}

		this._exerciseMap.clear(); // Clear old exercises
		const data = this.banqueProvider.isSearchMode
			? this.banqueProvider.searchResults
			: this.banqueProvider.data;

		const treeHtml = this.renderTree(data);
		try {
			this._view.webview.postMessage({
				type: 'updateTree',
				html: treeHtml,
				searchQuery: this._currentSearchQuery
			});
		} catch (error) {
			console.error('[BanqueWebView] Error posting message to webview:', error);
		}
	}

	renderTree(items) {
		if (!items || items.length === 0) {
			console.log('[BanqueWebView] renderTree: no items');
			return '<div class="empty-state">Aucun exercice trouvé</div>';
		}

		console.log('[BanqueWebView] renderTree: rendering', items.length, 'themes');
		let html = '<div class="tree-container">';
		let exerciseIndex = 0;
		items.forEach((theme, idx) => {
			console.log('[BanqueWebView] Rendering theme', idx, ':', theme.label, '- expanded:', this._expandedItems.has(`theme-${theme.label}`));
			const result = this.renderTheme(theme, exerciseIndex);
			html += result.html;
			exerciseIndex = result.nextIndex;
		});
		html += '</div>';
		return html;
	}

	renderTheme(theme, exerciseIndex) {
		const themeId = `theme-${theme.label}`;
		const isExpanded = this._expandedItems.has(themeId);
		let html = `
			<div class="tree-item theme-item">
				<div class="tree-item-content tree-toggle-btn" data-id="${themeId}" data-type="theme">
					<span class="tree-toggle ${isExpanded ? 'expanded' : ''}">▶</span>
					<span class="tree-icon">📚</span>
					<span class="tree-label">${this.escapeHtml(theme.label)}</span>
				</div>`;

		if (isExpanded && theme.children) {
			const result = this.renderChapters(theme, exerciseIndex);
			html += result.html;
			exerciseIndex = result.nextIndex;
		}

		html += '</div>';
		return { html, nextIndex: exerciseIndex };
	}

	renderChapters(theme, exerciseIndex) {
		if (!theme.children || theme.children.length === 0) return { html: '', nextIndex: exerciseIndex };

		let html = '<div class="tree-children visible">';
		theme.children.forEach(chapter => {
			const result = this.renderChapter(theme, chapter, exerciseIndex);
			html += result.html;
			exerciseIndex = result.nextIndex;
		});
		html += '</div>';
		return { html, nextIndex: exerciseIndex };
	}

	renderChapter(theme, chapter, exerciseIndex) {
		const chapterId = `chapter-${theme.label}-${chapter.label}`;
		const isExpanded = this._expandedItems.has(chapterId);

		// Lazy load exercises if not already loaded
		if (!chapter.children) {
			chapter.children = BanqueExoShow.loadExercises(chapter);
		}

		let html = `
			<div class="tree-item chapter-item">
				<div class="tree-item-content tree-toggle-btn" data-id="${chapterId}" data-type="chapter">
					<span class="tree-toggle ${isExpanded ? 'expanded' : ''}">▶</span>
					<span class="tree-icon">📖</span>
					<span class="tree-label">${this.escapeHtml(chapter.label)}</span>
				</div>`;

		if (isExpanded && chapter.children) {
			const result = this.renderExercises(chapter, exerciseIndex);
			html += result.html;
			exerciseIndex = result.nextIndex;
		}

		html += '</div>';
		return { html, nextIndex: exerciseIndex };
	}

	renderExercises(chapter, exerciseIndex) {
		if (!chapter.children || chapter.children.length === 0) return { html: '', nextIndex: exerciseIndex };

		let html = '<div class="tree-children visible">';
		chapter.children.forEach(exercise => {
			const result = this.renderExercise(exercise, exerciseIndex);
			html += result.html;
			exerciseIndex = result.nextIndex;
		});
		html += '</div>';
		return { html, nextIndex: exerciseIndex };
	}

	renderExercise(exercise, exerciseIndex) {
		this.storeExercise(exerciseIndex, exercise);
		return {
			html: `
				<div class="tree-item exercise-item">
					<div class="tree-item-content exercise-btn" data-exercise-index="${exerciseIndex}">
						<span class="tree-icon">📄</span>
						<span class="tree-label exercise-label">${this.escapeHtml(exercise.label)}</span>
					</div>
				</div>
			`,
			nextIndex: exerciseIndex + 1
		};
	}

	escapeHtml(text) {
		const map = {
			'&': '&amp;',
			'<': '&lt;',
			'>': '&gt;',
			'"': '&quot;',
			"'": '&#039;'
		};
		return text.replace(/[&<>"']/g, m => map[m]);
	}

	getHtmlContent() {
		return `<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Banque d'Exercices</title>
	<style>
		* {
			margin: 0;
			padding: 0;
			box-sizing: border-box;
		}

		body {
			font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
			background-color: var(--vscode-editor-background);
			color: var(--vscode-editor-foreground);
			font-size: 13px;
			overflow: hidden;
			display: flex;
			flex-direction: column;
			height: 100vh;
		}

		.search-container {
			display: flex;
			align-items: center;
			gap: 8px;
			padding: 8px;
			border-bottom: 1px solid var(--vscode-panel-border);
			background-color: var(--vscode-sideBar-background);
			flex-shrink: 0;
		}

		.search-input {
			flex: 1;
			padding: 6px 8px;
			border: 1px solid var(--vscode-input-border, #555);
			border-radius: 2px;
			background-color: var(--vscode-input-background);
			color: var(--vscode-input-foreground);
			font-size: 13px;
		}

		.search-input::placeholder {
			color: var(--vscode-input-placeholderForeground);
		}

		.search-input:focus {
			outline: none;
			border-color: var(--vscode-focusBorder);
			box-shadow: 0 0 0 1px var(--vscode-focusBorder);
		}

		.filter-btn {
			padding: 4px 8px;
			border: 1px solid transparent;
			background-color: transparent;
			color: var(--vscode-editor-foreground);
			cursor: pointer;
			border-radius: 2px;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		.filter-btn:hover {
			background-color: var(--vscode-button-hoverBackground);
		}

		.tree-container {
			flex: 1;
			overflow-y: auto;
			overflow-x: hidden;
			padding: 4px 0;
		}

		.tree-item {
			user-select: none;
		}

		.tree-item-content {
			display: flex;
			align-items: center;
			padding: 2px 8px;
			cursor: pointer;
			white-space: nowrap;
		}

		.tree-item-content:hover {
			background-color: var(--vscode-list-hoverBackground);
		}

		.tree-toggle {
			display: inline-block;
			width: 16px;
			text-align: center;
			margin-right: 2px;
			transition: transform 0.1s;
			color: var(--vscode-icon-foreground);
		}

		.tree-toggle.expanded {
			transform: rotate(90deg);
		}

		.tree-icon {
			margin-right: 4px;
			display: inline-block;
			width: 16px;
			height: 16px;
			line-height: 16px;
		}

		.tree-label {
			overflow: hidden;
			text-overflow: ellipsis;
		}

		.theme-item {
			margin-left: 0;
		}

		.theme-item .tree-item-content {
			font-weight: 500;
			color: var(--vscode-editor-foreground);
		}

		.chapter-item {
			margin-left: 16px;
		}

		.exercise-item {
			margin-left: 32px;
		}

		.exercise-item .tree-item-content {
			padding-left: 24px;
			color: var(--vscode-descriptionForeground);
		}

		.exercise-item .tree-item-content:hover {
			color: var(--vscode-editor-foreground);
		}

		.tree-children {
			display: none;
		}

		.tree-children.visible {
			display: block;
		}

		.empty-state {
			padding: 20px;
			text-align: center;
			color: var(--vscode-descriptionForeground);
		}

		/* Scrollbar styling */
		.tree-container::-webkit-scrollbar {
			width: 10px;
		}

		.tree-container::-webkit-scrollbar-track {
			background: transparent;
		}

		.tree-container::-webkit-scrollbar-thumb {
			background: var(--vscode-scrollbarSlider-background);
			border-radius: 4px;
		}

		.tree-container::-webkit-scrollbar-thumb:hover {
			background: var(--vscode-scrollbarSlider-hoverBackground);
		}
	</style>
</head>
<body>
	<div class="search-container">
		<input
			type="text"
			id="searchInput"
			class="search-input"
			placeholder="Filter (e.g. text, !exclude, @tag)"
		/>
		<button id="filterBtn" class="filter-btn" title="Filter Options">
			🔽
		</button>
	</div>
	<div id="treeContent" class="tree-container"></div>

	<script>
		const vscode = acquireVsCodeApi();
		const searchInput = document.getElementById('searchInput');
		const treeContent = document.getElementById('treeContent');
		let searchTimeout;
		let currentTreeData = [];

		// Handle search input
		searchInput.addEventListener('input', (e) => {
			clearTimeout(searchTimeout);
			searchTimeout = setTimeout(() => {
				console.log('[WebView] Search input:', e.target.value);
				vscode.postMessage({
					type: 'search',
					query: e.target.value
				});
			}, 300);
		});

		// Handle messages from extension
		window.addEventListener('message', event => {
			const message = event.data;
			console.log('[WebView] Received message:', message.type);
			if (message.type === 'updateTree') {
				console.log('[WebView] Updating tree with', message.html.length, 'bytes');
				treeContent.innerHTML = message.html;
				searchInput.value = message.searchQuery;
				if (message.searchQuery && message.searchQuery.trim()) {
					searchInput.focus();
				}
				// Re-attach click handlers for dynamically created elements
				attachEventListeners();
			}
		});

		function attachEventListeners() {
			console.log('[WebView] Attaching event listeners...');

			// Attach toggle event listeners
			const toggleBtns = document.querySelectorAll('.tree-toggle-btn');
			console.log('[WebView] Found', toggleBtns.length, 'toggle buttons');

			toggleBtns.forEach((el, idx) => {
				el.addEventListener('click', (e) => {
					e.stopPropagation();
					const itemId = el.getAttribute('data-id');
					console.log('[WebView] Toggle clicked:', itemId);
					vscode.postMessage({
						type: 'toggleExpand',
						itemId: itemId
					});
				});
			});

			// Attach exercise click listeners
			const exerciseBtns = document.querySelectorAll('.exercise-btn');
			console.log('[WebView] Found', exerciseBtns.length, 'exercise buttons');

			exerciseBtns.forEach(el => {
				el.addEventListener('click', (e) => {
					e.stopPropagation();
					const index = el.getAttribute('data-exercise-index');
					console.log('[WebView] Exercise clicked:', index);
					vscode.postMessage({
						type: 'openExercise',
						exerciseIndex: index
					});
				});
			});
		}

		// Focus on search input when view loads
		setTimeout(() => {
			console.log('[WebView] Initial load - focusing search input');
			searchInput.focus();
			attachEventListeners();
		}, 100);
	</script>
</body>
</html>`;
	}
}

module.exports = BanqueWebViewProvider;
