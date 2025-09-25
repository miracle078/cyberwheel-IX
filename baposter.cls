% baposter.cls - Basic Academic Poster class
% Simplified version for basic poster functionality
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{baposter}[2024/01/01 v1.0 Basic Academic Poster]

% Base class
\LoadClass[a0paper,landscape]{article}

% Required packages
\RequirePackage[margin=1cm]{geometry}
\RequirePackage{multicol}
\RequirePackage{xcolor}
\RequirePackage{tikz}
\RequirePackage{tcolorbox}
\RequirePackage{calc}
\RequirePackage{ifthen}

% Color definitions
\definecolor{lightblue}{rgb}{0.145,0.6666,1}
\definecolor{lightgray}{rgb}{0.9,0.9,0.9}
\definecolor{darkblue}{rgb}{0.0,0.2,0.5}
\definecolor{white}{rgb}{1,1,1}
\definecolor{darkgray}{rgb}{0.4,0.4,0.4}

% Global variables for poster configuration
\newcommand{\@bgColorOne}{white}
\newcommand{\@bgColorTwo}{white}
\newcommand{\@borderColor}{darkblue}
\newcommand{\@headerColorOne}{darkblue}
\newcommand{\@headerColorTwo}{lightblue}
\newcommand{\@headerFontColor}{white}
\newcommand{\@boxColorOne}{white}
\newcommand{\@boxColorTwo}{lightgray}
\newcommand{\@textborder}{roundedleft}
\newcommand{\@eyecatcher}{true}
\newcommand{\@headerborder}{closed}
\newcommand{\@headerheight}{0.1\textheight}
\newcommand{\@textfont}{\normalfont}
\newcommand{\@headershape}{roundedright}
\newcommand{\@headershade}{shadelr}
\newcommand{\@headerfont}{\Large\bfseries}
\newcommand{\@textshade}{shade-tb}
\newcommand{\@background}{shade-tb}
\newcommand{\@linewidth}{2pt}
\newcommand{\@colspacing}{1em}

% Poster environment
\newenvironment{poster}[1][]{%
  % Process options (simplified)
  \begin{tikzpicture}[remember picture,overlay]
    \fill[\@bgColorOne] (current page.south west) rectangle (current page.north east);
  \end{tikzpicture}
  \pagestyle{empty}
  \setlength{\columnsep}{\@colspacing}
}{%
  % End poster
}

% Header box environment
\newtcolorbox{headerbox}[3][]{
  colback=\@boxColorOne,
  colframe=\@borderColor,
  coltitle=\@headerFontColor,
  colbacktitle=\@headerColorOne,
  title={#2},
  fonttitle=\@headerfont,
  rounded corners,
  boxrule=\@linewidth,
  width=\linewidth,
  #1
}

% Simplified column breaking (only if not already defined)
\providecommand{\columnbreak}{\vfill\break}

% Page setup
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.5em}

% Font size adjustments for a0paper
\renewcommand{\normalsize}{\fontsize{25}{30}\selectfont}
\renewcommand{\large}{\fontsize{30}{36}\selectfont}
\renewcommand{\Large}{\fontsize{36}{43}\selectfont}
\renewcommand{\LARGE}{\fontsize{43}{52}\selectfont}
\renewcommand{\huge}{\fontsize{52}{62}\selectfont}
\renewcommand{\Huge}{\fontsize{62}{75}\selectfont}
\renewcommand{\small}{\fontsize{22}{26}\selectfont}
\renewcommand{\footnotesize}{\fontsize{20}{24}\selectfont}
\renewcommand{\scriptsize}{\fontsize{18}{22}\selectfont}
\renewcommand{\tiny}{\fontsize{15}{18}\selectfont}