# Expanding Macros

Expansion of Macros can be a relatively complex subject, it's significantly more complicated than just looking one up that was cataloged in [section 2](2_Cataloging_Macros.md). Here are the main complexities that must be dealt with:

* Replacing multiple macros on the same line
* Applying a prefix and suffix to each line
* Pulling in macros from other files

At a high level, the macro expansion process replaces instances of `<...#...>` with the macro that pattern represents. This will happen on a line by line basis, recursively expanding until no more are found.

The following information is necessary for this process to be successful:

* The code that needs to be expanded, broken up into lines
* The full path of the file currently being expanded, so the `MacroRegistry` defined in [section 2](2_Cataloging_Macros.md) can be used for local expansion
* A list of the stack of macros already evaluated to detect infinite recursion

{#Parser functions}: m
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

{#Parser functions}: m
```python
def detect_macro(self, line):
    result = re.search(r"<([^>#]*)#([^>#]+)>", line)
    if result:
        return {
            "start": result.start(),
            "end": result.end(),
            "path": result.group(1),
            "name": result.group(2),
            "identifier": f"{location["path"]}#{location["name"]}",
        }
```

The actual expansion of a line varies depending on if a macro was found. Even if it's not, other functions are still expecting this function to return a list.

{#Parser functions}: m
```python
def parse_line(self, line, file, expanded):
    location = self.detect_macro(line)
    if location:
        <#Expand macro for a line>
    else:
        return [line]
```

Before doing anything else, if there's a circular reference it's important to bail out at this point.

{#Expand macro for a line}: m
```python
if identifier in expanded:
    raise Exception(f"Circular reference detected for macro {location['identifier']}")
```

The macro can either be local to the current file or a path to another file. Either way, the context should have it associated with the path.

{#Expand macro for a line}: m
```python
macros = self.context.macros[location["path"] or file]
```

Any prefix and suffix around the macro expansion needs to be applied to each line. This is a really cool feature inspired by [Knot](https://github.com/mqsoh/knot), and is absolutely vital in languages with significant whitespace.

{#Expand macro for a line}: m
```python
prefix = line[:location["start"]]
suffix = line[location["end"]:]
lines = []
for mline in expand_macros(macros[location["name"]], file, expanded + [location["identifier"]]):
    lines.append(prefix + mline + suffix)
return lines
```
