# File Context

The simplest type of context is one which simply is aware of files beneath a particular directory.

`{#/build/context/file.py}: f`
```
from context.base import Context
import re

class FileContext(Context):
    def __init__(self, project_root):
        self.project_root = project_root

    <#Context functions>
```

A path in the local operating system is provided when files are added, but absolute paths within the markdown files will be in relation to the project root.

`{#Convert system path to project path}: s`
```python
f"/{file.absolute().relative_to(self.project_root)}"
```

`{#Context functions}: m`
```python
def convert_system_path_to_project_path(self, file):
    return f"/{file.absolute().relative_to(self.project_root)}"
```

Iterating over the context needs to communicate both the absolute path and the one relative to the project root.

`{#Context functions}: m`
```python
def __iter__(self):
    return iter({
        self.convert_system_path_to_project_path(file): file.absolute()
        for file in self.project_root.glob("**/*.md")
    }.items())
```

## Project Path Resolution

Determining the absolute path has a few components Any relative paths that are provided need to be resolved, and for that a reference path is necessary.

`{#Context functions}: m`
```python
def relative_path(self, reference, project_path):
    if not reference.is_dir():
        reference = reference.parent
    return (reference / project_path).resolve()
```

When other parts of the codebase need to interact with a file, they need to be aware of the absolute path to use. This of course will be different depending on if the file is staged.

`{#Context functions}: m`
```python
def absolute_path(self, project_path):
    return self.project_root / re.sub(r"^/", "", str(project_path))
```
