# Building Tome Context

A context is a set of files that need to be operated on together. Initially this will be all of the Markdown files below the directory provided to the constructor, but the library leaves the possibility of additional files being added.

The library can be imported like this:

`{#Import}: s`
```python
from context import tome_context
```

Establishing the context from the project root is fairly common, which can be done like this:

`{#Within project context}: s`
```python
<#Import>
with tome_context() as context:
```

## Identifying the Root Directory

As mentioned above, identifying the project root is almost always how this class will be used. Although the general constructor should remain generic, a factory method that normalizes that particular use case is convenient.

`{#/build/context/__init__.py}: f`
```python
from context.file import FileContext
from context.staged import StagedContext
from pathlib import Path

from contextlib import contextmanager
import tempfile

@contextmanager
def tome_context():
    with tempfile.TemporaryDirectory() as staged_path:
        <#Search up from current directory for .tome>
        staged_context = StagedContext(
            FileContext(path),
            Path(staged_path),
            [r"^/(build|test)/"]
        )
        yield staged_context
```

As outlandish as this is, the root directory could feasibly be a Tome project. Not sure what that would look like, but to leave that open as possibility the condition has to come at the end of the loop.

`{#Search up from current directory for .tome}: s`
```python
path = Path.cwd()
while True:
    if (path / ".tome").exists():
        break
    if path.parent == path:
        raise Exception("Cannot locate the project root")
    path = path.parent
```

Other options were considered for identifying the project root, such as presence of a README or version control. While these are possible, it also opens the possibility of acting on a really large set of files, which could be dangerous.

