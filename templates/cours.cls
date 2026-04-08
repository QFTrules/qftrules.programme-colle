%%%%%%%%%%%%%%%%%%%%%%
%% start of file `elegantbook.cls'.
%% Copyright 2013-2021 ElegantLaTeX (elegantlatex2e@gmail.com)
%%
%% This work may be distributed and/or modified freely
%% available at https://github.com/ElegantLaTeX/ElegantBook
%
%%%%%%%%%%%%%%%%%%%%%
% % !Mode:: "TeX:UTF-8"
% !TEX encoding = UTF-8 Unicode


\NeedsTeXFormat{LaTeX2e}
% \ProvidesClass{/home/eb/Dropbox/texmf/tex/latex/Preambles/cours}[2021/05/02 v4.1 ElegantBook document class]%$
\ProvidesClass{cours}[2021/05/02 v4.1 ElegantBook document class]%$
\RequirePackage{kvoptions}
\RequirePackage{etoolbox}
\RequirePackage{thmtools}
\SetupKeyvalOptions{family=ELEGANT, prefix=ELEGANT@, setkeys=\kvsetkeys}
\newcommand{\ekv}[1]{\kvsetkeys{ELEGANT}{#1}}

% ----- Colors -----
\DeclareStringOption[blue]{color}
\DeclareStringOption[en]{lang}
\DeclareStringOption[answer]{result}
\DeclareStringOption[fancy]{mode}
\DeclareStringOption[normal]{device}
\DeclareStringOption[cm]{math}
\DeclareStringOption[marginfalse]{marginpar}
\DeclareStringOption[onecol]{toc}
\DeclareStringOption{scheme}
% ----- backward compatibility
\DeclareVoidOption{green}{\ekv{color=green}}
\DeclareVoidOption{cyan}{\ekv{color=cyan}}
\DeclareVoidOption{blue}{\ekv{color=blue}}
\DeclareVoidOption{gray}{\ekv{color=gray}}
\DeclareVoidOption{black}{\ekv{color=black}}
\DeclareVoidOption{nocolor}{\ekv{color=none}}
\DeclareStringOption[ctexfont]{chinesefont}

\DeclareVoidOption{chinese}{\ekv{scheme=chinese}}

\DeclareVoidOption{ctexfont}{\ekv{chinesefont=ctexfont}}
\DeclareVoidOption{founder}{\ekv{chinesefont=founder}}
\DeclareVoidOption{nofont}{\ekv{chinesefont=nofont}}

\DeclareVoidOption{en}{\ekv{lang=en}}
\DeclareVoidOption{cn}{\ekv{lang=cn}}
\DeclareVoidOption{it}{\ekv{lang=it}}

\DeclareVoidOption{fancy}{\ekv{mode=fancy}}
\DeclareVoidOption{simple}{\ekv{mode=simple}}

\DeclareVoidOption{answer}{\ekv{result=answer}}
\DeclareVoidOption{noanswer}{\ekv{result=noanswer}}

\DeclareVoidOption{normal}{\ekv{device=normal}}
\DeclareVoidOption{pad}{\ekv{device=pad}}

\DeclareStringOption[numeric-comp]{citestyle}
\DeclareStringOption[numeric]{bibstyle}


\DeclareVoidOption{newtx}{\ekv{math=newtx}}
\DeclareVoidOption{mtpro2}{\ekv{math=mtpro2}}
\DeclareVoidOption{cm}{\ekv{math=cm}}

\DeclareVoidOption{margintrue}{\ekv{marginpar=margintrue}}
\DeclareVoidOption{marginfalse}{\ekv{marginpar=marginfalse}}


\DeclareVoidOption{onecol}{\ekv{toc=onecol}}
\DeclareVoidOption{twocol}{\ekv{toc=twocol}}


% ----- Math option -----
\newcommand\mailto[1]{\href{mailto:#1}{\nolinkurl{#1}}}

% ----- Title Style -----
\DeclareStringOption[hang]{titlestyle}[hang]
% ----- backward compatibility
\DeclareVoidOption{hang}{\ekv{titlestyle=hang}}
\DeclareVoidOption{display}{\ekv{titlestyle=display}}
% ----- Default Options -----
\DeclareDefaultOption{\PassOptionsToClass{\CurrentOption}{book}}

\ProcessKeyvalOptions*\relax
% \ProcessOptions*\relax
\LoadClass[a4paper,oneside]{book}

% \RequirePackage{setspace}

\RequirePackage{csquotes}


%%% TABLE OF CONTENTS %%%
\usepackage{minitoc}
\mtcsettitle{minitoc}{}
\setcounter{minitocdepth}{3}
\newcommand{\filterminitoc}[1]{#1}
% \renewcommand{\chaptername}{\Large\textsc{Chapitre}~M\thechapter}
\renewcommand{\thesection}{\csname filterminitoc \endcsname{\arabic{chapter}.}\arabic{section}}
\newcommand{\minitocsection}{\begingroup\renewcommand{\filterminitoc}[1]{}\minitoc\endgroup}






\RequirePackage{hyperref}
\hypersetup{
  breaklinks,
  unicode,
  linktoc=all,
  bookmarksnumbered=true,
  bookmarksopen=true,
  pdfkeywords={ElegantBook},
  colorlinks,
  linkcolor=coolblack,
  citecolor=coolblack,
  urlcolor=coolblack,
  % winered
  plainpages=false,
  pdfstartview=FitH,
  pdfborder={0 0 0},
  linktocpage
  }
  
  % ifthenelse
  \RequirePackage{xstring}
  \RequirePackage{xifthen}

  %% device settings
  \RequirePackage{geometry}
  \ifdefstring{\ELEGANT@device}{normal}{
    \geometry{
      a4paper,
      top=25.4mm, bottom=25.4mm,
      left=15mm, right=15mm,
      headheight=2.17cm,
      headsep=4mm,
      footskip=12mm
      }
      \ifdefstring{\ELEGANT@marginpar}{margintrue}{
        \geometry{
      marginparwidth=5cm, marginparsep=5mm,
      left=2cm,right=7cm}}{\relax}}{
    \relax}

\ifdefstring{\ELEGANT@device}{pad}{
\geometry{
  paperwidth=7.5in,
  paperheight=10in,
  margin=16mm,
  headheight=2.17cm,
  footskip=4mm
}}{\relax}

\RequirePackage{indentfirst,comment}
% fontsetting
\ifdefstring{\ELEGANT@math}{mtpro2}{
  \let\Bbbk\relax
  \RequirePackage[lite]{mtpro2}
}{\relax}

\setcounter{tocdepth}{1}
\renewcommand{\baselinestretch}{1.2}

\PassOptionsToPackage{no-math}{fontspec}
\RequirePackage{iftex}
\ifdefstring{\ELEGANT@lang}{cn}{
  \ifXeTeX
    \ifdefstring{\ELEGANT@chinesefont}{founder}{
      \RequirePackage[UTF8,scheme=plain,fontset=none]{ctex}
      \setCJKmainfont[BoldFont={FZHei-B01},ItalicFont={FZKai-Z03}]{FZShuSong-Z01}
      \setCJKsansfont[BoldFont={FZHei-B01},ItalicFont={FZHei-B01}]{FZHei-B01}
      \setCJKmonofont[BoldFont={FZHei-B01},ItalicFont={FZHei-B01}]{FZFangSong-Z02}
      \setCJKfamilyfont{zhsong}{FZShuSong-Z01}
      \setCJKfamilyfont{zhhei}{FZHei-B01}
      \setCJKfamilyfont{zhkai}{FZKai-Z03}
      \setCJKfamilyfont{zhfs}{FZFangSong-Z02}
      \newcommand*{\songti}{\CJKfamily{zhsong}}
      \newcommand*{\heiti}{\CJKfamily{zhhei}}
      \newcommand*{\kaishu}{\CJKfamily{zhkai}}
      \newcommand*{\fangsong}{\CJKfamily{zhfs}}}{\relax}

    \ifdefstring{\ELEGANT@chinesefont}{nofont}{
      \RequirePackage[UTF8,scheme=plain,fontset=none]{ctex}}{\relax}

    \ifdefstring{\ELEGANT@chinesefont}{ctexfont}{
      \RequirePackage[UTF8,scheme=plain]{ctex}}{\relax}
  \else
    \ifdefstring{\ELEGANT@chinesefont}{ctexfont}{
      \RequirePackage[UTF8,scheme=plain]{ctex}}{\relax}
  \fi
  \AfterEndPreamble{
    % \renewcommand{\itshape}{\kaishu}
    \setlength\parindent{2\ccwd}}
}{\relax}

\ifcsname heiti\endcsname
  \newcommand{\cbfseries}{\heiti}
\else
  \newcommand{\cbfseries}{\bfseries}
\fi


\ifcsname kaishu\endcsname
  \newcommand{\citshape}{\kaishu}
\else
  \newcommand{\citshape}{\itshape}
\fi
\ifcsname kaishu\endcsname
  \newcommand{\cnormal}{\kaishu}
\else
  \newcommand{\cnormal}{\normalfont}
\fi

\ifcsname fangsong\endcsname
  \newcommand{\cfs}{\fangsong}
\else
  \newcommand{\cfs}{\normalfont}
\fi

\RequirePackage{newtxtext}
\RequirePackage{anyfontsize}
\ifdefstring{\ELEGANT@math}{newtx}{
  \RequirePackage{newtxmath}
  \let\Bbbk\relax
  \RequirePackage{esint}
  %%% use yhmath pkg, uncomment following code
  % \let\oldwidering\widering
  % \let\widering\undefined
  % \RequirePackage{yhmath}
  % \let\widering\oldwidering

  %%% use esvect pkg, uncomment following code
  %\RequirePackage{esvect}

  \DeclareSymbolFont{CMlargesymbols}{OMX}{cmex}{m}{n}
  \let\sumop\relax\let\prodop\relax
  \DeclareMathSymbol{\sumop}{\mathop}{CMlargesymbols}{"50}
  \DeclareMathSymbol{\prodop}{\mathop}{CMlargesymbols}{"51}
}{\relax}

% ----- Handle Colors -----
%% 章节以及页脚图形

\RequirePackage[table,dvipsnames]{xcolor}
\ifdefstring{\ELEGANT@color}{green}{
  \definecolor{structurecolor}{RGB}{0,120,2}%
  \definecolor{main}{RGB}{0,120,2}%
  \definecolor{second}{RGB}{230,90,7}%
  \definecolor{third}{RGB}{0,160,152}%
}{\relax}
\ifdefstring{\ELEGANT@color}{cyan}{
  \definecolor{structurecolor}{RGB}{31,186,190}%
  \definecolor{main}{RGB}{59,180,5}%
  \definecolor{second}{RGB}{175,153,8}%
  \definecolor{third}{RGB}{244,105,102}%
}{\relax}
\ifdefstring{\ELEGANT@color}{blue}{
  \definecolor{structurecolor}{RGB}{60,113,183}
  \definecolor{main}{RGB}{0,166,82}%
  \definecolor{second}{RGB}{255,134,24}%
  \definecolor{third}{RGB}{0,174,247}%
}{\relax}
\ifdefstring{\ELEGANT@color}{gray}{
  \definecolor{structurecolor}{RGB}{150,150,150}
  \definecolor{main}{RGB}{150,150,150}%
  \definecolor{second}{RGB}{150,150,150}%
  \definecolor{third}{RGB}{150,150,150}%
}{\relax}
\ifdefstring{\ELEGANT@color}{black}{
  \definecolor{structurecolor}{RGB}{0,0,0}
  \definecolor{main}{RGB}{0,0,0}%
  \definecolor{second}{RGB}{0,0,0}%
  \definecolor{third}{RGB}{0,0,0}%
}{\relax}

%green color
\definecolor{structure1}{RGB}{0,120,2}%
\definecolor{main1}{RGB}{0,120,2}%
\definecolor{second1}{RGB}{230,90,7}%
\definecolor{third1}{RGB}{0,160,152}%
%cyan color
\definecolor{structure2}{RGB}{31,186,190}%
\definecolor{main2}{RGB}{59,180,5}%
\definecolor{second2}{RGB}{175,153,8}%
\definecolor{third2}{RGB}{244,105,102}%
%blue color
\definecolor{structure3}{RGB}{60,113,183}
\definecolor{main3}{RGB}{0,166,82}%
\definecolor{second3}{RGB}{255,134,24}%
\definecolor{third3}{RGB}{0,174,247}%
% gray color
\definecolor{structure4}{RGB}{150,150,150}
\definecolor{main4}{RGB}{150,150,150}%
\definecolor{second4}{RGB}{150,150,150}%
\definecolor{third4}{RGB}{150,150,150}%
% black color
\definecolor{structure5}{RGB}{0,0,0}
\definecolor{main5}{RGB}{0,0,0}%
\definecolor{second5}{RGB}{0,0,0}%
\definecolor{third5}{RGB}{0,0,0}%

% corlor definition
\definecolor{winered}{rgb}{0.5,0,0}
\definecolor{bule}{RGB}{18,29,57}
\colorlet{coverlinecolor}{second}


% ----- Title Style -----
\ifdefstring{\ELEGANT@titlestyle}{hang}{\def\style{hang}}{\relax}
\ifdefstring{\ELEGANT@titlestyle}{display}{\def\style{display}}{\relax}

% reference:
% https://tex.stackexchange.com/questions/58506/how-to-make-a-new-command-similar-to-author
% https://pastebin.com/C8W4axzV
\newcommand\email[1]{\href{mailto:#1}{\nolinkurl{#1}}}

\global\let\@title\@empty
\global\let\@author\@empty
\global\let\@date\@empty
\newcommand{\subtitle}[1]{\gdef\@subtitle{#1}}
\newcommand{\institute}[1]{\gdef\@institute{#1}}
\newcommand{\version}[1]{\gdef\@version{#1}}
\newcommand{\extrainfo}[1]{\gdef\@extrainfo{#1}}

\RequirePackage{mwe}
\newcommand{\logo}[1]{\gdef\@logo{#1}}
\newcommand{\cover}[1]{\gdef\@cover{#1}}

%\newcommand{\question}[1]{{\par\citshape #1}\\[0.2ex]}

\RequirePackage{enumerate}
% list/itemize/enumerate setting
\RequirePackage[shortlabels,inline]{enumitem}
\setlist{nolistsep}

\RequirePackage[labelfont={bf,color=structurecolor}]{caption}
\captionsetup[table]{skip=3pt}
\captionsetup[figure]{skip=3pt}

\AtBeginDocument{
  \setlength{\abovedisplayskip}{3pt}
  \setlength{\belowdisplayskip}{3pt}
  \RequirePackage[flushmargin,stable]{footmisc}
  \setlength{\footnotesep}{12pt}
}



\RequirePackage{graphicx}
%\RequirePackage{enumerate}
\RequirePackage{amsmath,mathrsfs,amsfonts,amssymb}
% \providecommand\qed{}
% \renewcommand{\qed}{\hfill\ensuremath{\square}}
\RequirePackage{booktabs}
\RequirePackage{multicol,multirow}

\RequirePackage{fancyvrb}
\RequirePackage{makecell,lipsum,hologo}
%%中文结构名字

% BIBTEX NOT NECESSARY %
% \RequirePackage[
  % backend=biber,
  % citestyle=\ELEGANT@citestyle,
  % bibstyle=\ELEGANT@bibstyle]{biblatex}




%%   章节设置

\RequirePackage{appendix}

\ifdefstring{\ELEGANT@lang}{en}{
  \setlength\parindent{2em}
  \newcommand\figref[1]{\textbf{Figure}~\ref{#1}}
  \newcommand\tabref[1]{\textbf{Tableau}~\ref{#1}}
  % \renewcommand{\chaptername}{\Large\textsc{Chapitre} \thechapter}
  % \renewcommand{\chaptername}{\Large\textsc{Chapitre}~M}
  \renewcommand{\partname}{\color{structurecolor} Part}
  \newcommand{\authorname}{
  %\textbf{Auteur: }
  }
  \newcommand{\institutename}{
  %\textbf{Institut: }
  }
  \newcommand{\datename}{
  %\textbf{Date: }
  }
  \newcommand{\versionname}{Version~: }
  \newcommand{\notename}{Méthode}
  \newcommand{\proofname}{Preuve}
  \newcommand{\problemname}{Probl\`eme}
  \newcommand{\definitionname}{D\'efinition}
  \newcommand{\theoremname}{Formule}
  \newcommand{\axiomname}{Méthode}
  \newcommand{\postulatename}{\faFlask~Expérience}
  \newcommand{\lemmaname}{Lemme}
  \newcommand{\propname}{Propri\'et\'e}
  \newcommand{\propositionname}{Proposition}
  \newcommand{\corollaryname}{Corollaire}
  \newcommand{\examplename}{%
    % {\color{third}\hspace{-0.8cm}\faPen}%
    % \faPen~Exemple}
    \faPencil*~Exemple}
  \newcommand{\exercisename}{Exercice}
  \newcommand{\remarkname}{Remarque}
  \newcommand{\assumptionname}{Hypoth\`ese}
  \newcommand{\conclusionname}{Conclusion}
  \newcommand{\solutionname}{Solution}
  \newcommand{\propertyname}{Propri\'et\'e}
  \newcommand{\introductionname}{Introduction}
  \renewcommand{\appendixname}{Appendice}
  % \newcommand{\problemsetname}{Exercise}
  \newcommand\bioinfo[2]{\gdef\@bioinfo{\textbf{#1}: #2}}
  \newcommand{\updatename}{Updates:}
  \newcommand{\historyname}{Version History}
}{\relax}

% PERSO PARAGRAPH
\renewcommand{\theparagraph}{{\color{structurecolor}\hspace*{1em}(\roman{paragraph})}\hspace*{-0.7em}}
\newcommand{\parag}[1]{
\paragraph{{\color{structurecolor}#1}~---$\!\!\!\!$}}

% ---------------------------------
% PATHS
% ---------------------------------
%\makeatletter
%\def\input@path{{./figures/}{./Figure/}{./Figures/}}
%\makeatother
\graphicspath{{./figure/}{./Figures/}{./figures/}{./image/}{./images/}{./graphics/}{./graphic/}{./pictures/}{./picture/}{../../Covers/}{../Covers/}}

\RequirePackage{tikz} %% load tikz without tikz
\usetikzlibrary{angles, quotes}
\usetikzlibrary{backgrounds,calc,shadows,positioning,fit}
\newcommand*\circled[1]{\tikz[baseline=(char.base)]{
            \node[shape=circle,draw,inner sep=1pt] (char) {#1};}}
%  https://tex.stackexchange.com/questions/7032/good-way-to-make-textcircled-numbers

\newcommand*{\eitemi}{\tikz \draw [baseline, ball color=structurecolor,draw=none] circle (2pt);}
\newcommand*{\eitemii}{\tikz \draw [baseline, fill=structurecolor,draw=none,circular drop shadow] circle (2pt);}
\newcommand*{\eitemiii}{\tikz \draw [baseline, fill=structurecolor,draw=none] circle (2pt);}
% \setlist[enumerate,1]{label=\color{structurecolor}\arabic*.}
% \setlist[enumerate,2]{label=\color{structurecolor}(\alph*).}
% \setlist[enumerate,3]{label=\color{structurecolor}\Roman*.}
% \setlist[enumerate,4]{label=\color{structurecolor}\Alph*.}
% \setlist[itemize,1]{label={\eitemi}}
% \setlist[itemize,2]{label={\eitemii}}
% \setlist[itemize,3]{label={\eitemiii}}


\RequirePackage[center,pagestyles]{titlesec}
\RequirePackage{apptools}
\setcounter{secnumdepth}{5}


\def\ColorStructure{structurecolor}

%%% CHAPTER %%%
% \renewcommand{\thechapter}{\arabic{chapter}}
\renewcommand{\thepart}{\ThemeLetter{\arabic{part}}}
\renewcommand{\thechapter}{{\thepart\arabic{chapter}}}
\titlespacing{\chapter}{0pt}{-20pt}{1.3\baselineskip}
\titleformat{\chapter}[\style]{\bfseries}{
  %\filcenter
  %\LARGE
  %\enspace
  % \color{\ColorStructure} \IfAppendix{\appendixname\;\thechapter}{\chaptername\;\thechapter}\;
  \formatchapter
  }{1pt}{
  \formatchaptertitle
  %\LARGE\color{\ColorStructure}%\filcenter
  }[]

\newcommand{\formatchaptertitle}[1]{%
  %\parbox[t]{\dimexpr\textwidth-10pt}{
  \raggedright\LARGE\color{\ColorStructure}\scshape#1}
  %}
\newcommand{\formatchapter}[1]{%
  %\parbox[t]{120pt}{
  \LARGE\color{\ColorStructure}\IfAppendix{\appendixname\;\thechapter}{\chaptername\;\thechapter}\;#1}
  %}
  %}
\newcommand{\formatsection}[1]{%
  %\parbox[t]{120pt}{
  \LARGE\color{\ColorStructure}\IfAppendix{\appendixname\;\thesection}{\sectionname\;\thesection}\;#1}
  %}

  

%%% SECTION %%%
\renewcommand{\thesection}{\Roman{section}}
\titleformat{\section}[hang]{\bfseries}{
  \Large\bfseries{\color{\ColorStructure}\thesection~$-$}~}{1pt}{%
  \color{\ColorStructure}\Large\bfseries\filright}

%%% SUBSECTION %%%
\renewcommand{\thesubsection}{\thesection.\Alph{subsection}}
\titleformat{\subsection}[hang]{\bfseries}{
  ~~~~~~
  \large\bfseries\color{\ColorStructure}\thesubsection~$-$~}{1pt}{%
  \color{\ColorStructure}\large\bfseries\filright}


%%% SUBSUBSECTION %%%
\titleformat{\subsubsection}[hang]{\bfseries}{
  \large\bfseries\color{\ColorStructure}\thesubsubsection\enspace}{1pt}{%
  \color{\ColorStructure}\large\bfseries\filright}

%\titlespacing{\subsection}{0pt}{0.5\baselineskip}{-\baselineskip}




%%% TCOLORBOX %%%
\RequirePackage{pifont,manfnt,bbding}
\RequirePackage[skins,many]{tcolorbox}
% \newlength{\normalparindent}
% \setlength{\normalparindent}{\parindent}
\ifdefstring{\ELEGANT@mode}{fancy}{
  \tcbset{
    common/.style={
      fontupper=\citshape,
      lower separated=false,
      % before upper={\setlength{\parindent}{\normalparindent}},
      coltitle=white,
      colback=gray!1,
      boxrule=0.5pt,
      fonttitle=\bfseries,
      enhanced,
      breakable,
      top=8pt,
      before skip=8pt,
      attach boxed title to top left={
        yshift=-0.11in,
        xshift=0.15in},
      boxed title style={
        boxrule=0pt,
        colframe=white,
        arc=0pt,
        outer arc=0pt},
      separator sign={.},},
    regular/.style={
      fontupper=\normalfont,
      lower separated=false,
      % before upper={\setlength{\parindent}{\normalparindent}},
      coltitle=white,
      colback=gray!1,
      boxrule=0.5pt,
      fonttitle=\bfseries,
      enhanced,
      breakable,
      top=8pt,
      before skip=8pt,
      attach boxed title to top left={
        yshift=-0.11in,
        xshift=0.15in},
      boxed title style={
        boxrule=0pt,
        colframe=white,
        arc=0pt,
        outer arc=0pt},
      separator sign={.},},
    defstyle/.style={
      common,
      colframe=main,
      colback=main!1,
      colbacktitle=main!70,
      overlay unbroken and last={
        \node[anchor=south east, outer sep=0pt] at (\linewidth-width,0) {
          \textcolor{main}{
          %$\clubsuit$
          }};}},
    thmstyle/.style={
      common,
      colframe=second,
      colback=second!1,
      colbacktitle=second!70,
      overlay unbroken and last={
        \node[anchor=south east, outer sep=0pt] at (\linewidth-width,0) {
          \textcolor{second}{
          %$\heartsuit$
          }};}},
    propstyle/.style={
      regular,
      % boxed title style={
      %   boxrule=1pt,
      %   colframe=third,
      %   arc=5pt,
      %   outer arc=5pt},
      colframe=third,
      colback=third!1,
      % coltitle=black,
      % fonttitle=\normalfont,
      fonttitle=\bfseries,
      colbacktitle=third!70!gray!70,
      overlay unbroken and last={
        \node[anchor=east, outer sep=0pt] at (0,height) {
          \textcolor{third}{
          % $\spadesuit$
          }};}},}
  % \newtcbtheorem[auto counter,number within=chapter]{definition}{\definitionname}{defstyle}{def}
  \DeclareTColorBox[auto counter,number within=chapter]{definition}{ o t\label g }{
    common,defstyle,
    IfValueTF={#1}{title={\definitionname~\thetcbcounter\ (#1)}}{title=\definitionname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}
  % \newtcbtheorem[auto counter,number within=chapter]{theorem}{\theoremname}{thmstyle}{thm}
  \DeclareTColorBox[auto counter,number within=chapter]{theorem}{ o t\label g }{
    common,
    %thmstyle,
    defstyle,
    IfValueTF={#1}{title={\theoremname~\thetcbcounter\ (#1)}}{title=\theoremname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}
    \DeclareTColorBox[auto counter,number within=chapter]{prop}{ o t\label g }{
    common,
    %propstyle,
    defstyle,
    IfValueTF={#1}{title={\propname~\thetcbcounter\ (#1)}}{title=\propname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}
  % \newtcbtheorem[auto counter,number within=chapter]{postulate}{\postulatename}{thmstyle}{pos}


  % METHODE
  \DeclareTColorBox[auto counter,number within=chapter]{axiom}{ o t\label g }{
    common,
    thmstyle,
    IfValueTF={#1}{title={\axiomname~\thetcbcounter\ (#1)}}{title=\axiomname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}
  % \newtcbtheorem[auto counter,number within=chapter]{corollary}{\corollaryname}{thmstyle}{cor}

  % EXPERIENCE
  \DeclareTColorBox[auto counter,number within=chapter]{postulate}{ o t\label g }{
  common,
  propstyle,
  IfValueTF={#1}{title={\postulatename~\thetcbcounter~: #1}}{title=\postulatename~\thetcbcounter},
  IfBooleanTF={#2}{label=#3}{}}
  % \newtcbtheorem[auto counter,number within=chapter]{axiom}{\axiomname}{thmstyle}{axi}

  % EXEMPLE
  \DeclareTColorBox[auto counter,number within=chapter]{example}{ o t\label g }{
    regular,
    propstyle,
    IfValueTF={#1}{title={{\bfseries \examplename~\thetcbcounter\ }: #1}}{title=\examplename~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}

  \DeclareTColorBox[auto counter,number within=chapter]{corollary}{ o t\label g }{
    common,thmstyle,
    IfValueTF={#1}{title={\corollaryname~\thetcbcounter\ (#1)}}{title=\corollaryname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}
  % \newtcbtheorem[auto counter,number within=chapter]{lemma}{\lemmaname}{thmstyle}{lem}
  \DeclareTColorBox[auto counter,number within=chapter]{lemma}{ o t\label g }{
    common,thmstyle,
    IfValueTF={#1}{title={\lemmaname~\thetcbcounter\ (#1)}}{title=\lemmaname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}
  % \newtcbtheorem[auto counter,number within=chapter]{proposition}{\propositionname}{propstyle}{pro}
  \DeclareTColorBox[auto counter,number within=chapter]{proposition}{ o t\label g }{
    common,propstyle,
    IfValueTF={#1}{title={\propositionname~\thetcbcounter\ (#1)}}{title=\propositionname~\thetcbcounter},
    IfBooleanTF={#2}{label=#3}{}}}{\relax}


\ifdefstring{\ELEGANT@mode}{simple}{
  \let\openbox\relax
  \RequirePackage{amsthm}
  \let\proof\relax
  % \let\proofname\relax
  \let\endproof\relax

  % declare a new theorem style
  \newtheoremstyle{defstyle}{3pt}{3pt}{\citshape}{-3pt}{
      \bfseries\color{main}}{}{0.5em}{\thmname{#1} \thmnumber{#2} \thmnote{(#3)}}
  \newtheoremstyle{thmstyle}{3pt}{3pt}{\citshape}{-3pt}{
    \bfseries\color{second}}{}{0.5em}{\thmname{#1} \thmnumber{#2} \thmnote{(#3)}}
  \newtheoremstyle{prostyle}{3pt}{3pt}{\citshape}{-3pt}{
    \bfseries\color{third}}{}{0.5em}{\thmname{#1} \thmnumber{#2} \thmnote{(#3)}}


  \theoremstyle{defstyle} % definition style
  \newtheorem{definition}{\definitionname}[chapter]

  \theoremstyle{thmstyle} %theorem style
  \newtheorem{theorem}{\theoremname}[chapter]
  \newtheorem{note}{\notename}[chapter]
  \newtheorem{corollary}{\corollaryname}[chapter]
  \newtheorem{postulate}{\postulatename}[chapter]
  \newtheorem{methode}{\axiomname}[chapter]



  \theoremstyle{prostyle} % proposition style
  \newtheorem{proposition}{\propositionname}[chapter]
}{\relax}

% main（green-def): example exercise problem solution
% second（orange-thm）: proof note remark
% third（blue-prop):  assumptions property conclusion custom

%% Example with counter
% \newcounter{exam}[chapter]
% \setcounter{exam}{0}
% \renewcommand{\theexam}{\thechapter.\arabic{exam}}
% \newenvironment{example}[1][]{
%   \refstepcounter{exam}
%   \par\noindent\textbf{\color{main}{\examplename} \theexam #1 }\rmfamily}{
%   \par\ignorespacesafterend}

%% Exercise with counter
\newcounter{exer}[chapter]
\setcounter{exer}{0}
\renewcommand{\theexer}{\thechapter.\arabic{exer}}
\newenvironment{exercise}[1][]{
  \refstepcounter{exer}
  \par\noindent\makebox[-3pt][r]{
    \scriptsize\color{red!90}\HandPencilLeft\quad}
    \textbf{\color{main}{\exercisename} \theexer #1 }\rmfamily}{
    \par\ignorespacesafterend}

%% Problem with counter
\newcounter{prob}[chapter]
\setcounter{prob}{0}
\renewcommand{\theprob}{\thechapter.\arabic{prob}}
\newenvironment{problem}[1][]{
  \refstepcounter{prob}
  \par\noindent\textbf{\color{main}{\problemname} \theprob #1 }\rmfamily}{
  \par\ignorespacesafterend}

\newenvironment{note}{
  \par\noindent\makebox[-3pt][r]{
    \scriptsize\color{red!90}\textdbend\quad}
    \textbf{\color{second}\notename} \citshape}{\par}

\newenvironment{proof}{
  \par\noindent\textbf{\color{second}\proofname\;}
  \color{black!90}\cfs}{
  % \hfill$\Box$\quad
  \par}

\newenvironment{solution}{\par\noindent\textbf{\color{main}\solutionname} \citshape}{\par}
\newenvironment{remark}{\noindent\textbf{\color{second}\remarkname}}{\par}
\newenvironment{assumption}{\par\noindent\textbf{\color{third}\assumptionname} \citshape}{\par}
\newenvironment{conclusion}{\par\noindent\textbf{\color{third}\conclusionname} \citshape}{\par}
\newenvironment{property}{\par\noindent\textbf{\color{third}\propertyname} \citshape}{\par}
\newenvironment{custom}[1]{\par\noindent\textbf{\color{third} #1} \citshape}{\par}

\RequirePackage{multicol}
\tcbset{
  introductionsty/.style={
    enhanced,
    breakable,
    colback=structurecolor!10,
    colframe=structurecolor,
    fonttitle=\bfseries,
    colbacktitle=structurecolor,
    fontupper=\citshape,
    attach boxed title to top center={yshift=-3mm,yshifttext=-1mm},
    boxrule=0pt,
    toprule=0.5pt,
    bottomrule=0.5pt,
    top=8pt,
    before skip=8pt,
    sharp corners
  },
}

\newenvironment{introduction}[1][\introductionname]{
  \begin{tcolorbox}[introductionsty,title={#1}]
    \begin{multicols}{2}
      \begin{itemize}[label=\textcolor{structurecolor}{\upshape\scriptsize\SquareShadowBottomRight}]}{
      \end{itemize}
    \end{multicols}
  \end{tcolorbox}}

%%% FORMULA ENVERONMENT %%%
\newenvironment{formula}[1]
{
%\def\lab{{\MakeLowercase{#1}}}
\begin{theorem}[#1]
\vspace{-0.2cm}
\begin{equation}
\label{eq:#1}
}
{
\end{equation}
\end{theorem}
}

\RequirePackage{adforn}

\newenvironment{problemset}[1][\chaptername~\;\exercisename]{
  \begin{center}
    \phantomsection\addcontentsline{toc}{section}{\texorpdfstring{\chaptername\;\exercisename}{\exercisename}}
    % \markboth{#1}{\rightmark}
    \markright{#1}
    \textcolor{structurecolor}{\Large\bfseries\adftripleflourishleft~#1~\adftripleflourishright}
  \end{center}
  \begin{enumerate}}{
  \end{enumerate}}

\def\relsec{\endgroup start}
\def\endrelsec{end\begingroup\def \@currenvir {relsec}}

\ifdefstring{\ELEGANT@result}{noanswer}{
  \AtBeginDocument{
  \excludecomment{solution}
  \excludecomment{proof}
  \excludecomment{inline}
  }
}{\relax}


%%% HEADINGS %%%
\RequirePackage{fancyhdr}
\RequirePackage{tabularx}
%\usepackage{lastpage}
\fancyhf{}
\fancyfoot[c]{\color{black}\small\thepage%/\pageref{LastPage}
}							% page numbering
%\if@twoside
%  \fancyhead[EL]{\color{black}\cnormal\leftmark}
%  \fancyhead[OR]{\color{black}\cnormal\rightmark}
%\else
  \fancyhead[R]{\small\color{black}\cnormal\rightmark}
  \fancyhead[C]{\small\color{black}\@subtitle}
    \fancyhead[L]{\small\color{black}Eric Brillaux}
%\fi
\renewcommand{\headrule}{\color{black}\hrule width\textwidth}
\pagestyle{fancy}
\renewcommand{\headrulewidth}{1pt}
% \renewcommand{\headrule}{}
\fancypagestyle{plain}{\renewcommand{\headrulewidth}{0pt}\fancyhf{}\renewcommand{\headrule}{}}
\renewcommand{\sectionmark}[1]{\markright{\color{black}\thesection\, #1}{}}
\renewcommand{\chaptermark}[1]{
%\markboth{\color{black}\chaptername\, #1}{}
%\protect\parbox{0.9\linewidth}{\chaptername\, #1}
}

\lhead{\small PC Th\'eophile Gautier}
\chead{\small \theyears}
\rhead{\small Eric Brillaux}

%%% TITRE DE PAGE %%%

% student version commands
% \cover{full_blank.png}
\def\courstopspace{-0.5cm}
\def\blueribbon{0in}
% \def\courstopspace{0pt}
% \def\blueribbon{0.5in}
% \newcommand{\pcsi}[1]{}
% \newcommand{\PrintProgramme}{}
\newcommand{\PrintProgramme}{
  {\large\bfseries\textcolor{\ColorStructure}{Programme officiel}}
  % \vspace{-0.5cm}
  \begin{center}
    % \includegraphics[width=\textwidth,height=9cm,keepaspectratio]{programme}
    {\footnotesize
    \input{prog.tex}
    }
    \vspace{0.5cm}
  \end{center}
  }

% prérequis de pcsi
\newcommand{\pcsi}[1]{
  \if\relax\detokenize{#1}\relax\else
  {\large\bfseries\textcolor{\ColorStructure}{Prérequis de PCSI}}
  \begin{liste}
    #1
  \end{liste}
  \vspace{0cm}\fi
  }

% prérequis
\newcommand{\prerequis}[2][]{
  \if\relax\detokenize{#2}\relax\else
  {\large\bfseries\textcolor{\ColorStructure}
  % \StrLen{#1}[\mystringlen]%
  % \ifthenelse{\mystringlen > 0}{Prérequis de #1}
  {  Prérequis  }
  }
  \begin{liste}
    #2
  \end{liste}
  \vspace{0cm}\fi
  }

\newcommand{\expliste}{
  {\large\bfseries\textcolor{\ColorStructure}{Expériences}}
  \listofdefinitions
}

\newcommand{\maketitre}[3][***]{%
\dominitoc
\hypersetup{pageanchor=false}
\pagenumbering{alph}
\begin{titlepage}
  \newgeometry{margin = 0in}
  \parindent=0pt
  \ifdefstring{\ELEGANT@device}{normal}{
    \ifcsname @cover\endcsname
      \includegraphics[width=\linewidth]{\@cover}
      % \includegraphics[trim=0 5cm 0 5cm,clip, width=\linewidth]{\@cover}
    \else
      \includegraphics[width=\linewidth]{example-image}
    \fi
  }{\relax}
  \ifdefstring{\ELEGANT@device}{pad}{
    \ifcsname @cover\endcsname
      \includegraphics[trim=0 5cm 0 5cm,clip=true, width=\linewidth]{\@cover}
    \else
      \includegraphics[trim=0 26bp 0 26bp,clip=true, width=\linewidth]{example-image}
    \fi
  }{\relax}
  \setlength{\fboxsep}{0pt}
  \colorbox{structurecolor}{\makebox[\linewidth][c]{\shortstack[c]{\vspace{\blueribbon}}}}
  \vfill
  \hspace{2em}
  \vspace{\courstopspace}
  \parbox{0.8\textwidth}{
    \bfseries\Huge%\scshape
      \ifcsname @title\endcsname \@title \fi
    \par}
  \vfill
  % \vspace{-1cm}
  % \vspace{-0.5cm}
  \setstretch{2.5}
  \hspace{1.75em}
  \begin{minipage}[c]{0.95\linewidth}
    {\color{darkgray}\bfseries
      \ifcsname @subtitle\endcsname\chapter{:~\textsc{\Large\@subtitle}}~\\[-10ex]\fi}
      % \vspace{-1.5cm}
      \vspace{-0.5cm}
    \begin{minipage}[l]{0.3\linewidth}
    {\color{gray}\normalsize\renewcommand{\arraystretch}{0.55}
    \begin{tabular}{l}
      \ifx\@author\empty\else\authorname\cnormal\@author\\ \fi
      \ifcsname @institute\endcsname \institutename \cnormal\@institute\\ \fi
      \ifx\@date\empty\else\datename\cnormal\@date \\ \fi
      \ifcsname @version\endcsname \cnormal\versionname\@version\\ \fi
      \ifcsname @bioinfo\endcsname \cnormal\@bioinfo\\ \fi
    \end{tabular}}
      \end{minipage}
    \begin{minipage}[r]{0.68\linewidth}
    \setlength{\baselineskip}{20pt}
    \ifthenelse{\equal{#1}{\string *}}{\prerequis{#3}}{
      \ifthenelse{\equal{#1}{\string **}}{\pcsi{#3}}{
        \ifthenelse{\equal{#1}{\string ***}}{\pcsi{#3}}{}
      }
      }
    % \ifthenelse{\equal{#1}{\string }}{}{\prerequis{#3}}
    \end{minipage}
    % \begin{minipage}[r]{0.68\linewidth}
    %   \expliste
    %   \end{minipage}
  \end{minipage}
  \begin{center}
    \setstretch{1}
    \parbox[t]{0.7\textwidth}{\centering \citshape
      \ifcsname @extrainfo\endcsname\@extrainfo\fi}
  \end{center}
  \setstretch{1}
  \begin{center}
  \begin{minipage}{0.8\textwidth}
  \ifthenelse{\equal{#1}{\string ***}}{\PrintProgramme\vspace{-2cm}}{}%{#1}
    \setcounter{tocdepth}{-2}
    \renewcommand{\contentsname}{}
    \tableofcontents
   	{\large\bfseries\textcolor{\ColorStructure}{Sommaire}}\\[-0.5cm]
    \begin{justify}
    {#2}
    \end{justify}
    \minitoc
  \end{minipage}
  \end{center}
  \vfill
\end{titlepage}
\restoregeometry

\mainmatter
}


\newcommand{\dollar}{\mbox{\textdollar}}

\RequirePackage{listings}
\renewcommand{\ttdefault}{cmtt}
\lstdefinestyle{mystyle}{
  basicstyle=%
    \ttfamily
    \lst@ifdisplaystyle\small\fi
}

\lstset{basicstyle=\ttfamily,style=mystyle,breaklines=true}

\definecolor{lightgrey}{rgb}{0.9,0.9,0.9}
\definecolor{frenchplum}{RGB}{190,20,83}
\lstset{language=[LaTeX]TeX,
  texcsstyle=*\color{winered},
  numbers=none,
  mathescape=false,
  breaklines=true,
  keywordstyle=\color{winered},
  commentstyle=\color{gray},
  emph={elegantpaper,fontenc,fontspec,xeCJK,citestyle,FiraMono,xunicode,newtxmath,figure,fig,image,img,table,itemize,enumerate,newtxtext,newtxtt,ctex,microtype,description,times,booktabs,tabular,PDFLaTeX,XeLaTeX,type1cm,BibTeX,device,color,mode,lang,amsthm,tcolorbox,titlestyle,cite,ctex,listings,base,math,scheme,toc,esint,chinesefont,amsmath,bibstyle,natbib,pgfornament},
  emphstyle={\color{frenchplum}},
  morekeywords={DeclareSymbolFont,SetSymbolFont,toprule,midrule,bottomrule,institute,version,includegraphics,setmainfont,setsansfont,setmonofont ,setCJKmainfont,setCJKsansfont,setCJKmonofont,RequirePackage,figref,tabref,email,maketitle,keywords,definecolor,extrainfo,logo,cover,subtitle,appendix,chapter,hypersetup,mainmatter,frontmatter,tableofcontents,elegantpar,heiti,kaishu,lstset,pagecolor,zhnumber,marginpar,part,equote,marginnote,bioinfo,datechange,listofchange,lvert,lastpage,songti,heiti,fangsong,setCJKfamilyfont,textbf},
  frame=single,
  tabsize=2,
  rulecolor=\color{structurecolor},
  framerule=0.2pt,
  columns=flexible,
  % backgroundcolor=\color{lightgrey}
}

\newcommand\bmmax{0}
\RequirePackage{bm}

% add the list of change history
\newcommand{\dateinfoline}[2]{
  \noindent\makebox[0pt][r]{%
  \makebox[-3em][r]{%
    \small
    \textbf{\textcolor{structurecolor}{#1}}}\;\;}%
  {\citshape\updatename\ignorespaces#2}}

\newcommand{\datechange}[2]{%
  \noindent{\makebox[\textwidth][r]{\color{structurecolor}\rule{1.15\textwidth}{.4pt}}}
  \dateinfoline{#1}{#2}
  \addcontentsline{dates}{section}{#1 -- #2}}

\newcommand{\listofchanges}{%
  \begingroup
    \renewcommand{\contentsname}{\historyname}
    \let\old@starttoc\@starttoc
    \def\@starttoc##1{
      \old@starttoc{dates}}
    \tableofcontents%
  \endgroup}
% https://tex.stackexchange.com/questions/472931/list-of-all-dates-in-a-document

\newenvironment{change}{
  \begin{enumerate}[label=\small\protect\circled{\arabic*}]}{
  \end{enumerate}}

% \addbibresource[location=local]{reference.bib}

\renewcommand\tableofcontents{%
  \hypersetup{linktoc=all, linkcolor=black}
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \ifdefstring{\ELEGANT@toc}{twocol}{
      \setlength{\columnsep}{2em}
      \begin{multicols}{2}%
        \@starttoc{toc}
      \end{multicols}}{
      \@starttoc{toc}}
    \if@restonecol\twocolumn\fi}


\renewcommand*{\cleardoublepage}{\clearpage\if@twoside \ifodd\c@page\else
\hbox{}%
\thispagestyle{empty}%
\newpage%
\if@twocolumn\hbox{}\newpage\fi\fi\fi}


%%% CAPTIONS %%%
\DeclareCaptionFormat{custom}
{%
    #1#2\small #3
}
\DeclareCaptionLabelSeparator{trait}{$\,-\,$}
\DeclareCaptionLabelSeparator{vert}{$\,\bm{\mid}\,$}
\usepackage[labelsep=trait]{caption}
\captionsetup{labelfont={sc,onehalfspacing,color=black},
format=custom}

%%% EXTRA PACKAGES %%%
\usepackage{tikz}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}

%%% SYMBOLS AND COMMON COMMANDS %%%
\input{symbols.sty}%$
% \input{URL.tex}%$
\input{URL_qftrules.tex}
\input{QR_qftrules.tex}

%%% FIGURE WITHIN EXERCISE ENVIRONNEMENT %%%
\newcommand{\capt}[1]{\captionof{figure}{#1}}
\addto\captionsfrench{
  \renewcommand{\figurename}{Fig.}
  }

%----------------------------------------------------------------------------------------
%	REMARQUE ET REMARQUETECH ET EXEMPLE
%----------------------------------------------------------------------------------------
\usepackage{mdframed}

%%% LAYOUT %%%
% \newmdenv[
%   topline=false,
%   bottomline=false,
%   rightline=false,
%   linecolor=brickred,
%   linewidth=1pt,
%   skipabove=\topsep,
%   skipbelow=\topsep
% ]{siderule}

%
% \newmdenv[
%   topline=false,
%   bottomline=false,
%   rightline=false,
%   linecolor=black,
%   linewidth=1.5pt,
%   skipabove=\topsep,
%   skipbelow=\topsep
% ]{sideruleremarque}
%
% \makeatletter
% \newenvironment{remarque}
% {  \begin{sideruleremarque}
%  \small}
% {\end{sideruleremarque}
% \normalsize}
% \makeatother

\newmdenv[
  topline=false,
  bottomline=false,
  rightline=false,
  linecolor=JoliRouge,
  linewidth=1.5pt,
  skipabove=\topsep,
  skipbelow=\topsep
]{siderulerappel}

\makeatletter
\newenvironment{rappel}[1]
{
%\vspace{-0.5em}
\begin{siderulerappel}{\textsc{#1}}\\
 \small}
{\end{siderulerappel}
\normalsize}
\makeatother

\newmdenv[
  topline=false,
  bottomline=false,
  rightline=false,
  linecolor=JoliRouge,
  linewidth=1.5pt,
  skipabove=\topsep,
  skipbelow=\topsep
]{sideruleremarquetech}

\makeatletter
\newenvironment{remarquetech}
{  \begin{sideruleremarquetech}
 \small}
{\end{sideruleremarquetech}
\normalsize}
\makeatother

\newmdenv[
  topline=false,
  bottomline=false,
  rightline=false,
  linecolor=JoliVert,
  linewidth=1.5pt,
  skipabove=\topsep,
  skipbelow=\topsep
]{sideruleexemple}

%\makeatletter
%\newenvironment{exemple}[1]
%{  \begin{sideruleexemple}{\textsc{#1}}\\
% \small}
%{\end{sideruleexemple}
%\normalsize}
%\makeatother

% \newcounter{exemple}
% \setcounter{exemple}{1}
% \makeatletter
% \newenvironment{exemple}[1]
% {\vspace{0.5em}
% \noindent{\color{structurecolor}\hrulefill}\fcolorbox{white}{structurecolor!30!white}
% {Exemple~\theexemple~:~\textsc{#1}}{\color{structurecolor}\hrulefill}\\
%  \small}
% {\vspace{-1em}
% {\noindent\color{structurecolor}\hrulefill}\\[-1em]
% \normalsize\addtocounter{exemple}{1}}
% \makeatother

% \newcounter{experience}
% \setcounter{experience}{1}
% \makeatletter
% \newenvironment{experience}[1]
% {\vspace{0.5em}
% \noindent{\color{structurecolor}\hrulefill}\fcolorbox{white}{structurecolor!30!white}
% {Expérience~\theexperience~:~\textsc{#1}}{\color{structurecolor}\hrulefill}\\
%  \small}
% {\vspace{-1em}
% {\noindent\color{structurecolor}\hrulefill}\\[-1em]
% \normalsize\addtocounter{experience}{1}}
% \makeatother

% \usepackage{vwcol}
\newcommand{\sol}[1]{
\begin{answer}
{#1}
\end{answer}
}

% remove leftmargin in quest env
\renewenvironment{quest}[1][\arabic]
{\begin{enumerate}[label=#1*),leftmargin=*,align=left]
\setcounter{enumi}{\value{quest}}
\everymath{\textstyle}
}
{\end{enumerate}
\setcounter{quest}{\value{enumi}}
}

\RenewDocumentEnvironment{soluce}{ O{Solution} }{%

% \begin{minipage}{\linewidth}%
\noindent\iconSoluce~~\textbf{\textcolor{iconcolor}{#1}}%
\begin{answer}%
}{%
\end{answer}%
% \end{minipage}%
}%

\newcommand{\examplesol}[2][*]{
% \bigskip\qqua
\ifthenelse{\equal{\detokenize{#1}}{\detokenize{*}}}{\setcounter{quest}{0}}{}
% \textbf{\textcolor{BrickRed}{Solution}}\medskip

\begin{soluce}
{#2}
\end{soluce}
\medskip

}
%
% %----------------------------------------------------------------------------------------
% %	ENVIRONNEMENTS POUR INCLURE LES FIGURES
% %---------------------------------------------------------------------------------------
% \usepackage{calc}
% \usepackage{subfigure}
\usepackage{wrapfig}
% \newlength{\mylength}
% \usepackage{xargs}
%
% \makeatletter
% \newcommand{\sousfigure}[6]
% { \tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[width={#3}\textwidth]{#1}\label{#2}}
%    \tikz[remember picture]\coordinate(figcenter);
%   \subfigure{\includegraphics[width={#6}\textwidth]{#4}\label{#5}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (a)};
%     \draw ($(figtop -| figcenter)-(0,0)$) node {\small (b)};
%   \end{tikzpicture}
% }
% \newcommand{\sousfigurecd}[6]
% { \tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[{#3}]{#1}\label{#2}}
%    \tikz[remember picture]\coordinate(figcenter);
%   \subfigure{\includegraphics[{#6}]{#4}\label{#5}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (c)};
%     \draw ($(figtop -| figcenter)-(0,0)$) node {\small (d)};
%   \end{tikzpicture}
% }
% \newcommand{\sousfigurecolonne}[6]
% { \tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[{#3}]{#1}\label{#2}}
%
%   \tikz[remember picture] \coordinate(figcenter);
%
%   \subfigure{\includegraphics[{#6}]{#4}\label{#5}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (a)};
%     \draw ($(figleft |- figcenter)-(0,0)$) node {\small (b)};
%   \end{tikzpicture}
% }
% \newcommand{\troissousfigures}[9]
% { \tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[{#3}]{#1}\label{#2}}\tikz[remember picture] \coordinate(figcenter1);
%   \subfigure{\includegraphics[{#6}]{#4}\label{#5}}
%   \tikz[remember picture] \coordinate(figcenter2);
%   \subfigure{\includegraphics[{#9}]{#7}\label{#8}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (a)};
%     \draw ($(figtop -| figcenter1)-(0,0)$) node {\small (b)};
%     \draw ($(figtop -| figcenter2)-(0,0)$) node {\small (c)};
%   \end{tikzpicture}
% }
% \newcommand{\troissousfigurescolonne}[9]
% { \tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[{#3}]{#1}\label{#2}}
%
%   \tikz[remember picture] \coordinate(figcenter1);
%
%   \subfigure{\includegraphics[{#6}]{#4}\label{#5}}
%
%   \tikz[remember picture] \coordinate(figcenter2);
%
%   \subfigure{\includegraphics[{#9}]{#7}\label{#8}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (a)};
%     \draw ($(figleft |- figcenter1)-(0,0)$) node {\small (b)};
%     \draw ($(figleft |- figcenter2)-(0,0)$) node {\small (c)};
%   \end{tikzpicture}
%   \vspace{-0.4cm}
% }
%
% \newcommand{\sousfigurescolonnedeuxun}[9]
% {\tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[{#3}]{#1}\label{#2}}\tikz[remember picture] \coordinate(figcenter);
%   \subfigure{\includegraphics[{#6}]{#4}\label{#5}}
%
%   \tikz[remember picture] \coordinate(figcenter1);
%
%   \subfigure{\includegraphics[{#9}]{#7}\label{#8}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (a)};
%     \draw ($(figtop -| figcenter)-(0,0)$) node {\small (b)};
%     \draw ($(figleft |- figcenter1)-(0,0)$) node {\small (c)};
%   \end{tikzpicture}
%   \vspace{-0.7cm}
% }
%
% \newcommand{\sousfigurescolonneundeux}[9]
% {\tikz[remember picture] \coordinate(figtop);
%
%   \tikz[remember picture] \coordinate(figleft);
%   \subfigure{\includegraphics[{#3}]{#1}\label{#2}}
%
%   \tikz[remember picture] \coordinate(figcenter);
%
%   \tikz[remember picture] \coordinate(figcenter1);\subfigure{\includegraphics[{#6}]{#4}\label{#5}}
%   \subfigure{\includegraphics[{#9}]{#7}\label{#8}}
%   \begin{tikzpicture}[overlay, remember picture]
%     \draw ($(figtop -| figleft)-(0,0)$) node {\small (a)};
%     \draw ($(figcenter1 |- figcenter)-(0,0)$) node {\small (b)};
%     \draw ($(figtop |- figcenter)-(0,0)$) node {\small (c)};
%   \end{tikzpicture}
%   \vspace{-0.7cm}
% }
% \makeatother

%%% PERSO ITEMIZE %%%
% \newcounter{quest}
% \setcounter{quest}{0}
%
% \newenvironment{quest}
% {\begin{enumerate}[label=\arabic*)]
% \setcounter{enumi}{\value{quest}}
% }
% {\end{enumerate}
% \setcounter{quest}{\value{enumi}}
% }


%%% EQUATION ENVIRONMENTS %%%
\renewcommand\theequation{\arabic{equation}}
% \usepackage{empheq}
%\newenvironment{eqbox}[1][]{
%	\setkeys{EmphEqEnv}{equation}
%	\setkeys{EmphEqOpt}{box={\setlength{\fboxsep}{3pt}\fcolorbox{black}{white}},#1}
%	\EmphEqMainEnv}
%{\endEmphEqMainEnv}


%%% PYTHON CODE %%%%
%\usepackage{listings}
%\lstset{language=Python}
%\lstset{frame=lines}
%\lstset{caption={Insert code directly in your document}}
%\lstset{label={lst:code_direct}}
%\lstset{basicstyle=\footnotesize}

\usepackage{minted}
\setminted{fontsize=\footnotesize}
%\newcommand{Code}[1]{
%%\textsc{Code python}\\
%\inputminted{python}{#1}
%}

%\newenvironment{Code}[1]{
%\textsc{Code python}\\
%\inputminted{python}{
%}
%{}}

% environnement méthode
\makeatletter
\newenvironment{methode}[1][]{
\begin{axiom}[#1]
\begin{enumerate}[label*=\protect\fbox{\arabic{enumi}}]
}
{
\end{enumerate}
\end{axiom}
}
\makeatother

% define method environment with suffix * 
\makeatletter
\newenvironment{methode*}[1][]{
\begin{axiom}[#1]
}
{
\end{axiom}
}

% environnement expérience
\makeatletter
\newcommand\listofdefinitions{\@starttoc{lod}}
\newenvironment{experience}[2][]{
\addcontentsline{lod}{chapter}{{#2}}{}
\begin{postulate}[#2]
}
{
\end{postulate}
}
\makeatother

% environnement exemple
\makeatletter
\NewDocumentEnvironment{exemple}{ m }{
\begin{example}[#1]
\setcounter{quest}{0}
}
{
  % \vspace{5cm}
\end{example}
% \sol{#2}
}
\makeatother


% prérequis PCSI %
% \newcommand{\pcsi}[1]{
% }

%%% PREAMBULE %%%
\usepackage{float}
\usepackage{ragged2e}             % for justifying text
\definecolor{customcolor}{RGB}{32,178,170}
\colorlet{coverlinecolor}{customcolor}
\author{Eric Brillaux}
\institute{Lyc\'ee Th\'eophile Gautier PC}
\date{\theyears}
\version{\today}
\logo{logo-blue.png}
\input{programme.tex}%$
