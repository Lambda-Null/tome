# External Links

Up until now code has had to be thrown away in subsequent stages, but this stage provides the tools necessary for reuse. As a result, more features can be included at this stage without having to reimplement logic.

## Program Structure

The order of the markdown file is finally not forced. This allows creation of a couple classes to better organize the logic.

`{#3_External_Links.py}: f`
```python
import re
import os

<#File class>
<#Process arguments>
<#Macro class>
<#Expand macro functions>
<#Build new files>
```

## Processing Arguments

Now that multiple files can be referenced, it is necessary to track any files referenced in addition to the one provided as an argument.

`{#Process arguments}: s`
```python
import sys
doc_file = sys.argv[1]
files = { doc_file: File(doc_file) }
```

## File Organization

With the expansion into separate files, it's becoming more relevant to keep track of the individual files. Having a class as a box for things to operate in helps keep these namespaces separate. On top of the file name, it's also important to track the code blocks involved.

`{#File class}: s`
```python
class File():
    def __init__(self, file_name):
        self.file_name = file_name
        self.macros = {}
        self.file_lines = []

    <#Cache file lines>
    <#Catalog code blocks>
```

Putting I/O in the constructor can be troublesome for testing, so instead it will happen in a function that caches its results.

`{#Cache file lines}: s`
```python
def lines(self):
    if not self.file_lines:
        self.file_lines = open(self.file_name, "r")
    return self.file_lines
```

The overall shape of the cataloging of code blocks remains relatively unchanged.

`{#Catalog code blocks}: s`
```python
def catalog_code_blocks(self):
    macro = None
    previous_line = None
    for line in self.lines():
        line = line.removesuffix("\n")
        <#Process line>
```

The actual accumulation of lines becomes more natural, now that macros are the ones collating the lines.

`{#Process line}: s`
```python
if re.match(r"^```", line):
    <#Identify macro>
else:
    if macro:
        macro.add_code(line)
