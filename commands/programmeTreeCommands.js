"use strict";

const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const child_process = require('child_process');

// Recursively find files under dir where testFn(entry.name) is true, sorted
function findTexFiles(dir, testFn) {
	if (!fs.existsSync(dir)) return [];
	let results = [];
	const entries = fs.readdirSync(dir, { withFileTypes: true });
	for (const entry of entries) {
		const fullPath = path.join(dir, entry.name);
		if (entry.isDirectory()) {
			results = results.concat(findTexFiles(fullPath, testFn));
		} else if (entry.isFile() && testFn(entry.name)) {
			results.push(fullPath);
		}
	}
	return results.sort();
}

// JS equivalent of build_programme_colle.sh
function buildProgrammeColle({ collePath, styPath, pythonCommand, cpgePath, mdPath, extensionPath }) {
	const tmpdir = path.join(extensionPath, 'tmp');
	const progColleBase = 'ProgrammeColle';
	const ProgColleFile = progColleBase + '.tex';
	const ProgCollePath = path.join(tmpdir, ProgColleFile);

	// Resolve a style directory that contains both required files.
	const configuredStyDir = String(styPath || '').trim();
	const candidateDirs = [
		configuredStyDir,
		path.join(extensionPath, 'templates'),
	].filter(Boolean);

	const resolvedStyDir = candidateDirs.find(dir => {
		return fs.existsSync(path.join(dir, 'progcolle.sty')) && fs.existsSync(path.join(dir, 'programme.tex'));
	});

	if (!resolvedStyDir) {
		throw new Error(
			`No valid style directory found. Checked: ${candidateDirs.join(', ')}. ` +
			`Expected both progcolle.sty and programme.tex.`
		);
	}

	const texStyDir = resolvedStyDir.replace(/\\/g, '/').replace(/\/?$/, '/');
	const fallbackStyDir = path.join(extensionPath, 'templates').replace(/\\/g, '/').replace(/\/?$/, '/');
	const texInputs = [texStyDir, fallbackStyDir].filter(Boolean).join(':') + ':' + (process.env.TEXINPUTS || '');

	// Write ProgrammeColle.tex header
	fs.writeFileSync(ProgCollePath, [
		`\\input{${texStyDir}progcolle.sty}%$`,
		`      \\input{${texStyDir}programme.tex}%$`,
		'      \\begin{document}',
		'      \\tableofcontents',
		'      ',
	].join('\n'));

	// Run Python parser on each matching file in a section
	function processSection(files, sectionMacro) {
		if (sectionMacro) {
			fs.appendFileSync(ProgCollePath, sectionMacro + '\n');
		}
		for (const fichier of files) {
			try {
				const content = fs.readFileSync(fichier, 'utf8');
				if (content.includes('\\ProgrammeColle')) {
					child_process.execSync(
						`${pythonCommand} "${path.join(extensionPath, 'build_programme_colle_java.py')}" "${fichier}" "${ProgCollePath}"`,
						{ cwd: tmpdir }
					);
				}
			} catch (e) { /* skip unreadable or failed files */ }
		}
	}

	// Find files for each section
	const coursFiles = findTexFiles(path.join(cpgePath, 'Cours'), name =>
		name.endsWith('.tex') && !name.includes('TD') && !name.includes('Fig') && !name.includes('Doc')
	);
	const tdFiles = findTexFiles(path.join(cpgePath, 'TD'), name =>
		name.includes('TD') && name.endsWith('.tex')
	);
	const dmFiles = findTexFiles(path.join(cpgePath, 'Devoirs', 'DM'), name => name.endsWith('.tex'));
	const dsFiles = findTexFiles(path.join(cpgePath, 'Devoirs', 'DS'), name => name.endsWith('.tex'));
	const tpFiles = findTexFiles(path.join(cpgePath, 'Devoirs', 'TP'), name => name.endsWith('.tex'));

	processSection(coursFiles, null);
	processSection(tdFiles, '\\TD');
	processSection(dmFiles, '\\DM');
	processSection(dsFiles, '\\DS');
	processSection(tpFiles, '\\TP');

	fs.appendFileSync(ProgCollePath, '\\end{document}\n');

	// Compile helper — runs from tmpdir; throws with log excerpt on failure
	const runPdflatex = (texFile) => {
		try {
			const texFullPath = path.join(tmpdir, texFile);
			child_process.execSync(
				`pdflatex -synctex=1 --shell-escape -interaction=nonstopmode "${texFullPath}"`,
				{
					cwd: tmpdir,
					stdio: 'pipe',
					env: {
						...process.env,
						TEXINPUTS: texInputs,
					},
				}
			);
		} catch (e) {
			// pdflatex exits non-zero on errors; read the .log for context
			const logFile = path.join(tmpdir, texFile.replace(/\.tex$/, '.log'));
			let logTail = '';
			if (fs.existsSync(logFile)) {
				const lines = fs.readFileSync(logFile, 'utf8').split('\n');
				logTail = lines.filter(l => l.startsWith('!')).slice(0, 5).join('\n') || lines.slice(-20).join('\n');
			}
			// Only throw if the PDF was not produced (non-zero exit on warnings is ok)
			const pdfOut = path.join(tmpdir, texFile.replace(/\.tex$/, '.pdf'));
			if (!fs.existsSync(pdfOut)) {
				throw new Error(`pdflatex failed for ${texFile}:\n${logTail}`);
			}
		}
	};

	// First pass: compile ProgrammeColle.tex twice to generate .toc
	runPdflatex(ProgColleFile);
	runPdflatex(ProgColleFile);

	// Calculate dates for the upcoming week (same formula as bash date arithmetic)
	const today = new Date();
	const isoDay = today.getDay() === 0 ? 7 : today.getDay(); // Mon=1 … Sun=7
	const nextMonday = new Date(today);
	nextMonday.setDate(today.getDate() + (8 - isoDay));
	const nextFriday = new Date(today);
	nextFriday.setDate(today.getDate() + (13 - isoDay));

	const pad = n => String(n).padStart(2, '0');
	const NextMonday = `${pad(nextMonday.getDate())}/${pad(nextMonday.getMonth() + 1)}/${nextMonday.getFullYear()}`;
	const NextFriday = `${pad(nextFriday.getDate())}/${pad(nextFriday.getMonth() + 1)}/${nextFriday.getFullYear()}`;
	const Filedate   = `${nextMonday.getFullYear()}_${pad(nextMonday.getMonth() + 1)}_${pad(nextMonday.getDate())}`;

	const pdfSuffix = '_PC_Phy_colle.pdf';
	const texSuffix = '_PC_Phy_colle.tex';
	const txxSuffix = '_PC_Phy_colle_ini.tex';

	// Create dated final tex (reads TOC, adds date header)
	const finalTexFile = Filedate + texSuffix;
	fs.writeFileSync(path.join(tmpdir, finalTexFile), [
		`\\input{${texStyDir}progcolle.sty}%$`,
		`      \\input{${texStyDir}programme.tex}%$`,
		`      \\newcommand{\\babel}[6]{`,
		`      \\begin{center}`,
		`      {\\Large\\textsc{Programme de colle de physique}}`,
		`      \\end{center}`,
		`      \\begin{center}`,
		`      {Semaine du lundi ${NextMonday} ~au vendredi ${NextFriday}}`,
		`      \\end{center}`,
		`      }`,
		`      \\begin{document}`,
		`      \\input{ProgrammeColle.toc}`,
		`      \\end{document}`,
	].join('\n'));

	// Second pass: compile dated tex twice
	runPdflatex(finalTexFile);
	runPdflatex(finalTexFile);

	// Remove aux files for dated tex
	for (const ext of ['.aux', '.log', '.out', '.synctex.gz']) {
		const f = path.join(tmpdir, Filedate + '_PC_Phy_colle' + ext);
		if (fs.existsSync(f)) try { fs.unlinkSync(f); } catch (e) {}
	}

	// Remove old colle files from collePath
	if (fs.existsSync(collePath)) {
		for (const f of fs.readdirSync(collePath)) {
			if (f.includes('_PC_Phy_colle')) {
				try { fs.unlinkSync(path.join(collePath, f)); } catch (e) {}
			}
		}
	}

	// Move output files to collePath
	fs.renameSync(ProgCollePath, path.join(collePath, Filedate + txxSuffix));
	const tocSrc = path.join(tmpdir, progColleBase + '.toc');
	if (fs.existsSync(tocSrc)) {
		fs.renameSync(tocSrc, path.join(collePath, progColleBase + '.toc'));
	}
	fs.renameSync(path.join(tmpdir, finalTexFile), path.join(collePath, finalTexFile));
	const finalPdfSrc = path.join(tmpdir, Filedate + pdfSuffix);
	if (!fs.existsSync(finalPdfSrc)) {
		const logFile = path.join(tmpdir, Filedate + '_PC_Phy_colle.log');
		let logTail = 'Log file not found.';
		if (fs.existsSync(logFile)) {
			const lines = fs.readFileSync(logFile, 'utf8').split('\n');
			logTail = lines.filter(l => l.startsWith('!')).slice(0, 5).join('\n') || lines.slice(-20).join('\n');
		}
		throw new Error(`pdflatex did not produce ${Filedate + pdfSuffix}.\n${logTail}`);
	}
	fs.renameSync(finalPdfSrc, path.join(collePath, Filedate + pdfSuffix));

	// Remove remaining ProgrammeColle.* temp files
	for (const ext of ['.aux', '.log', '.out', '.synctex.gz', '.pdf']) {
		const f = path.join(tmpdir, progColleBase + ext);
		if (fs.existsSync(f)) try { fs.unlinkSync(f); } catch (e) {}
	}

	// Write MD file for GitHub Pages
	const mdSuffix = '_PC_Phy_colle.md';
	const collePathFwd = collePath.replace(/\/?$/, '/');
	fs.writeFileSync(path.join(mdPath, Filedate + mdSuffix), [
		'---',
		'layout: document',
		'image: /assets/images/3.jpg',
		`lien: ${collePathFwd}${Filedate}${pdfSuffix}`,
		'student: ',
		`title: Semaine du lundi ${NextMonday} au vendredi ${NextFriday}`,
		'type: programme_colle',
		'corrige: ',
		'theme: ',
		'deadline: ',
		`semaine: ${NextMonday}`,
		'summary: ',
		'---',
	].join('\n'));

	return Filedate + pdfSuffix;
}

