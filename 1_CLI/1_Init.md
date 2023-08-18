# Init

Initialize the current directory as a Tome project. This creates a few files and directories Tome depends on to function correctly.

[/build/bin/commands/init]: f+x
```python
#!/usr/bin/env python
from pathlib import Path

<#Create files and directories>

print("Tome Initialized")
```

# Meta Information

Any meta information needed to operate is stored in a directory at the project root called `.tome`.

[Create files and directories]: m
```python
print("Creating .tome")
dot_tome = context.root / ".tome"
dot_tome.mkdir(exists_ok = True)
```

## Git Accomodations

Since it might be initialized as a Tome project before it's initialized as a Git repository, it's helpful to assume it will eventually become that. There are a few things that need to be prepared for them to play nicely together.

Git doesn't track folders with no files, but Tome relies on the presence of the `.tome` folder to identify the project root. The convention is to place a file called `.gitkeep` in the folder.

[Create files and directories]: m
```python
(dot_tome / ".gitkeep").write_text("")
```

By convention, the `build` directory is where all generated files go. Typically those files aren't checked in, so ignoring those.


[Create files and directories]: m
```python
print("Creating .gitignore")
(context.root / ".gitignore").write_text("build")
```