previous_line = line
```

Now that a file can be referenced several times, though, existing macros have to be reused. The current design means a macro object is unnecessarily created in this case, the full program has a more elegant design that should eventually be retrofitted into this logic.

`{#Identify macro}: s`
```python
if macro:
    macro.end_block()
    macro = None
else:
    macro = Macro.build(previous_line)
    if macro:
        if macro.name in self.macros:
            macro = self.macros[macro.name]
        else:
            self.macros[macro.name] = macro
```

## Different Kinds of Macros

The full program didn't end up needing inheritance, so doing so here is probably a bit heavy handed. The design used there should eventually be retrofitted into this logic as well.

`{#Macro class}: s`
```python
class Macro():
    <#Macro factory>
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.code_block = []

    <#Add line>
    <#End block>

<#SingleMacro class>
<#MultiMacro class>
<#FileMacro class>
```

In [2_Named_Macros.md](2_Named_Macros.md), the `{#foo}: *` form was introduced to name macros. This will need to be reimplemented here, along with an additional mode which can be defined multiple times and accumulates what's defined. Separate child classes creates the need for a factory method for the classification step.

`{#Macro factory}: s`
```python
def build(descriptor):
    match = re.match(r"^`{#([^#>]+)}: (m|s|f(\+x)?)`", descriptor)
    if not match:
        return None
    name = match[1]
    mode = match[2]
    match mode:
        case "s":
            return SingleMacro(name)
        case "m":
            return MultiMacro(name)
        case "f":
            return FileMacro(name)
        case "f+x":
            return FileMacro(name, True)
```

Adding lines is going to happen separately, as the behavior needs to be overridden for `SingleMacro`.

`{#Add line}: s`
```python
def add_code(self, line):
    self.code_block.append(line)
```

When a block is finished processing, some of the children classes will sometimes need a hook to execute specific behavior:

`{#End block}: s`
```python
def end_block(self):
    pass
```

### Single Macro

Once the first code block is processed, the single macro needs raise an error if additional definitions are attempted.

`{#SingleMacro class}: s`
```python
class SingleMacro(Macro):
    def __init__(self, name):
        super().__init__("single", name)
        self.closed = False

    def add_code(self, line):
        if self.closed:
            raise Exception(f"Code block {name} has already been defined")
        super().add_code(line)

    def end_block(self):
        self.closed = True
```

### Multi Macro

The Multi Macro actually doesn't have any special behavior, but it's important to name this concept separately for clarity and consistency.

`{#MultiMacro class}: s`
```python
class MultiMacro(Macro):
    def __init__(self, name):
        super().__init__('multi', name)
```

### File Macro

File Macros behave mostly like `MultiMacro`, but need to keep track of if they will ultimately produce executable files.

`{#FileMacro class}: s`
```python
class FileMacro(Macro):
    def __init__(self, name, executable = False):
        super().__init__('file', name)
        self.executable = executable
```

## Expanding Macros

The recursive expansion in [2_Named_Macros.md](2_Named_Macros.md) worked quite well, so that strategy will be repeated here.

`{#Expand macro functions}: s`
```python
<#Detect unexpanded macro>
<#Find macro>
<#Expand line>
<#Get file name>
<#Expand code block>
```

### Expanding Lines

Many of these functions will take a filename in addition to the code that needs to be expanded. This is necessary to ensure that other files which also have macros to be expanded do so in their namespace.

`{#Detect unexpanded macro}: s`
```python
def detect_unexpanded_macro(line):
    result = re.search(r"<([^#]*)#([^>#]+)>", line)
    if result:
        return {
            "file": result[1],
            "name": result[2],
            "start": result.start(),
            "end": result.end(),
        }
```

One line could explode into many, so line expansion must return a list. If the line contains no macros, though, it still needs to return the original input.

`{#Expand line}: s`
```python
def expand_line(file, line):
    result = detect_unexpanded_macro(line)
    if result:
        <#Apply macro to line>
    else:
        return [line]
```

Since other files could be referenced, the form `<#...>` must expand to allow `<...#...>`. On top of that, returning a regexp object requires other code have too intimate knowledge of how this operates, so shifting to a data structure.

`{#Find macro}: s`
```python
def find_macro_file(current_file, location):
    file = location["file"] or current_file
    result = files.get(file, File(file))
    if not result.macros:
        result.catalog_code_blocks()
    return result
```

As discussed elsewhere, the prefix and suffix around the macro are applied to each line of the macro.

`{#Apply macro to line}: s`
```python
lines = []
macro_file = find_macro_file(file, result)
macro = macro_file.macros[result["name"]]
if not macro:
    raise Exception(f"Macro not found: {macro}")
for macro_line in macro.code_block:
    new_line = line[:result["start"]] + macro_line + line[result["end"]:]
    lines.append(re.sub(r"\n+$", "\n", new_line))
return expand_code(macro_file.file_name, lines)
```

### Expanding Code Blocks

The recursion is actually quite simple, all of the heavy lifting was taken care of in the line expansion.

`{#Expand code block}: s`
```python
def expand_code(file, code):
    if not code:
        return []
    return expand_line(file, code[0]) + expand_code(file, code[1:])
```

## Expanding Files

The only files that should be created are the ones related to the `doc_file` provided. Externally referenced files might cause trouble during the bootstrapping process.

`{#Build new files}: s`
```python
files[doc_file].catalog_code_blocks()
for file_macro in [m for m in files[doc_file].macros.values() if m.type == "file"]:
    print(f"Generating file: {file_macro.name}")
    file_name = get_file_name(file_macro)
    open(file_name, "w").writelines([line + "\n" for line in expand_code(doc_file, file_macro.code_block)])
    if file_macro.executable:
        os.chmod(file_name, os.stat(file_name).st_mode | 0o111)
```

The file writing logic will need to be different in the next stage, so breaking that out into a function that can be pulled in separately.

`{#Get file name}: s`
```python
def get_file_name(file_macro):
    return file_macro.name
```
