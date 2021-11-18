# Reducing Revisions of Advisor (RRA) Linter
The aim of this linter is to identify and remove unnecessary, imprecise, or problematic wording from your paper so your advisor doesn't need to.

## How does it work?

The linter uses the regex to to find words, phrases, or syntax in your tex file.
These regex expressions express rules that are written in the ``~/rules/` directory.
Run the linter using the command `RRAlint <your file>.tex` and it will output a report of the issues that RRA identified and the reason they are an issue.
You can add to the rules that exist there or comment out (using #) the ones you don't want to use.

## Acknowledgments
This linter is a modified version of the linter by  [Hundter Biede](https://git.unl.edu/hbiede), Which is based on the linter by  [Neil Spring](https://github.com/nspring/style-check).
