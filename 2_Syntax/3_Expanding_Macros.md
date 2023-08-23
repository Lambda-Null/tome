# Expanding Macros

Expansion of Macros can be a relatively complex subject, it's significantly more complicated than just looking one up that was cataloged in [section 2](2_Cataloging_Macros.md). Here are the main complexities that must be dealt with:

* Replacing multiple macros on the same line
* Applying a prefix and suffix to each line
* Pulling in macros from other files

At a high level, the macro expansion process replaces instances of `<...#...>` with the macro that pattern represents. This will happen on a line by line basis, recursively expanding until no more are found.

The link syntax provides a solution to a problem in other markdown-based Literate Programming tools. They either treat all macros as valid anywhere or make cross-reference between files impossible, limiting your ability to break more complex programs into multiple pages of exposition. Think of each page as a namespace, and the part of the link preceding the `#` as the full qualification necessary to get at the definitions in that namespace.

## Recursive Solution

The following information is necessary for this process to be successful:

* The code that needs to be expanded, broken up into lines
* The full path of the file currently being expanded, so the `MacroRegistry` defined in [section 2](2_Cataloging_Macros.md) can be used for local expansion
* A list of the stack of macros already evaluated to detect infinite recursion

`{#Parser functions}: m`
```python
def expand_macros(self, lines, file, expanded):
    if not lines:
        return lines
    result = []
    for line in lines:
        result += self.expand_line(line, file, expanded)
    return result
```

Macro expansion takes the form `<path#name>`, which is pretty easy to pick out with a regular expression. The result of such a match can be pretty opaque, though, so the return value is converted to a dictionary.

`{#Parser functions}: m`
```python
def detect_macro(self, line, file):
    result = re.search(r"<(([^>#]*)#([^>#]+))>", line)
    if result:
        return {
            "start": result.start(),
            "end": result.end(),
            "identifier": result.group(1),
            "path": result.group(2) and self.context.resolve_relative_path(Path(file), result.group(2)),
            "name": result.group(3),
        }
```

The actual expansion of a line varies depending on if a macro was found. Even if it's not, other functions are still expecting this function to return a list.

`{#Parser functions}: m`
```python
def expand_line(self, line, file, expanded):
    location = self.detect_macro(line, file)
    if location:
        <#Expand macro for a line>
    else:
        return [line]
```

Before doing anything else, if there's a circular reference it's important to bail out at this point.

`{#Expand macro for a line}: m`
```python
if location["identifier"] in expanded:
    raise Exception(f"Circular reference detected for macro {location['identifier']}")
```

The macro can either be local to the current file or a path to another file. Either way, the context should have it associated with the path. When expanding macros in other files, though, the namespace used must be the one in that file instead of the current one.

`{#Imports}: m`
```python
from pathlib import Path
```

`{#Expand macro for a line}: m`
```python
macro_file = location["path"] or file
macros = self.context.macros[str(self.context.resolve_relative_path(Path(file), macro_file))]
macro = macros.request(location["name"])
```

## Prefix and Suffix Handling {#prefix-and-suffix}

Any prefix and suffix around the macro expansion needs to be applied to each line. This is a really cool feature inspired by [Knot](https://github.com/mqsoh/knot), and is absolutely vital in languages with significant whitespace.

`{#Expand macro for a line}: m`
```python
prefix = line[:location["start"]]
suffix = line[location["end"]:]
lines = []
for mline in self.expand_macros(macro.lines, macro_file, expanded + [location["identifier"]]):
    lines.append(prefix + mline + suffix)
return lines
```
