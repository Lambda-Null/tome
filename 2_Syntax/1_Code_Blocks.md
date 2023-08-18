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

{#ParserFunctions}: m
```python
def extract_text(self, element):
    if isinstance(element, str):
        return element
    return "\n".join([extract_text(child) for child in element.children])
```

## Descriptors

Extracting code blocks should only happen if the preceding line is a valid descriptor. A descriptor will always start with `[...]:`, but the characters following that describe how it should be used:

* `f`: Write this block to the named file
* `f+x`: Write this block to the named file as executable
* `s`: Save this block as a macro to be referenced elsewhere, the name can only be used once
* `m`: Save this block as a macro as well, but the name can be used more than once

Handling how the behavior between these modes will be covered in [section 2](2_Macros.md), but parsing out the relevant information will be covered here.

[Parser Functions]: m
```python
def parse_descriptor(self, descriptor):
    foo
```



Indented:

    foo 1
    foo 2

    foo 3

Backticks:

```
bar 1
bar 2
bar 3
```

Tilde:

~~~
baz 1
baz 2
baz 3
~~~

