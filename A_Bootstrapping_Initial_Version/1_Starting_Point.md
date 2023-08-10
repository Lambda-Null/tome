# Starting Point

It's always difficult to know where to start with a project like this. The issue is that the very first logic will need to be assembled by hand, but this should be as little as possible. Furthermore, after the first tangle, no hand assembly should ever be necessary again.

This file should be easy to assemble by hand, resulting in a standalone program. That program is only guaranteed to tangle this file and [2_Named_Blocks.md](2_Named_Blocks.md) in this directory. From that point on, each file produces a program which is capable of assembling the one that follows it numerically.

## A Simplistic Approach

To keep things simple at this stage, we're going to assume that fenced code blocks are sequentially assembled into a program. Furthermore, the file created will be a python script bearing the same name. Since the resulting file will be the only checked in code, I'll include a preamble explaining the situation.

```python
# This script should be the only code directly checked in to the
# codebase. It was generated from 1_Starting_Point.md, see read that
# page to better understand this script.
```

Complicated argument structure is another thing we can dispense with, all this program needs to do is take the name of the file it's provided.

```python
import sys
doc_file = sys.argv[1]
```

We also need to know the new file name:

```python
import re
code_file = re.sub(r"[.]md$", ".py", doc_file)
```

There are certainly lots of options for parsing Markdown, but they're separate packages and dependency management is beyond purview of this stage of the bootstrapping process. Once again, we'll keep it simple by walking line by line through the file, assuming any line starting with a triple backtick flips the mode of operation.

```python
with open(code_file, "w") as f:
    writing = False
    for line in open(doc_file, "r").readlines():
        if re.match(r"^```", line):
            writing = not writing
        elif writing:
            f.write(line)
```
