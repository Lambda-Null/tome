# External Links

Names defined across files have been a real problem in other Literate Programming tools, they either treat all macros as valid anywhere make cross-reference between files impossible. Programming languages have solved this problem handily with namespaces, and using link syntax as macro expansion provides a natural solution.

Up until now code has had to be thrown away in subsequent stages, but with external references logic in previous stages can start being reused. As a result, more features can be included at this stage without having to reimplement logic repeatedly.

## Program Structure

The order of the markdown file is finally not forced. This allows creation of a couple classes to better organize the logic.

<3_External_Links.py>:
```python
<#File class>
<#Process arguments>
<#Macro class>
<#Build new files>
```

## Processing Arguments

Since the bootstrapping process involves feeding the results of one file into the next, it will continue to make sense to only worry about a single argument for much of this process.

Now that multiple files can be referenced, though, it is necessary to track any other files that are needed.

[Process arguments]:
```python
import sys
doc_file = sys.argv[1]
files = { doc_file: File(doc_file) }
```

## File Organization

With the expansion into separate files, it's becoming more relevant to keep track of the individual files. Having a class as a box for things to operate in helps keep these namespaces separate.

On top of the file name, it's also important to track the code blocks involved. This is another place where I'm still figuring out what it should look like :)

[File class]:
```python
class File:
    def __init__(self, file_name):
        self.file_name = file_name
        self.macros = {}

    <#Cache file lines>
    <#Catalog code blocks>
```

Putting I/O in the constructor can be troublesome for testing, so instead it will happen in a function that caches its results.

[Cache file lines]:
```python
def lines(self):
    if not self.file_lines:
        self.file_lines = open(self.file_name, "r")
    return self.file_lines
```

The overall shape of the cataloging of code blocks remains relatively unchanged.

[Catalog code blocks]:
```python
def code_blocks(self):
    if not self.code_blocks:
        macro = None
        previous_line = None
        for line in self.lines():
            <#Process line>
```

The actual accumulation of lines becomes more natural, now that macros are the ones collating the lines.

[Process line]:
```python
if re.match(r"^```", line):
    <#Identify macro>
else:
    if macro:
        macro.add_code(line)
previous_line = line
```

Now that a file can be referenced several times, though, existing macros have to be reused. The current design means a macro object is unnecessarily created in this case, should probably be redesigned so this doesn't happen.

[Identify macro]:
```python
if macro:
    macro.end_block()
    macro = None
else:
    macro = Macro.build(previous_line)
    if macro.name in self.macros:
        macro = self.macros[macro.name]
    else:
        self.macros[macro.name] = macro
```

## Different Kinds of Macros

Defining Macros as part of the `File` class would end up making that class pretty busy. It also makes it a bit complicated to group the descriptor and code block together.

On top of that, multiple types of macros are beginning to emerge, and inheritance will hopefully help organize their differences more effectively.

[Macro class]:
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

In [2_Named_Macros.md](2_Named_Macros.md), the `[foo]:` and `<foo.py>:` macros were introduced. These will need to be reimplemented here, but also a new macro in the form `(foo):` which can be defined multiple times and accumulates what's defined. As mentioned above, these will be organized as separate child classes, so adding a factory method for the classification step.

[Macro factory]:
```python
def build(descriptor):
    match = re.match(r"^(.)([^<#Descriptor terminators>]+).:", descriptor)
    type_symbol = match[1]
    name = match[2]
    match type_symbol:
        case "[":
            return SingleMacro(name)
        case "(":
            return MultiMacro(name)
        case "<":
            return FileMacro(name)
```

The Regexp was really difficult to read with the terminators embedded, so calling those out here for clarity.

[Descriptor terminators]:
```python
])>
```

Adding lines is going to happen separately, as the behavior needs to be overridden for `SingleMacro`.

[Add line]:
```python
def add_code(self, line):
    self.code_block.append(line)
```

When a block is finished processing, some of the children classes will sometimes need a hook to execute specific behavior:

[End block]:
```python
def end_block(self):
    pass
```

### Single Macro

Once the first code block is processed, the single macro needs raise an error if additional definitions are attempted.

[SingleMacro class]:
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

[MultiMacro class]:
```python
class MultiMacro(Macro):
    def __init__(self, name):
        super().__init__('multi', name)
```

### File Macro

File Macros are more a concept for classification than anything else. Might change that as the rest of the code evolves :)

[FileMacro class]:
```python
class FileMacro(Macro):
    def __init__(self, name):
        super().__init__('file', name)
```

## Expanding Macros

The recursive expansion in [2_Named_Macros.md](2_Named_Macros.md) worked quite well, so that strategy will be repeated here.

[Expand macros]:
```python
<#Detect unexpanded macro>
<#Expand line>
<#Expand code block>
```

### Expanding Lines

Since other files could be referenced, the form `<#...>` must expand to allow `<...#...>`. On top of that, returning a regexp object requires other code have too intimate knowledge of how this operates, so shifting to a data structure.

[Detect unexpanded macro]:
```python
def detect_unexpanded_macro(line):
    match = re.match(r".*(<([^#]*)#([^>]+)>).*", line)
    if match:
        file = doc_file if match[2] == "" else match[2]
        return {
            "file": file,
            "name": match[3],
            "start": match.start(1),
            "end": match.end(1),
        }
```

One line could explode into many, so line expansion must return a list. If the line contains no macros, though, it still needs to return the original input.

[Expand line]:
```python
def expand_line(line):
    match = detect_unexpanded_macro(line)
    if match:
        <#Apply macro to line>
    else:
        return [line]
```

As discussed elsewhere, the prefix and suffix around the macro are applied to each line of the macro.

[Apply macro to line]:
```python
lines = []
for macro_line in files.get(match["file"], File(match["file"])).macros[match["name"]].code_block:
    new_line = line[:match.start(1)] + macro_line + line[match.end(1):]
    lines.append(re.sub(r"\n+$", "\n", new_line))
return expand_code(lines)
```

### Expanding Code Blocks

The recursion is actually quite simple, all of the heavy lifting was taken care of in the line expansion.

[Expand code block]:
```python
def expand_code(code):
    if not code:
        return []
    return expand_line(code[0]) + expand_code(code[1:])
```

## Expanding Files

The only files that should be created are the ones related to the `doc_file` provided. Externally referenced files might cause trouble during the bootstrapping process.

[Build new files]:
```python
<#Expand macros>

for file_macro in [m for m in files[doc_file].macros.values() if m.type == "file"]:
    print(f"Generating file: {file}")
    open(file, "w").writelines(expand_macro
```
