import re
from itertools import count
import argparse

def read_template(fp):
    """
    Reads in file and returns a correctly formatted string
    :fp: Absolute path to file
    :returns: Template as string, replacements changed to indices
    """
    with open(fp, 'r', encoding = 'utf-8') as tmpl:
        replaced = ""
        c = count()
        for line in tmpl:
            if '{{' and '}}' in line:
                matches = re.findall(r'{{.*?}}', line)
                for match in matches:
                    repl = '{' + str(next(c)) + '}'
                    line = re.sub(match, repl, line)
            replaced += line

        return replaced

def _print(doc, reps, n, prnt):
    """
    Replaces all things needing replacing in form letter.
    :n: Number of replacements in the text
    :returns: Replaced string
    """
    docs = []
    for rep in reps:
        assert len(rep) == n
        formatted = doc.format(*rep)
        if prnt:
            print(formatted)
            input() # Wait for user to give response
        docs.append(formatted)
    return docs



def replace(template_fp, replacement_fp, skip_first, delim, n, prnt):
    """
    :template_fp: Filepath to templater
    :replacement_fp: Filepath to CSV containing replacements (each line must have n entries)
    :skip_first: Skip header row, defaults to false
    :delim: Delimiter in file, defaults to '\t'
    :n: Number of replacements in the text
    :prnt: Print lines
    """
    with open(replacement_fp, 'r', encoding = 'utf-8') as reps:
        if skip_first: next(reps)
        replacements = [line.strip().split(delim) for line in reps]
        template = read_template(template_fp)
        formatted = _print(template, replacements, n, prnt)
    return formatted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--template'       , required = True  , help = 'Path to file with template written')
    parser.add_argument('--csv'            , required = True  , help = 'Path to delimited file containing replacement values')
    parser.add_argument('--delimiter'      , required = False , help = 'Delimiter to use. Defaults to <TAB>')
    parser.add_argument('--skip-header'    , required = False , help = 'Skip Header. Defaults to False.'            , choices = ['True' , 'False'])
    parser.add_argument('--n-replacements' , required = True  , help = 'Number of items to be replaced per document', type = int)
    parser.add_argument('--mail-field'     , required = False , help = 'The field the emails can be found in.'      , type = int)
    parser.add_argument('--file'           , required = False , help = 'Write out to filehandle. If not set each document is printed')
    args = parser.parse_args()

    delim = args.delimiter if args.delimiter else '\t'
    header = args.skip_header if args.skip_header else False
    prnt = True if not args.file else False
    replacements = replace(args.template, args.csv, header, delim, args.n_replacements, prnt)

    if args.file:
        with open(args.file, 'w', encoding = 'utf-8') as out:
            for repl in replacements:
                out.write(repl + '\n' + 80 * '-' + '\n\n')

main()
