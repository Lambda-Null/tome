# Context

A context is a set of files that need to be operated on together. Initially this will be all of the Markdown files below the directory provided to the constructor, but the library leaves the possibility of additional files being added.

The library can be imported like this:

[Import]:
```python
from context import Context
```

Establishing the context from the project root is fairly common, which can be done like this:

[Establish project context]:
```python
<#Import>
context = Context.from_project_root()
```

## Project Context

The library primarily provides a class called `Context`.

</build/context.py>:
```python
<#Dependencies>

class Context():
    <#Context functions>
```

A context will start with all of the files beneath a particular directory. In addition to seeding the directory, the provided root enables [referencing paths relative to that root with a leading /](/2_Syntax/4_External_Macros.md#project-relative-paths).

(Context functions):
```python
def __init__(self, project_root):
    self.project_root = project_root.absolute()
    self.files = {}
    self.add_directory(self.project_root)
```

As part of the normalization process, all paths stored on this object will be absolute. This simplifies assumptions code interacting with this class makes.

Adding a directory is surprisingly easy to accomplish, as `pathlib` provides a `glob` function that simplifies the traversal process.

(Context functions):
```python
def add_directory(self, path):
    for file in path.glob("**/*.md"):
        self.add_file(file)
```

A path in the local operating system is provided when files are added, but absolute paths within the markdown files will be in relation to the project root. A key responsibility of this class is to provide a translation layer between project paths and operating system paths.

(Context functions):
```python
def add_file(self, file):
    self.files["/" + file.absolute().relative_to(self.project_root).to_posix()] = file.absolute()
```

## Identifying the Root Directory

As mentioned above, identifying the project root is almost always how this class will be used. Although the general constructor should remain generic, a factory method that normalizes that particular use case is convenient.

(Context functions):
```python
def from_project_root():
    <#Search up from current directory for .tome>
    return Context(path)
```

Until now, `pathlib` would have been imported by the code calling `Context`. With a factory method, though, that dependency has to be made explicit.

(Dependencies):
```python
from pathlib import Path
```

As outlandish as this is, the root directory could feasibly be a Tome project. Not sure what that would look like, but to leave that open as possibility the condition has to come at the end of the loop.

[Search up from current directory for .tome]:
```python
path = Path.cwd()
while True:
    break if (path / ".tome").exists()
    raise Exception("Cannot locate the project root") if path.parent == path
    path = path.parent
```

Other options were considered for identifying the project root, such as presence of a README or version control. While these are possible, it also opens the possibility of acting on a really large set of files, which could be dangerous.

