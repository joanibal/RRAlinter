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
add the option '--no-suggestions' to remove the suggestions from the linting report.

```
> RRAlint sentence.tex
Errors
  sentence.tex25:86 (of the docs\cite{greenwade9) - Syntax: add ~ to prevent a line break before the number
```

```
> RRAlint weasel_words.tex
Warnings
  weasel_words.tex15:15 (ve fairly many citations) - Weasel Word
  weasel_words.tex15:8 (I have fairly many cita) - Weasel Word
  weasel_words.tex16:15 (makes me very exceeding) - Weasel Word
  weasel_words.tex16:20 (s me very exceedingly qualified) - Weasel Word
  weasel_words.tex17:20 (tions are largely from myse) - Weasel Word
  weasel_words.tex17:51 (but there is a number of citati) - Weasel Word
  weasel_words.tex17:75 (citations which are not.) - Possible Wrong Word: May need a comma between which and noun or should be that
  weasel_words.tex18:15 (rly, I am relatively successfu) - Weasel Word
  weasel_words.tex18:1 (Clearly, I am rel) - Verbose: Should rarely be used
```

```
> RRAlint grammar.tex --cntxt-char=100
Errors
  grammar.tex15:12 (Grammar is comprised of many rules including: punctuation, spelling, etc.) - Grammar: Should be "composed of"
  grammar.tex15:36 (Grammar is comprised of many rules including: punctuation, spelling, etc.) - Grammar: Including implies an incomplete list, so don't double up with an etc.
  grammar.tex15:36 (Grammar is comprised of many rules including: punctuation, spelling, etc.) - Grammar: Including leads directly into lists without semi-colons. Semi-colon lists should come after nouns
  grammar.tex16:15 (And thusly, I can not remember all of them.) - Grammar: Should be "cannot"
  grammar.tex16:5 (And thusly, I can not remember all of them.) - Grammar: Should be "thus"
  grammar.tex17:14 (This lead to the the creation of RRAlinter to safe guard against error.) - Grammar: remove second "the"
  grammar.tex17:6 (This lead to the the creation of RRAlinter to safe guard against error.) - Grammar: Should be "leads to" or "led to"
  grammar.tex17:47 (This lead to the the creation of RRAlinter to safe guard against error.) - Grammar: Should be "safeguard"

Warnings
  grammar.tex15:25 (Grammar is comprised of many rules including: punctuation, spelling, etc.) - Weasel Word
  grammar.tex16:32 (And thusly, I can not remember all of them.) - Verbose: Should be "all"
```

## How does it work?

The linter uses regex expressions to find words, phrases, or syntax in your tex file.
These regex expressions express rules that are written in the `RRAlinter/rules/` and `RRAlinter/suggestions/`  directories.
You can add or comment out (using #) rules that exist by modifying the contents of the `rules` and `suggestions` directories.

## Acknowledgments
This linter is a modified version of the linter by  [Hundter Biede](https://git.unl.edu/hbiede), Which is based on the linter by  [Neil Spring](https://github.com/nspring/style-check).
