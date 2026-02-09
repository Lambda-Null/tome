# Writing Files

In order to write the files specified throught the project, each markdown file must have its file macros extracted and expanded. Ultimately this means that the path and contents of these files must be coupled, along with if the file must be made executable.

`{#/build/output_file.py}: f`
```python
class OutputFile():
    def __init__(self, path, executable, contents):
        self.path = path
        self.executable = executable
        self.contents = contents

    <#Output file functions>
```

`{#Imports}: m`
```python
from output_file import OutputFile
```

Because of the possibility of macros in other files, all must have their macros catalogued and associated in the context prior to any expansion.

`{#Parser functions}: m`
```python
def catalog_all_files(self):
    macros = {}
    for project_path, full_path in self.context:
        macros[project_path] = self.catalog_macros(full_path)
    return macros
```

Each files outputs need to be accumulated separately and collated for the [build command](/1_CLI/2_Build.md).

`{#Parser functions}: m`
```python
def output_files(self):
    self.macros = macros = self.catalog_all_files()

    files = []
    for project_path, system_path in self.context:
        <#Accumulate outputs for file>

    <#Process output files>

    return files
```

Multiple files can reference the same output file, so those need to be combined to avoid overwriting later in the process.

`{#/test/test_writing_files.py}: f`
```
from parser import Parser
from context.file import FileContext
from unittest import TestCase
from pathlib import Path
import os

class WritingFilesTest(TestCase):
    def test_output_files_are_not_duplicated(self):
        c = FileContext(Path(os.environ["PROJECT_ROOT"]))
        p = Parser(c)
        self.assertEqual(
            1,
            len([file for file in p.output_files() if file.path == c.absolute_path("/.tome/requirements.txt")]),
        )
```

`{#Process output files}: m`
```
file_hash = {}
for file in files:
    if file.path in file_hash:
        file_hash[file.path].contents += file.contents
    else:
        file_hash[file.path] = file
files = file_hash.values()
```

Files can have multiple output files, which each need to be expanded separately. There are a few considerations to keep in mind when identifying the path of the new file:

* Absolute paths are relative to the project root
* Relative paths are relative to the markdown file

`{#Accumulate outputs for file}: s`
```python
for output_file in macros[project_path].files():
    path = output_file.name
    if path[0] == "/":
        path = self.context.absolute_path(self.context.relative_path(Path(project_path), path))
    else:
        path = system_path.parent / path
    files.append(OutputFile(
        path,
        output_file.mode == "f+x",
        self.expand_macros(output_file.lines, project_path, [output_file.name])
    ))
```

When writing output files, it's important to keep in mind that it could be specified as executable. The command line version of `chmod` can just use `a+x`, but Python's more complicated to do the equivalent.

`{#Output file functions}: m`
```python
def write(self):
    self.path.parent.mkdir(parents=True, exist_ok=True)
    self.path.write_text("\n".join(self.contents) + "\n")
    if self.executable:
        self.path.chmod(self.path.stat().st_mode | 0o111)
```
