# Macros

For those unfamiliar, a [macro](https://en.wikipedia.org/wiki/Macro_(computer_science)) is an abbreviated description of a larger block of text. They aren't as common in newer programming languages, but the name has a long history in Literate Programming and is relevant to how Tome operates.

[Section 1](1_Code_Blocks.md) covered how code blocks are detected and associated with a name. This section deals with how they're cataloged. Expansion of those macros, including how macros in other files are pulled in, is covvered in [section 3](3_Expanding_Macros.md).

## Links as Macros

Macros essentially have a definition and places that reference that definition. Links follow a similar pattern, so macros in Tome extend the link syntax of Markdown.

* Descriptors share the `{#...}` syntax with [heading anchors](https://www.markdownguide.org/extended-syntax/#heading-ids), although need to be quoted in `` `s to avoid funny rendering such as underscores in a filename
* [Angle brackets](https://www.markdownguide.org/basic-syntax/#urls-and-email-addresses) are used to reference those definitions `<#like this>`

Neither of these forms are strictly valid markdown, but they follow the semantic meaning nicely enough to feel natural building a project using them.

## Types of Macros

The different types of macros serve different purposes, going to contain that in a class called `Macro`. It's tempting to create an inheritance hierarchy out of the different possibilities, but because there are so few the logic navigating that hierarchy would exceed the benefits.

`{#/build/macro.py}: f`
```python
class Macro():
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.code_blocks = 0
        self.lines = []

    <#Base functions>
```

Since many macros have the ability to be specified multiple times, adding code as a separate function is the lowest common denominator. Marko provides the text within these blocks newlines and all, so that will have to split apart so a prefix and suffix can be added to each line later on. This includes a trailing newline that needs to be trimmed, but only one as any additional trailing whitespace needs to be retained.

`{#Base functions}: m`
```python
def add_code(self, code):
    self.lines += code.removesuffix("\n").split("\n")
    <#Handle validation of "s" mode>
```

In the case of `s`, this also needs to throw an error if called after the first code block is added. This could have been handled with a boolean, but a count could provide additional functionality later on.

`{#Handle validation of "s" mode}: s`
```python
self.code_blocks += 1
if self.mode == "s" and self.code_blocks > 1:
    raise Exception(f"Macro {self.name} received a second code block with mode {self.mode}")
```

## Organizing by Name

The organization of macros has many different responsibilities:

* Connect macro names to their objects
* Provide a list of files that need to be generated
* Reuse macros which have already been registered instead of creating new ones

All of these factors will be collected into a single class:

`{#/build/macro_registry.py}: f`
```python
<#Macro imports>

class MacroRegistry():
    def __init__(self, source):
        self.source = source
        self.macros = {}

    <#Registry functions>
```

To deal with the potential appending nature of some macros, it needs a function that either finds or creates a new macro.

`{#Registry functions}: m`
```python
def request(self, name, mode = None):
    macro = None
    if name in self.macros:
        macro = self.macros[name]
        <#Validate macro>
    else:
        <#Create new macro>
        self.macros[name] = macro
    return macro
```

If the macro retrieved has a different mode than the one described, this is an inconsistency that might cause problems during generation. Also allowing the mode to remain unspecified, so the logic can be reused during macro expansion. The logic that parsed the line initially is responsible for ensuring that mode is present.

`{#Validate macro}: s`
```python
if mode and macro.mode != mode:
    raise Exception(f"Macro {name} has an inconsistent mode")
```

Creation of the Macro should only happen if the mode is specified. If it's not, that suggests the system got to expansion without defining that macro. File names are just as valid for expansion as other macros, it might not be very likely but there's not a good reason to limit that ability.

`{#Macro imports}: m`
```python
from macro import Macro
```

`{#Create new macro}: s`
```python
if not mode:
    raise Exception(f"Macro `{name}` was never created for `{self.source}`")
macro = Macro(name, mode)
```

During generation, just the files will need to be pulled out as a starting point for expansion.

`{#Macro imports}: m`
```python
import re
```

`{#Registry functions}: m`
```python
def files(self):
    return [macro for macro in self.macros.values() if re.match(r"^f", macro.mode)]
```

## Accumulating Macros

At this point, all of the pieces are necessary to pull macros in a file out and store them. This incorporates several functions defined in the preceding sections.

`{#Parser functions}: m`
```python
def catalog_macros(self, path):
    registry = MacroRegistry(path)
    for code_block in self.extract_code_blocks(self.parse_file(path)):
        descriptor = code_block["descriptor"]
        macro = registry.request(descriptor["name"], descriptor["mode"])
        macro.add_code(code_block["code"])
    return registry
```

## External References

Other files can include this macro to import the library:

`{#Imports}: s`
```python
from macro_registry import MacroRegistry
```
