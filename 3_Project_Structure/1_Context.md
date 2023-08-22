# Context

A context is a set of files that need to be operated on together. Initially this will be all of the Markdown files below the directory provided to the constructor, but the library leaves the possibility of additional files being added.

The library can be imported like this:

`{#Import}: s`
```python
from context import Context
```

Establishing the context from the project root is fairly common, which can be done like this:

`{#Establish project context}: s`
```python
<#Import>
context = Context.from_project_root()
```

## Project Context

The library primarily provides a class called `Context`.

`{#/build/context.py}: f`
```python
<#Dependencies>

class Context():
    <#Context functions>
```

A context will start with all of the files beneath a particular directory. In addition to seeding the directory, the provided root enables referencing paths relative to that root with a leading /.

`{#Context functions}: m`
```python
def __init__(self, project_root):
    self.project_root = project_root.absolute()
    <#Initialize class>
    self.add_directory(self.project_root)
```

As part of the normalization process, all paths stored on this object will be absolute. This simplifies assumptions code interacting with this class makes.

Adding a directory is surprisingly easy to accomplish, as `pathlib` provides a `glob` function that simplifies the traversal process.

`{#Context functions}: m`
```python
def add_directory(self, path):
    for file in path.glob("**/*.md"):
        self.add_file(file)
```

A path in the local operating system is provided when files are added, but absolute paths within the markdown files will be in relation to the project root.

`{#Convert system path to project path}: s`
```python
f"/{file.absolute().relative_to(self.project_root)}"
```

A key responsibility of this class is to provide a translation layer between project paths and operating system paths.

`{#Initialize class}: m`
```python
self.files = {}
```

`{#Context functions}: m`
```python
def add_file(self, file):
    self.files[<#Convert system path to project path>] = file.absolute()
```

## Identifying the Root Directory

As mentioned above, identifying the project root is almost always how this class will be used. Although the general constructor should remain generic, a factory method that normalizes that particular use case is convenient.

`{#Context functions}: m`
```python
def from_project_root():
    <#Search up from current directory for .tome>
    return Context(path)
```

Until now, `pathlib` would have been imported by the code calling `Context`. With a factory method, though, that dependency has to be made explicit.

`{#Dependencies}: m`
```python
from pathlib import Path
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

## Associating Macros

To avoid reparsing files when external links are involved, it's helpful to associate the project relative path with the macros identified.

`{#Initialize class}: m`
```python
self.macros = {}
```

`{#Context functions}: m`
```python
def associate_macro(self, path, macros):
    self.macros[path] = macros
```

## Project Path Resolution

As project paths are relative to the root of the `Context`, it must be responsible for for resolving those into full paths. In addition, sometimes files need to be staged elsewhere until later in the process, such as when [replacing the build directory](/1_CLI/2_Build.md#replacing-build-directory).

When files need to be staged elsewhere, the requesting code needs to communicate that fact. It does so by calling `stage` with a regular expression that is applied to the project relative path using `re.search`.

`{#Context functions}: m`
```python
def stage(self, regexp):
    self.staged.append(regexp)
```

Along with the data structure to hold staged paths, the context will need a place to resolve them to temporarily until it's unstaged.

`{#Dependencies}: m`
```python
import tempfile
```

`{#Initialize class}: m`
```python
self.staged = []
self.staged_tempdir = tempfile.TemporaryDirectory()
self.staged_root = Path(self.staged_tempdir.name)
```

Once the code using this context is done, it needs a way to return the files to their rightful home. This is a naturally recursive process, but the entry needs to set up some information from the project class.

`{#Context functions}: m`
```python
def unstage(self, source = None, target = None):
    if not source or not target:
        return self.unstage(source or self.staged_root, target or self.project_root)
    for child in source.iterdir():
        <#Unstage child>
```

Unstaging the child looks significantly different if it's a file or directory.

`{#Unstage child}: s`
```python
if child.is_dir():
    <#Unstage directory>
else:
    <#Unstage file>
```

If the file exists in the target, it will be replaced. If it's a directory, though, something is probably wrong so an exception is raised.

`{#Unstage file}: s`
```python
target_file = target / child.name
if target_file.is_dir():
    raise Exception(f"Trying to replace {target_file}, but it's currently a directory")
child.replace(target_file)
```

Similarly, it's fine for the contents to be merged with directories already in the project root, but directories will raise an exception if they are replacing a file.

`{#Unstage directory}: s`
```python
target_dir = target / child.name
if not target_dir.exists() and not target_dir.is_dir():
    raise Exception(f"Trying to replace {target_dir}, but it's currently a file")
target_dir.mkdir(exist_ok = True)
self.unstage(child, target_dir)
child.rmdir()
```

Because the staged values are regular expressions, it's fairly straightforward to determine if a particular file should be staged. This takes advantage of the fact that an empty list evaluates to false.

`{#Dependencies}: m`
```python
import re
```

`{#Context functions}: m`
```python
def is_staged(project_path):
    return [regexp for regexp in self.staged if re.search(regexp, project_path)]
```

When other parts of the codebase need to interact with a file, they need to be aware of the absolute path to use. This of course will be different depending on if the file is staged.

`{#Context functions}: m`
```python
def absolute_path(self, project_path):
    base_path = self.staged_root if self.is_staged(project_path) else self.project_path
    return base_path / re.sub(r"^/", "", project_path)
```
