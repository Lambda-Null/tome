# Syntax

If you're unfamiliar with Markdown, the first thing to do is to go through a tutorial such as [this one](https://www.markdownguide.org/). Here's what's covered in this chapter:

* [Section 1 - Code Blocks](1_Code_Blocks.md)
* [Section 2 - Cataloging Macros](2_Cataloging_Macros.md)
* [Section 3 - Expanding Macros](3_Expanding_Macros.md)
* [Section 4 - Writing Files](4_Writing_Files.md)

This README ties the functionality described in each of those sections together into a single `Parser` class that can be used throughout the rest of the project. On top of that, the construction of this class serves as an introduction to Tome's syntax.

## Introduction to Tome's Syntax

Consider the parsing library for Tome. It uses [Marko](https://marko-py.readthedocs.io/en/latest/) to parse Markdown, so the file is started like this:

`{#dependencies}: m`
```
marko==2.0.0
```

`{#/build/parser.py}: f`
```python
import marko
```

When Tome encounters this, it produces the file `/build/parser.py` relative to the top level directory of this repository. To learn more about code blocks specifically, check out [section 1](1_Code_Blocks.md). The `f` describes how to interpret this block, in this case as a file.

It's also valid to to name a code block for later reuse, called a macro, like this:

`{#Parse file using Marko}: s`
```python
marko.parse(path.read_text())
```

In this case, the `s` indicates that the contents of the code block can only be defined once, and can be referenced in other code blocks in this way:

`{#Function to parse a file}: s`
```python
def parse_file(self, path):
    return <#Parse file using Marko>
```

If the same filename is reused, subsequent code blocks will add to the end of what's already there:

`{#/build/parser.py}: f`
```python
<#Imports>

class Parser():
    <#Function to parse a file>
    <#Parser Functions>
```

Notice that something else subtle happened there, the indentation from both lines of the `parse_file` were used. In general, anything before and after the reference to a macro get prepended and appended to each line of that macro.

The `s` used thus far can only be defined once, if they were to be defined a second time Tome would throw an error. To continue adding to the same macro repeatedly like with files, use `m` instead.

`{#Parser Functions}: m`
```python
def __init__(self, context):
    self.context = context
```

The argument relates to the [project context](/3_Project_Structure/1_Context.md) which is covered in [chapter 3](/3_Project_Structure/README.md). Since `Parser Functions` was defined with `m`, though, additional functions can also be added. You can find more information about macros in [section 2](2_Cataloging_Macros.md), which also defines other functions that will be needed.

`{#Parser Functions}: m`
```python
<2_Cataloging_Macros.md#Parser functions>
```

This also demonstrates how to use macros defined in other files, which is covered in more detail in [section 3](3_Expanding_Macros.md). In fact, all of the sections in this chapter define functions for this class.

`{#Parser Functions}: m`
```python
<1_Code_Blocks.md#Parser functions>
<3_Expanding_Macros.md#Parser functions>
<4_Writing_Files.md#Parser functions>
```

Some of those files will also need to import additional libraries for some of their logic.

`{#Imports}: s`
```python
<1_Code_Blocks.md#Imports>
<2_Cataloging_Macros.md#Imports>
<3_Expanding_Macros.md#Imports>
<4_Writing_Files.md#Imports>
```

Defining a macro used by other files looks no different from one defined for local use:

`{#Import}: s`
```python
from parser import Parser
```

This enables other files to import the class defined here.
