# Spec and Markdown Merger 

Merges your Swagger spec and MarkDown description files, 
optionally adding code samples.

# Usage

`python3 main.py COMMAND ARGS`

# Commands

## `createfiles`
`python3 main.py createfiles YOUR_SPEC [YOUR_ROOT_FOLDER] 
[--languages LANG1 LANG2 ... LANGN`

This command will create all necessary folders and 
empty .md and code sample files for your spec. 
`LANG1`, `LANG2` etc are names of programming languages. 
Now this program supports
languages listed below. 
```python3
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
```

## `merge`
`python3 main.py merge YOUR_SPEC [YOUR_ROOT_FOLDER] [OUTPUT_SPEC]`

This command will merge your spec and your MarkDown files and output the result
to `OUTPUT_SPEC` if it is present, or will `print()` the result.

## Note

`YOUR_ROOT_FOLDER` is current working directory by default.

# Folders and files

## `YOUR_ROOT_FOLDER/info.md`

Contains general information about your spec. The first line is the `"title"`, 
the rest of the file is the `"description"`

## `YOUR_ROOT_FOLDER/YOUR_PATH/YOUR_METHOD.md`

Contains information about one of YOUR_PATH methods. The first line is the 
`"summary"`, the rest of the file is the `"description"`

## Example
You have API method `/users/list` and you're writing a MarkDown file
for `POST` method. You should name your file `YOUR_ROOT_FOLDER/users/list/post.md`.