function registerProgrammeTreeCommands(context, options) {
	const {
		programmeBalise,
		collePath,
		styPath,
		pythonCommand,
		cpgePath,
		mdPath,
		programmeProvider,
	} = options;

	const collapse = vscode.commands.registerCommand('programme.collapse', () => {
		// Step-by-step collapse: repeatedly collapse one level on the focused tree.
		vscode.commands.executeCommand('workbench.view.extension.programme-colle');
		vscode.commands.executeCommand('list.collapse');
	});

	const programmePdf = vscode.commands.registerCommand('programme.pdf', function (document) {
		const pdfFile = document.filePath.replace(/\.[^/.]+$/, '.pdf');
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(pdfFile), { viewColumn: vscode.ViewColumn.Two });
	});

	const programmeMd = vscode.commands.registerCommand('programme.md', function (document) {
		const mdFile = document.filePath.replace(/\.[^/.]+$/, '.md');
		vscode.commands.executeCommand('vscode.open', vscode.Uri.file(mdFile), { viewColumn: vscode.ViewColumn.Two });
	});

	const remove = vscode.commands.registerCommand('programme.remove', function (document) {
		const text = fs.readFileSync(document.filePath, 'utf8');
		const escapedBalise = programmeBalise.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
		const baliseRegex = new RegExp(escapedBalise, 'gi');
		const updatedText = text.replace(baliseRegex, '');
		fs.writeFileSync(document.filePath, updatedText, 'utf8');
		vscode.commands.executeCommand('programme.refresh');
	});

	const uploading = vscode.commands.registerCommand('programme.uploading', function () {
		// empty function to change the icon when programme de colle uploading
	});

	const compile = vscode.commands.registerCommand('programme.compile', function () {
		try {
			const programmeColleFile = buildProgrammeColle({
				collePath,
				styPath,
				pythonCommand,
				cpgePath,
				mdPath,
				extensionPath: path.join(__dirname, '..'),
			});
			vscode.window.showInformationMessage(programmeColleFile + ' compile avec succes', { timeout: 1 });
			vscode.commands.executeCommand('vscode.open', vscode.Uri.file(path.join(collePath.trim(), programmeColleFile.trim())), { viewColumn: vscode.ViewColumn.Two });
		} catch (err) {
			vscode.window.showErrorMessage('programme.compile: ' + err.message);
		}
	});

	const refresh = vscode.commands.registerCommand('programme.refresh', () => {
		programmeProvider.refresh();
	});

	context.subscriptions.push(collapse, programmePdf, programmeMd, remove, uploading, compile, refresh);
}

module.exports = {
	registerProgrammeTreeCommands,
};
