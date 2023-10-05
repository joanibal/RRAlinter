import re
import sys
import argparse
from math import log10, floor
import os
from os import listdir
from os.path import isfile, join, isdir, expanduser
from typing import List, Dict, Tuple
from pprint import pprint

Pattern = type(re.compile("", 0))
Match = type(re.match(r"\s", " "))
default_commands = (
    r"begin|bibliography|documentclass|end|figure|includegraphics|input|label|newcommand|table"
    r"|texttt|todo|(auto)?ref"
)


def main():
    """
    This is the entry point for the linter
    """
    parser = argparse.ArgumentParser(prog="RRAlint")
    parser.add_argument("tex_file", help="Name of input .tex file")
    parser.add_argument(
        "--no-color", default=False, action="store_true", help="Disable color output"
    )
    parser.add_argument(
        "--cntxt-char",
        default=10,
        type=int,
        help="Number of characters to show before and after a match",
    )
    parser.add_argument(
        "--no-suggestions",
        default=False,
        action="store_true",
        help="Disables the suggestions",
    )
    args = parser.parse_args()

    # Read in the rules
    rules_list, suggestions_list = read_rules()
    rules, ignored_commands = parse_rules(rules_list)
    suggestions, ignored_commands = parse_rules(suggestions_list)

    # There must be some rules
    if len(rules) == 0:
        print("Define some rules before using", file=sys.stderr)
        exit(-1)

    ignored_commands.extend(default_commands.split("|"))

    command_regex = compile_command(ignored_commands)

    latex_lines = read_latex(args.tex_file)

    errors, warnings = process_files(
        latex_lines,
        rules,
        suggestions,
        command_regex,
        num_context_char=args.cntxt_char,
        coloring=(not args.no_color),
    )

    if len(errors) > 0:
        # print the header
        print("Errors", file=sys.stderr)
    for rule in errors:
        print(rule, file=sys.stderr)

    if not args.no_suggestions:
        if len(warnings) > 0:
            if len(errors) > 0:
                print("")  # add a break between the two categories
            # print the header
            print("Warnings", file=sys.stderr)
        for rule in warnings:
            print(rule, file=sys.stderr)

    exit(len(errors))


def get_all_files(directory: str) -> List[str]:
    """
    Searches the top level of a given directory and returns a list of all files in the given directory

    :param directory: str
        The directory to be searched
    :rtype: List[str]
    :return: A list of file paths in the given directory
    """
    if isfile(directory):
        return [directory]
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    try:
        files.remove(".DS_Store")
    except ValueError:
        pass
    return list(
        map(
            lambda file: directory + ("" if directory[-1] == "/" else "/") + file, files
        )
    )


def read_rules() -> List[str]:
    """
    Searches the command line arguments for a rule-set and defaults to the user rule-set if none is given.
    Reads all rules and returns a set of rules to be processed.

    :rtype: List[str]
    :returns rulesList (List[str]) The list of rules as read in from the rule-sets to be used
    """

    # find rule set directory(ies) in the arguments
    # rules_dirs = [i for i, arg in enumerate(sys.argv) if ['-r', '--rules'].__contains__(arg)]
    rules_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules")
    suggestions_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "suggestions"
    )

    rule_set_files = get_all_files(rules_dir)
    suggestions_set_files = get_all_files(suggestions_dir)

    rules_list = []
    suggestions_list = []

    for file in rule_set_files:
        f = open(file, "r")
        for line in f:
            # raw_line = fr'{line.strip()}'
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue

            # raw_line = repr(line)
            # print(raw_line)
            rules_list.append(line)
            # pprint(rules_list)

    for file in suggestions_set_files:
        f = open(file, "r")
        for line in f:
            # raw_line = fr'{line.strip()}'
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue

            # raw_line = repr(line)
            # print(raw_line)
            suggestions_list.append(line)
            # pprint(rules_list)

    return rules_list, suggestions_list


