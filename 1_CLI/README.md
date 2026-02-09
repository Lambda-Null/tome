# The Core Program

To interact with Tome, there is a CLI available called `tome` tome which takes various commands as its first argument. Here is a summary of those commands:

* [help](#Help): How to use this command.
* [init](1_Init.md): Initialize the current directory as a Tome project.
* [build](2_Build.md): Build the program documented in the project tree.

## Help

The help script, with no arguments, will print something very similar to the top level section of this page. There's some [future work](/B_Loose_Ends/Future_Work.md) around removing this duplication, but just copy/pasting for now.

`{#/build/bin/commands/help}: f+x`
```python
#!/usr/bin/env python

print("""
Usage: tome [command]

CLI for interacting with Tome projects, a directory based literate programming tool.
See https://github.com/Lambda-Null/tome/tree/main for more information.

Available Commands:
* help: Print this message.
* init: Initialize the current directory as a Tome project.
* build: Build the program documented in the project tree.
""")
```

Since project specific commands can also be defined, those should be listed here as well.

`{#/build/bin/commands/help}: f+x`
```python
</3_Project_Structure/Building_Tome_Context.md#Within project context>
    import pathlib
    commands = context.absolute_path(pathlib.Path(".tome") / "commands")

    if commands.is_dir():
        <#Print project specific help>
```

The issue with using `pathlib` is it's difficult to tell if the directory is empty from the API. So the prefix message will instead be on the first iteration through the loop.

`{#Print project specific help}: s`
```python
message_printed = False
for command in commands.iterdir():
    if not message_printed:
        print("In addition to commands defined by Tome, this project has the following commands available:")
        message_printed = True
    print(f"* {command.name}")
```

## The Executable

Right now, this executable has only been tested in Unix environments, specifically Ubuntu 23.04 and higher. It's built with [PyInstaller](https://pyinstaller.org/en/stable/), which allows portability, but not across operating systems.

`{#/.tome/requirements.txt}: f`
```
pyinstaller==6.10.0
```

The easiest way of using it currently is to add `/path/to/this/project/build/bin` to your `PATH`.

`{#/build/bin/tome}: f+x`
```python
#!/usr/bin/env python
```

The individual commands are independent scripts which can be run. To communicate Tome's python libraries to them, `PYTHONPATH` is added to.

`{#/build/bin/tome}: f+x`
```python
import os
import sys
import pathlib
executable = pathlib.Path(sys.argv[0])
if "PYTHONPATH" in os.environ:
    os.environ["PYTHONPATH"] += ":"
else:
    os.environ["PYTHONPATH"] = ""
os.environ["PYTHONPATH"] += str(executable.parent.parent)
sys.path.append(str(executable.parent.parent))
```

## Prebuilt Commands

Within all commands, knowing the project root is extremely helpful in operating on various generated files, so the environment variable `PROJECT_ROOT` is provided.

`{#/build/bin/tome}: f+x`
```python
command = sys.argv[1] if len(sys.argv) > 1 else "help"
context = None
if command not in {"init", "help"}:
    </3_Project_Structure/Building_Tome_Context.md#Within project context>
        os.environ["PROJECT_ROOT"] = str(context.absolute_path("/"))
        <#Context aware logic>
```

The `init` and `help` commands are resolved without using project context and only check the core command scripts.

The files in `/build/bin/commands/` are scripts which share the command name provided. If a command isn't found there, commands defined for the particular project will be executed.

`{#Context aware logic}: m`
```python
command_path = executable.parent / "commands" / command
if not command_path.exists():
    <#Locate script within project context>
```

## Project Commands {#project-commands}

The motivation for using scripts instead of libraries is to allow commands to be implemented in any language. Tome itself will define all of these in Python, but any scripts in `/.tome/commands/` of the project will be invoked if a core command doesn't exist.

`{#Locate script within project context}: s`
```python
if context:
    command_path = context.absolute_path(pathlib.Path(".tome") / "commands" / command)
```

## Missing Commands

If the command isn't defined anywhere, the help command is used.

`{#Context aware logic}: m`
```python
if not command_path.exists():
    command = "help"
    command_path = executable.parent / "commands" / command
```

## Executing Command

Since there's nothing left to do except execute the command, the `exec*` class of functions can be used. This is most likely a micro-optimization, but it makes the process of conveying the exit code to the caller easier.

`{#Context aware logic}: m`
```python
os.execvp(command_path, [command_path] + sys.argv[2:])
```
