# Spec and Markdown Merger 

Merges your Swagger spec and MarkDown description files

# Usage

1. Create a spec file and markdown files for each path and method. Also create
a file with general info for your spec.
2. Put your files into a folder which we'll call `$md_root$` according to the 
following rule:
    - `$md_root$ / info.md` - General information file, the first line is the `"title"`, 
the rest of the file is the `"description"`
    - `$md_root$ / YOUR_PATH_HERE / YOUR_METHOD_HERE.md` - A path's method information, 
the first line is the `"summary"`, the rest of the file is the `"description"`

    **Example:** You have API method `/users/list` and you're writing a MarkDown file
for `POST` method. You should name your file `$md_root$/users/list/post.md`.
3. Run `python3 main.py YOUR_RAW_SPEC_PATH $md_root$ [OUTPUT_SPEC_PATH]` where 
`YOUR_RAW_SPEC_PATH` is the path to your JSON spec file, and `OUTPUT_SPEC_PATH`
is the path where the result will be saved. If `OUTPUT_SPEC_PATH` is not present, 
the program will `print()` the result.