def parse_rules(rule_list: List[str]) -> (Dict[Pattern, str], List[str]):
    """
    Take a list of rules strings in the form 'rule_pattern % RuleType: Reasoning' and parse it out to be used

    :param rule_list: List[str]
        A list of rules to be parsed and compiled to regex and reasonings
    :rtype: Tuple[Dict[Pattern, str], List[str]]
    :return: First, a dictionary of RegEx patterns to their reasonings, and then a list of commands to ignore
    """
    rule_mapping: Dict[Pattern, str] = {
        re.compile(
            r"(?<!(etc|seq))(?<!(al))(?<!(etal))\.\s+[a-z]"
        ): "Capitalization: Sentences start with capital letters"
    }
    commands_to_ignore = []
    surrounding_terms = {"Capitalization": r"\b", "Phrasing": r"\b", "Spelling": r"\b"}
    case_sensitivity_mapping = {
        "Capitalization": 0,
    }

    for rule_line in rule_list:
        if rule_line.startswith("#") or len(rule_line) == 0:
            continue
        try:
            rule_str, reasoning = rule_line.split("%", 1)
        except ValueError:
            print("The following line is malformed: %s" % rule_line, file=sys.stderr)
            continue
        rule_str = rule_str.strip().replace("$", r"\b")
        reasoning = reasoning.strip()
        if reasoning == "ignoredCommand":
            commands_to_ignore.append(rule_str)
        else:
            surrounding_term = surrounding_terms.get(
                reasoning.split(":")[0].strip(), ""
            )
            case_sensitivity = (
                case_sensitivity_mapping.get(
                    reasoning.split(":")[0].strip(), re.IGNORECASE
                )
                + re.UNICODE
                + re.MULTILINE
            )
            rule_str = rule_str.replace(" ", r"\s")
            try:
                regex = re.compile(
                    surrounding_term + rule_str + surrounding_term, case_sensitivity
                )
            except re.error as e:
                print(
                    "The following rule could not be compiled to a valid regex: %s"
                    % rule_line,
                    file=sys.stderr,
                )
                continue
            rule_mapping[regex] = reasoning
            pass

    return rule_mapping, commands_to_ignore


def read_latex(file_name) -> Dict[str, List[str]]:
    """
    Reads all files given to the command arguments (after the rule set directories have been parsed out),
    reads their contents, and returns a dictionary of the file names mapped onto lines from that file as a list

    :rtype: Dict[str, List[str]]
    :return: A dictionary of the file name mapped onto lines from that file as a list
    """
    comment_regex = re.compile(r"(([^\\]%.*)|(^%.*))$")

    file_lines = {}
    file = open(file_name, "r")
    single_file_lines = []
    for line in file:
        line = line.strip()
        if comment_regex.search(line):
            line = comment_regex.split(line)[0]
        single_file_lines.append(line)
    file_lines[file_name] = single_file_lines

    return file_lines


def test_line(
    line_to_test: str, rule_patterns: Dict[Pattern, str]
) -> List[Tuple[Pattern, Match]]:
    """
    Test a given string against all rule patters
    :param line_to_test: str
        The string to be tested against the RegEx patterns for a match
    :param rule_patterns: Dict[Pattern, str]
        A dictionary mapping the list of RegEx patterns onto their reasoning strings
    :rtype: List[Tuple[Pattern, Match]]
    :return: A list of rules broken and the Match objects that define the start and end points of the match in the test
        string
    """
    rules_broken = []
    for rule in rule_patterns:
        match = rule.search(line_to_test)

        if match is not None:
            rules_broken.append((rule, match))
    return rules_broken


def remove_commands(line: str, commands: Pattern) -> str:
    """
    Strip a LaTeX source string of commands defined as needing to be ignored
    :param line: str
        The LaTeX source string
    :param commands: Pattern
        The pattern compiled of all the commands to ignore
    :rtype: str
    :return: The source string, with the commands and their arguments removed
    """
    # noinspection RegExpRedundantEscape
    clear_of_french_spacing = re.search(r"\s[\.\?!,;:]", line) is None
    return_val = commands.sub("", line)
    if len(return_val) > 1 and clear_of_french_spacing:
        return_val = re.sub(r"[~\s]*(?=[.?!,;:])", "", return_val)
    return return_val


