# Named Macros

A version of this program which allows named macros to be expanded would greatly expand our capabilities for subsequent stages of the bootstrap process. It's a core feature of literate programming, and will allow subsequent phases to be tangled in a more natural manner.

## Links as Macros

When we think about the concept of macros, they essentially have a definition and places that reference that definition. This is precisely the same relationships that links have, so we can think of macros simply as links within code. Since we're in the midst of bootstrapping, though, this behavior will be considerably constrained:

* Fenced blocks preceded by a label definition `[like this]:`
* Angle bracket style links to those definitions `<#like this>`

Keep in mind that this file is designed to be run by <1_Starting_Point.md>, so the named blocks don't have meaning in this context. If blocks are named, it's because they're reused by later stages in the bootstrapping process.

## Tracking Macros

Before embarking on parsing the input file, there should be a couple dictionaries to track file and macro definitions:

```python
files = {}
macros = {}
```

## Keeping a Single File

While much else may change, it still makes sense for this script to take a single file as input.

```python
import sys
doc_file = sys.argv[1]
```

## File Naming

With named blocks, it's no longer the case that fenced blocks can just be assembled in order. It therefore becomse necessary to come up with a syntax for indicating that the described block will become the named file. Since `[this]:` defines a block that's expanded within the document, perhaps `<this.py>:` is a good way to define a block expanded outside of the document.

```python
def record_block(descriptor, code):
    match = re.match(r"^(.)([^]]+).:", descriptor)
    type = match[1]
    name = match[2]
    if type == "[":
        macro[name] = code
    elif type == "<":
        file[name] = code
```

## Line Processing

Processing a line has become more complicated, as now we need to wait until a code block is complete before recording it somewhere for later use. It still needs to track if its in a code block, but now it accumulates that information in a variable for later use instead of writing immediately. Furthermore, it also must be aware of the descriptor immediately preceding that block.

```python
with open(code_file, "w") as f:
    descriptor = ""
    current_block = None
    in_code = False
    for line in open(doc_file, "r").readlines():
        if re.match(r"^```", line):
            in_code = not in_code
            if in_code:
                current_block = []
            else:
                record_block(descriptor, current_block)
        elif in_code:
            current_block.append(line)
        else:
            descriptor = line
```

Eventually this probably makes more sense handled as a class, but the significant whitespace in Python poses a problem for this stage in the bootstrapping.

## Detecting Unexpanded Macros

Within a block of code, it's necessary to identify what macros are unexpanded and where they are. Earlier the code was broken into individual lines to make some logic during the expansion process easier, this makes a line a more appropriate choice here than the full block.

```python
def detect_unexpanded_macro(line):
    return re.match(r".*(<#([^>]+)>).*", line)
```

## Expanding Lines

To expand a macro, the position of the match must be used. Rather than the naive expansion usually seen, though, I'm going to draw inspiration from [Knot](https://github.com/mqsoh/knot) and treat what's preceding and following the macro as a prefix and suffix for each line in the expansion. This may seem like a big feature to include in such an early phase in the bootstrapping process, but because Python has significant whitespace it's important for maintaining correct indentation during expansion.

```python
def expand_line(line):
    lines = []
    match = detect_unexpanded_macro(line)
    if match:
        for macro_line in macros[match[2]]:
            lines.append(line[:match.start(1)] + macro_line + line[match.end(1):])
        return lines
    else:
        return [line]
```

## Expanding Code Blocks

Expansion lends itself to a recursive solution, primarily because of the need to support arbitrary depth. An iterative solution would need a final pass to confirm that there are no additional expansions needed, but going depth first feels a bit more natural. Note that this is primarily stylistic, both approaches probably have the same algorithmic complexity.

```python
def expand_code(code):
    if not code:
        return []
    return expand_line(code[0]) + expand_code(code[1:])
```

## Expanding Files

Finally, to output actual files, each file detected earlier is expanded and written.

```python
for file in files:
    open(file, "w").writelines(expand_code(files[file]))
```
