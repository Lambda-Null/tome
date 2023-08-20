# Code Blocks

There are three distinct ways to represent code blocks in Markdown. Marko doesn't represent them all in the same way internally:

* Indentation: `marko.block.CodeBlock`
* Fenced with ` ``` `: `marko.block.FencedCode`
* Fenced with `~~~~`: `marko.block.FencedCode`

To work around this, Tome's parser will need to provide a function to consistently determine if it's looking at a code block.

{#Parser Functions}: m
```python
def is_code_block(self, element):
    return isinstance(element, marko.block.CodeBlock) or  isinstance(element, marko.block.FencedCode)
```

Additionally, below that code block are objects that need to be assembled into the actual text representing the code. Typically it is a single `RawText` child with a `str` as its child, but making this logic robust to changes in that API.

{#Parser Functions}: m
```python
def extract_text(self, element):
    if isinstance(element, str):
        return element
    return "\n".join([extract_text(child) for child in element.children])
```

## Descriptors

Extracting code blocks should only happen if the preceding line is a valid descriptor. A descriptor will always start with `{#...}:`, but the characters following that describe how it should be used:

* `f`: Write this block to the named file
* `f+x`: Write this block to the named file as executable
* `s`: Save this block as a macro to be referenced elsewhere, the name can only be used once
* `m`: Save this block as a macro as well, but the name can be used more than once

Handling how the behavior between these modes will be covered in [section 2](2_Cataloging_Macros.md), but parsing out the relevant information will be covered here.

{#Imports}: m
```
import re
```

{#Parser Functions}: m
```python
def parse_descriptor(self, descriptor):
    match = re.match(r"^{#([^}]+)}: (f(\+x)?|s|m)$", descriptor)
    if match:
        return {
            "name": match[1],
            "mode": match[2],
        }
```

## Coupling

In order to extract code blocks, descriptor lines must be coupled with their corresponding code. Because consecutive lines can be considered part of the same paragraph, the descriptor must also be preceded by a blank line to get picked up by the parser. This is also helpful for visibility, as otherwise various renderers are going to pull it into that paragraph.

{#Parser Functions}: m
```python
def extract_code_blocks(self, parse_tree):
    code_blocks = []
    descriptor = None
    for child in parse_tree.children:
        <#Parse syntax element>
```

The `descriptor` was initialized outside of the loop since state of the previous line has to be tracked. Finding a valid descriptor puts the the next iteration into a mode where it could potentially add to the code blocks.

{#Parse syntax element}: s
```python
if descriptor:
    <#Add to result if child is a code block>
descriptor = self.extract_text(child)
```

Detecting if it's a code block is covered above, using a simple dictionary to represent the pairing of descriptor and code.

{#Add to result if child is a code block}: s
```python
if self.is_code_block(child):
    code_blocks.append({ "descriptor": descriptor, "code": self.extract_text(child) })
```