def remove_math(latex: Dict[str, List[str]]):
    """
    Removes all characters enclosed in a math block
    :param latex: Dict[str, List[str]]
        A mapping of file names onto a list of that file's lines
    """
    for file_name in latex:
        file = latex[file_name]
        math_mode: bool = False
        for i in range(len(file)):
            new_line = ""
            for c in file[i]:
                if c == "$":
                    math_mode = not math_mode
                elif not math_mode:
                    new_line += c
            file[i] = new_line
    return latex


def process_files(
    file_lines: Dict[str, List[str]],
    error_patterns: Dict[Pattern, str],
    suggestion_patterns: Dict[Pattern, str],
    ignored_command_regex: Pattern,
    num_context_char=10,
    coloring=True,
) -> List[str]:
    """
    Takes all the lines that need to be checked, removes any math blocks and commands, then checks them for broken
        rules (including those that span multiple lines)
    :param file_lines: Dict[str, List[str]]
        A mapping of file names onto a list of that file's lines
    :param rule_patterns: Dict[Pattern, str]
        A dictionary mapping the list of RegEx patterns onto their reasoning strings
    :param suggestions_patterns: Dict[Pattern, str]
        A dictionary mapping the list of RegEx patterns onto their reasoning strings
    :param ignored_command_regex:
        The pattern compiled of all the commands to ignore
    :rtype: List[str]
    :return: A list of strings reporting each rule broken formatted for output
    """
    remove_math(file_lines)
    errors = []
    warnings = []

    def save_broken_rules(rule_broken_on_line, rule_patterns, error_list, line_num):
        error_line = line_num + 1
        for rule_broken, error in rule_broken_on_line:
            # print(rule_broken, error)
            # import pdb; pdb.set_trace()
            # try:
            # line_break_index = combined_line.index('\n')
            # except ValueError:
            # line_break_index = len(line)
            # error_line = i + 1 if error.span()[0] < line_break_index else i + 2
            if error != "" and (
                len(errors) == 0
                or not rules_broken.get(error_line, []).__contains__(rule_broken)
            ):
                error_beg = error.span()[0]
                error_end = error.span()[1]
                context_beg = max(0, error_beg - num_context_char)
                context_end = min(len(line), error_end + num_context_char)

                error_str = line[error_beg:error_end]

                context_before = line[context_beg:error_beg]
                context_after = line[error_end:context_end]

                if coloring:
                    error_str = "\033[1;31m" + error_str + "\033[0m"

                full_error_str = (
                    (context_before + error_str + context_after)
                    .strip()
                    .replace("\n", " ")
                )

                # error_list.append(("  %s:%0" + format_length + "d:%0d (%s) - %s") %
                #                 (file_name, error_line, error_beg+1, full_error_str, rule_patterns[rule_broken]))
                error_list.append(
                    f"  {file_name}"
                    + format_length
                    + f"{error_line}:{error_beg+1:0d} ({full_error_str}) - {rule_patterns[rule_broken]}"
                )
                # rules_broken_list = rules_broken.get(error_line, [])
                # if rules_broken_list:
                #     rules_broken_list.append(rule_broken)
                # else:
                #     rules_broken[error_line] = [rule_broken]

    for file_name in file_lines:
        file = file_lines[file_name]
        format_length = str(floor(log10(len(file)) + 1))
        rules_broken = dict()
        for i in range(len(file)):
            # first_line = remove_commands(file[i], ignored_command_regex)
            line = remove_commands(file[i], ignored_command_regex)
            if line == "":
                continue
            # second_line = remove_commands('' if i == (len(file) - 1) else '\n' + file[i + 1].strip(),
            #   ignored_command_regex)
            # combined_line = first_line + second_line
            rule_broken_on_line = test_line(line, error_patterns)
            save_broken_rules(rule_broken_on_line, error_patterns, errors, i)
            suggestion_broken_on_line = test_line(line, suggestion_patterns)
            save_broken_rules(
                suggestion_broken_on_line, suggestion_patterns, warnings, i
            )

    return errors, warnings


def compile_command(commands: List[str]) -> Pattern:
    """
    Generates a pattern to be used in removing commands from LaTeX source lines
    :param commands: List[str]
        A list of command names (case-sensitive) to be ignored
    :rtype: Pattern
    :return: The compiled pattern
    """
    return re.compile(r"\\(" + "|".join(commands) + r")(\[[^\]]*\])?{[^{}]*}")
