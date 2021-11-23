# Reducing Revisions of Advisor (RRA) Linter
The aim of this linter is to identify and remove unnecessary, imprecise, or problematic wording from your paper so your advisor doesn't need to.

## How to install 

From the root directory simply run:
```
pip install -e .
```

## How to run
Run the linter using the command `RRAlint <your file>.tex` and it will output a report of the issues that RRA identified and the reason they are an issue.
```
> RRAlint sentence.tex
sentence.tex:05:(e docs\cite{green) - Syntax: add ~ to prevent a line break before the number
> RRAlint code_names.tex
code_names.tex:05:(adflow is n) - Capitalization: Its ADflow
code_names.tex:06:(I also like tacs.) - Capitalization: Its TACS
code_names.tex:07:(In particular, I like that they use a jacobian-free newton-kryl) - Capitalization: Capitalize the name Newton
code_names.tex:07:(In particular, I like that they use a jacobian-free) - Capitalization: Capitalize the name Jacobian
code_names.tex:07:(In particular, I like that they use a jacobian-free newton-krylov meth) - Syntax: use -- to get the right dash
> RRAlint weasal_words.tex
weasal_words.tex:5:(irly many cita) - Weasel Word
weasal_words.tex:6:(This makes me very exce) - Weasel Word
weasal_words.tex:5:(have fairly many) - Weasel Word
weasal_words.tex:6:(This makes me very exceedingly qual) - Weasel Word
weasal_words.tex:7:(This citations are largely from myself, but there is a number of citations which are) - Possible Error: May need a comma between which and noun or should be that
weasal_words.tex:7:(This citations are largely from) - Weasel Word
weasal_words.tex:7:(This citations are largely from myself, but there is a number of c) - Weasel Word
weasal_words.tex:8:(not. Clearly, I a) - Weasel Word
weasal_words.tex:8:(Clearly, I am relatively succ) - Weasel Word
```

## How does it work?

The linter uses regex expressions to find words, phrases, or syntax in your tex file.
These regex expressions express rules that are written in the `RRAlinter/rules/` and `RRAlinter/suggestions/`  directories.
You can add or comment out (using #) rules that exist by modifying the contents of the `rules` and `suggestions` directories.

## Acknowledgments
This linter is a modified version of the linter by  [Hundter Biede](https://git.unl.edu/hbiede), Which is based on the linter by  [Neil Spring](https://github.com/nspring/style-check).
