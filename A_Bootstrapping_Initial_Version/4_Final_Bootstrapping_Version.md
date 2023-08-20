# Final Bootstrapping Version

With the base syntax implemented and the ability to reference external files, it's now possible to assemble a version capable of building the main codebase. Unlike previous steps in the bootstrapping process, the script produced takes no arguments. When run, it will produce a full version of the `tome` executable, after which you should be capable of running `tome build`.

## Project Relative Paths

The main feature still lacking is a notion of project relative paths. This is a simplified version of the logic defined in [the section on the project context](/3_Project_Structure/1_Context.md).

{#Project context}: s
```python
import re
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
```

## Expanding Macros

With a broader set of files that need to be operated on, a new loop has to be incorporated into the expansion process from the previous stage.

{#Build files}: s
```python
for doc_file in context.values():
    {3_External_Links.md#Build new files}
```

Finding a macro now requires awareness of the overall context, so a new definition of this function is used.

{#Find macro}: s
```python
def find_macro_file(current_file, location):
    path = location["file"]
    if not path:
        path = current_file
    elif path[0] == "/":
        path = context.absolute_path(path)
    else:
        path = Path(current_file).parent / path
```

The rest of the expansion process should be reusable unmodified.

{#4_Final_Bootstrapping_Version.py}: f
```python
<#Project context>
<3_External_links.md#Detect unexpanded macro>
<#Find macro>
<3_External_links.md#Expand line>
<3_External_links.md#Expand code block>
<#Build files>
```
