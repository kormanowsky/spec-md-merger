import argparse
from os.path import abspath
from os import getcwd
from pathlib import Path
from sys import stderr
from json import loads, dumps, JSONDecodeError
from enum import Enum, auto


# Exit Codes
class ExitCodes(Enum):
    INVALID_COMMAND = auto()
    NO_INPUT_FILE = auto()
    NO_MD_ROOT = auto()
    MD_ROOT_EXISTS = auto()
    INVALID_INPUT_FILE = auto()
    INVALID_INFO = auto()
    INVALID_PATHS = auto()
    INVALID_PATH = auto()
    INVALID_METHOD = auto()
    NO_OUTPUT_PARENT = auto()


# Strip # from titles
def strip_starting_hash(inp):
    inp = inp.strip()
    if inp and inp[0] == "#":
        inp = inp[1:].strip()
    return inp


# Code Languages
LANGUAGES = {
    "Python": ".py",
    "PHP": ".php",
    "JavaScript": ".js",
    "Java": ".java",
    "C": ".c",
    "C++": ".cpp",
    "C#": ".cs",
    "Go": ".go",
    "Dart": ".dart",
}

# Available Commands
COMMANDS = ["merge", "createfiles"]

# Parse CLI Args
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    dest="command"
)

# merge subcommand
parser_merge = subparsers.add_parser(
    "merge",
    help="Merge your spec file "
         "and your markdown files"
)
parser_merge.add_argument(
    "input_file",
    help="The path to your raw spec file "
         "(must be a valid JSON file "
         "so must end in .json)"
)
parser_merge.add_argument(
    "files_root",
    nargs="?",
    default=getcwd(),
    help="The path to the root of the folder "
         "with your .md and code samples files"
)
parser_merge.add_argument(
    "output_file",
    nargs="?",
    default=None,
    help="The path to the result"
         "(must be a valid JSON file "
         "so must end in .json). "
         "If not present, the result "
         "will be printed to"
         "the screen."
)

# createfiles subcommand
parser_createfiles = subparsers.add_parser(
    "createfiles",
    help="Create blank .md and "
         "code samples files for "
         "easy copy-pasting"
)
parser_createfiles.add_argument(
    "input_file",
    help="The path to your raw spec file "
         "(must be a valid JSON file "
         "so must end in .json)"
)
parser_createfiles.add_argument(
    "files_root",
    nargs="?",
    default=getcwd(),
    help="The path to the root of the folder "
         "with your .md and code samples files"
)
parser_createfiles.add_argument(
    "--languages",
    nargs="+",
    default=[],
    choices=LANGUAGES.keys(),
    help="A list of programming languages to use for empty code sample files."
)

args = parser.parse_args()

# Check What Command Are We Running
command = args.command
if command not in COMMANDS:
    print("Error: incorrect command, must be one of %s" % dumps(COMMANDS))
    exit(ExitCodes.INVALID_COMMAND)

# Check Input File
input_path = Path(abspath(args.input_file))
if not input_path.exists():
    print("Error: input spec %s does not exist" % input_path, file=stderr)
    exit(ExitCodes.NO_INPUT_FILE)

# Check Root
root_path = args.files_root
md_root = Path(abspath(root_path))
if md_root.exists() and md_root.is_dir():
    if command == "createfiles":
        print("Error: given root %s already exists" % md_root, file=stderr)
        exit(ExitCodes.MD_ROOT_EXISTS)
elif command == "createfiles":
    md_root.mkdir(parents=True)
else:
    print("Error: MarkDown root %s does not exist "
          "or is not a directory" % md_root, file=stderr)
    exit(ExitCodes.NO_MD_ROOT)

# Open Input File
spec = {}
with open(input_path, "r") as input_file:
    try:
        spec = loads(input_file.read())
    except JSONDecodeError:
        print("Error: given file is not valid JSON", file=stderr)
        exit(ExitCodes.INVALID_INPUT_FILE)

# Add General Info
if "info" not in spec:
    spec["info"] = {}
info_md_path = md_root / "info.md"
if info_md_path.exists():
    if command == "merge":
        with open(info_md_path, "r") as info_file:
            if type(spec["info"]) != dict:
                print("Error: \"info\" section is not a dictionary",
                      file=stderr)
                exit(ExitCodes.INVALID_INFO)
            spec["info"]["title"] = strip_starting_hash(
                info_file.readline()
            )
            spec["info"]["description"] = info_file.read()
elif command == "createfiles":
    info_md_path.touch()
else:
    print("Warning: MarkDown file "
          "with general info %s is not present" % info_md_path)

# Add Methods Info
if "paths" not in spec:
    spec["paths"] = {}
if type(spec["paths"]) != dict:
    print("Error \"paths\" section is not a dictionary", file=stderr)
    exit(ExitCodes.INVALID_PATHS)

for path in spec["paths"]:
    # Add Path Info
    path_info = spec["paths"][path]
    if type(path_info) != dict:
        print("Error: path %s is not a dictionary" % path, file=stderr)
        exit(ExitCodes.INVALID_PATH)
    for method in path_info:
        # Add Method Info
        method_info = path_info[method]
        if type(method_info) != dict:
            print("Error: method %s of path %s "
                  "is not a dictionary" % (method, path), file=stderr)
            exit(ExitCodes.INVALID_METHOD)
        path_no_slash = path[1:] if path[0] == "/" else path
        method_md_path = md_root.joinpath(path_no_slash) / ("%s.md" % method)
        if command == "createfiles":
            method_md_path.parent.mkdir(parents=True)
            method_md_path.touch()
            for lang in args.languages:
                method_code_path = md_root.joinpath(path_no_slash) / (
                        "%s%s" % (method, LANGUAGES[lang])
                )
                method_code_path.touch()
            continue
        if not method_md_path.exists():
            print("Warning: MarkDown file %s "
                  "for path %s and method %s "
                  "is not present" % (method_md_path, path, method))
            continue
        with open(method_md_path, "r") as method_file:
            method_info["summary"] = strip_starting_hash(
                method_file.readline()
            )
            method_info["description"] = method_file.read()
        code_samples = []
        for lang in LANGUAGES:
            method_code_path = md_root.joinpath(path_no_slash) / (
                    "%s%s" % (method, LANGUAGES[lang])
            )
            if method_code_path.exists():
                with open(method_code_path, "r") as method_code_file:
                    code_samples.append({
                        "lang": lang,
                        "source": method_code_file.read()
                    })
        if code_samples:
            method_info["x-codeSamples"] = code_samples

# Finish createfiles
if command == "createfiles":
    print("Done")
    exit()

# Write To Screen
if args.output_file is None:
    print(dumps(spec))
    exit()

# Write To File
output_path = Path(abspath(args.output_file))
if not output_path.parent.exists():
    print("Error: output spec %s parent does not exist" % output_path.parent)
    exit(ExitCodes.NO_OUTPUT_PARENT)
with open(output_path, "w") as output_file:
    output_file.write(dumps(spec))
print("Done")
