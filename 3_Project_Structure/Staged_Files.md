# Staged Files

When files need to be staged elsewhere, different paths must be used. Coupling the staging logic to `FileContext` makes that class difficult to work with in varying circumstances, so staging will be a class that can be layered on top of anything confirming to the `Context` base class.

`{#/build/context/staged.py}: f`
```
import re
from context.base import Context
from context.file import FileContext

class StagedContext(Context):
    def __init__(self, context, staged_root, staged_patterns):
        self.context = context
        self.staged_context = FileContext(staged_root)
        self.staged_patterns = staged_patterns
    <#functions>
```

The output of `relative_path` expected by the rest of the system is a bit surprising, it's absolute with respect to the project root. This probably needs to be cleaned up at some point, but trying to limit the scope of the current changes.

`{#functions}: m`
```python
def relative_path(self, reference, project_path):
    return self.context.relative_path(reference, project_path)
```

To determine if the path is staged, each pattern needs to be considered in turn.

`{#functions}: m`
```python
def is_staged(self, project_path):
    return [regexp for regexp in self.staged_patterns if re.search(regexp, str(project_path))]
```

Deciding between the staged context and base context is dictated entirely on if the provided path is staged.

`{#functions}: m`
```python
def absolute_path(self, project_path):
    if self.is_staged(project_path):
        return self.staged_context.absolute_path(project_path)
    else:
        return self.context.absolute_path(project_path)
```

This should probably be shifted so the absolute path is that in the staged context when relevant, but for now this doesn't matter for the system.

`{#functions}: m`
```python
def __iter__(self):
    return iter(self.context)
```

## Unstaging

Once the code using this context is done, it needs a way to return the files to their rightful home. This is a naturally recursive process, but the entry needs to set up some information from the project class.

`{#functions}: m`
```python
def unstage(self, source = None, target = None):
    if not source or not target:
        return self.unstage(source or self.staged_context.absolute_path("/"), target or self.context.absolute_path("/"))
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
if target_dir.exists() and not target_dir.is_dir():
    raise Exception(f"Trying to replace {target_dir}, but it's currently a file")
target_dir.mkdir(exist_ok = True)
self.unstage(child, target_dir)
child.rmdir()
```
