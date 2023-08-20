# Named Macros

This stage in the bootstrapping process ensures creates a version which supports named macros within the same file. See [the chapter on syntax](/2_Syntax) to learn more about what is supported here.

Keep in mind that this file is designed to be passed to the script created by [1_Starting_Point.md](1_Starting_Point.md), so the named blocks don't have meaning in this context.

## Tracking Macros

Before embarking on parsing the input file, there should be a couple dictionaries to track file and macro definitions:

```python
files = {}
macros = {}
```

## Imports

There are a couple core libraries used throughout the code, which are imported here. While much else may change, it still makes sense for this script to take a single file as input.

```python
import re
import sys
doc_file = sys.argv[1]
```

## File Naming

With named blocks, it's no longer the case that fenced blocks can just be assembled in order. See the [page on macro expansion](/2_Syntax/3_Expanding_Macros.md) for more information on the syntax.

```python
def record_block(descriptor, code):
    match = re.match(r"^{#([^}#]+)}: (.)", descriptor)
    name = match[1]
    type = match[2]
    if type == "s":
        macros[name] = code
    elif type == "f":
        files[name] = code
```

## Line Processing

Processing a line has become more complicated, as now it must be deferred until a code block is complete before recording it somewhere for later use. Now the logic accumulates that information in a variable for later use instead of writing immediately. Furthermore, the descriptor immediately preceding that block must also be tracked.

```python
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

## Detecting Unexpanded Macros

Within a block of code, it's necessary to identify what macros are unexpanded and where they are. Earlier the code was broken into individual lines to make some logic during the expansion process easier, this makes a line a more appropriate choice here than the full block.

```python
def detect_unexpanded_macro(line):
    return re.match(r".*(<#([^>]+)>).*", line)
```

## Expanding Lines

To expand a macro, the position of the match must be used. Additionally, [prefixes and suffixes are added to each line](/2_Syntax/3_Expanding_Macros.md#prefixes-and-suffixes).

```python
def expand_line(line):
    lines = []
    match = detect_unexpanded_macro(line)
    if match:
        for macro_line in macros[match[2]]:
            new_line = line[:match.start(1)] + macro_line + line[match.end(1):]
            lines.append(re.sub(r"\n+$", "\n", new_line))
        return expand_code(lines)
    else:
        return [line]
```

Another nuance is that the return value of `readlines` included a trailing `\n`, which will get duplicated for any expansion. Since the original input was broken up by line, it's safe to normalize that to a single newline.

## Expanding Code Blocks

Expansion lends itself to a recursive solution, primarily because of the need to support arbitrary depth. An iterative solution would need a final pass to confirm that there are no additional expansions needed, but going depth first feels a bit more natural. Note that this is primarily stylistic, both approaches probably have the same algorithmic complexity.

```python
def expand_code(code):
    if not code:
        return []
    return expand_line(code[0]) + expand_code(code[1:])
```

## Expanding Files

Finally, to output actual files, each file detected earlier is expanded and written. Adding some feedback so the user knows what files are generated as well.

```python
for file in files:
    print(f"Generating file: {file}")
    open(file, "w").writelines(expand_code(files[file]))
```
