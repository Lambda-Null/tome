# Build

Build the program documented in the project tree. If a root of the project cannot be identified, as identified by the `.tome` directory, an error is thrown.

{#/build/bin/commands/build}: f+x
```python
#!/usr/bin/env python
```

The [project context](/3_Project_Structure/1_Context.md) builds up a collection of files in a project, which is needed to build the project.

{#/build/bin/commands/build}: f+x
```python
</3_Project_Structure/1_Context.md#Establish project context>
```

## Preparations

Before Tome can run, it needs to install some dependencies. The bootstrapping command should take care of this, but it also has a project command that can be used called `dependencies`.

{#/.tome/commands/dependencies}: f+x
```shell
#!/bin/sh
pip install -r ../requirements.txt
```

The only dependency right now is [Marko](https://marko-py.readthedocs.io/en/latest/):

{#/.tome/requirements.txt}: f
```
marko==2.0.0
```

## Build Directory

Large projects typically rename and move around files as needs evolve and the design is refined. When this occurs, the old file can linger causing issues. To combat this, the `build` directory will be deleted before generating new files.

{#/build/bin/commands/build}: f+x
```python
(context.project_root / "build").rmdir()
```

It's perfectly valid to define files outside of the `build` directory, just keep in mind that if they are renamed or removed it will have to be addressed manually.

## Building Root Directory

Each of the files in the context needs to be [parsed](/2_Syntax). That process will identify files that should be generated, those need to be written. It's also helpful for the user to get feedback on what occurred during this process.

{#/build/bin/commands/build}: f+x
```python
</2_Syntax/1_General_Concepts.md#Import>
parser = parser.Parser(context)
parser.parse()
for file in parser.output_files():
    print(f"Writing {file.name}")
    file.write()
print("Build Finished")
```
