# Reducing Revisions of Advisor (RRA) Linter
The aim of this linter is to identify and remove unnecessary, imprecise, or problematic wording from your paper so your advisor doesn't need to.

## How to install 

From the root directory simply run:
```
pip install -e .
```

## How to run
Run the linter using the command `RRAlint <your file>.tex` and it will output a report of the issues that RRA identified and the reason they are an issue.

add the option '--no-color' to the command to disable color output.
set the option '--cntxt-char' to specify the number of characters to show before and after the issue.

```
> RRAlint sentence.tex
sentence.tex:05:86:(of the docs\cite{greenwade9) - Syntax: add ~ to prevent a line break before the number
```

```
> RRAlint weasel_words.tex
weasel_words.tex:5:15:(ve fairly many citations) - Weasel Word
weasel_words.tex:5:8:(I have fairly many cita) - Weasel Word
weasel_words.tex:6:15:(makes me very exceeding) - Weasel Word
weasel_words.tex:6:20:(s me very exceedingly qualified) - Weasel Word
weasel_words.tex:7:75:(citations which are not.) - Possible Wrong Word: May need a comma between which and noun or should be that
weasel_words.tex:7:20:(tions are largely from myse) - Weasel Word
weasel_words.tex:7:51:(but there is a number of citati) - Weasel Word
weasel_words.tex:8:1:(Clearly, I am rel) - Verbose: Should rarely be used
weasel_words.tex:8:15:(rly, I am relatively successfu) - Weasel Word
```

```
> RRAlint grammar.tex --cntxt-char=100
grammar.tex:5:12:(Grammar is comprised of many rules including: punctuation, spelling, etc.) - Grammar: Should be "composed of"
grammar.tex:5:36:(Grammar is comprised of many rules including: punctuation, spelling, etc.) - Grammar: Including implies an incomplete list, so don't double up with an etc.
grammar.tex:5:36:(Grammar is comprised of many rules including: punctuation, spelling, etc.) - Grammar: Including leads directly into lists without semi-colons. Semi-colon lists should come after nouns
grammar.tex:5:25:(Grammar is comprised of many rules including: punctuation, spelling, etc.) - Weasel Word
grammar.tex:6:15:(And thusly, I can not remember all of them.) - Grammar: Should be "cannot"
grammar.tex:6:5:(And thusly, I can not remember all of them.) - Grammar: Should be "thus"
grammar.tex:6:32:(And thusly, I can not remember all of them.) - Verbose: Should be "all"
grammar.tex:7:14:(This lead to the the creation of RRAlinter to safe guard against error.) - Grammar: remove second "the"
grammar.tex:7:6:(This lead to the the creation of RRAlinter to safe guard against error.) - Grammar: Should be "leads to" or "led to"
grammar.tex:7:47:(This lead to the the creation of RRAlinter to safe guard against error.) - Grammar: Should be "safeguard"
```

## How does it work?

The linter uses regex expressions to find words, phrases, or syntax in your tex file.
These regex expressions express rules that are written in the `RRAlinter/rules/` and `RRAlinter/suggestions/`  directories.
You can add or comment out (using #) rules that exist by modifying the contents of the `rules` and `suggestions` directories.

## Acknowledgments
This linter is a modified version of the linter by  [Hundter Biede](https://git.unl.edu/hbiede), Which is based on the linter by  [Neil Spring](https://github.com/nspring/style-check).
