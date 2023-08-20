# Writing Files

In order to write the files specified throught the project, each markdown file must have its file macros extracted and expanded. Ultimately this means that the path and contents of these files must be coupled, along with if the file must be made executable.

{#/build/output_file.py}: f
```python
class OutputFile():
    def __init__(self, path, executable, contents):
        self.path = path
        self.executable = executable
        self.contents = contents

    <#Output file functions>
```

{#Imports}: m
```python
import output_file
```

Because of the possibility of macros in other files, all must have their macros catalogued and associated in the context prior to any expansion.

{#Parser functions}: m
```python
def catalog_all_files(self):
    for project_path, full_path in self.context.files.items():
        self.context.associate_macro(project_path, self.catalog_macros(full_path))
```

Each files outputs need to be accumulated separately and collated for the [build command](/1_CLI/2_Build.md).

{#Parser functions}: m
```python
def output_files(self):
    self.catalog_all_files()

    files = []
    for file in self.context.files:
        {#Accumulate outputs for file}

    return files
```

Files can have multiple output files, which each need to be expanded separately.

{#Accumulate outputs for file}: s
```python
for output_file in self.context.macros[file].files():
    files.append(OutputFile(
        self.context.absolute_path(output_file.name),
        output_file.mode == "f+x",
        expand_macros(output_file.lines, file, [output_file.name])
    ))
```

When writing output files, it's important to keep in mind that it could be specified as executable. The command line version of `chmod` can just use `a+x`, but Python's more complicated to do the equivalent.

{#Output file functions}: m
```python
def write(self):
    self.path.parent.mkdir(parents=True, exist_ok=True)
    self.path.write_text(self.contents)
    if self.executable:
        self.path.chmod(file_path.stat().st_mode | 0o111)
```
