# Final Bootstrapping Version

With the base syntax implemented and the ability to reference external files, it's now possible to assemble a version capable of building the main codebase. Unlike previous steps in the bootstrapping process, the script produced takes no arguments. When run, it will produce a full version of the `tome` executable, after which you should be capable of running `tome build`.

## Project Relative Paths

The main feature still lacking is a notion of project relative paths. This is a simplified version of the logic defined in [the section on the project context](/3_Project_Structure/1_Context.md).

`{#Project context}: s`
```python
import re
import os
from pathlib import Path

class Context():
    def __init__(self):
        self.project_root = Path.cwd().parent
        self.files = {}
        self.add_directory(self.project_root)
        self.macros = {}

    def add_directory(self, path):
        for file in path.glob("**/*.md"):
            self.add_file(file)

    def add_file(self, file):
        self.files[<../3_Project_Structure/1_Context.md#Convert system path to project path>] = file.absolute()

    def absolute_path(self, project_path):
        return self.project_root / re.sub(r"^/", "", project_path)

context = Context()
```

## Expanding Macros

With a broader set of files that need to be operated on, a new loop has to be incorporated into the expansion process from the previous stage. The previous logic tracks and depends on a dictionary named `files`, so also need to use that here.

`{#Build files}: s`
```python
for doc_file in context.files.values():
    if doc_file not in files:
        files[doc_file] = File(doc_file)
    <3_External_Links.md#Build new files>
```

Finding a macro now requires awareness of the overall context, so a new definition of this function is used.

`{#Find macro}: s`
```python
files = {}
def find_macro_file(current_file, location):
    path = location["file"]
    if not path:
        path = current_file
    elif path[0] == "/":
        path = context.absolute_path(path)
    else:
        path = Path(current_file).parent / path
    file = files.get(path, File(path))
    if not file.macros:
        file.catalog_code_blocks()
    return file
```

When writing file macros, project relative paths have to be expanded and nonexistent directories need to be created.

`{#Get file name}: s`
```python
def get_file_name(file_macro):
    path = context.absolute_path(file_macro.name)
    path.parent.mkdir(exist_ok = True, parents = True)
    return path
```

The rest of the expansion process should be reusable unmodified.

`{#4_Final_Bootstrapping_Version.py}: f`
```python
<#Project context>
<3_External_Links.md#File class>
<3_External_Links.md#Macro class>
<3_External_Links.md#Detect unexpanded macro>
<#Find macro>
<3_External_Links.md#Expand line>
<3_External_Links.md#Expand code block>
<#Get file name>
<#Build files>
```
