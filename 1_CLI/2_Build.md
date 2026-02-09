# Build

Build the program documented in the project tree. If a root of the project cannot be identified, as identified by the `.tome` directory, an error is thrown.

`{#/build/bin/commands/build}: f+x`
```python
#!/usr/bin/env python
```

The [project context](/3_Project_Structure/1_Context.md) builds up a collection of files in a project, which is needed to build the project.

`{#/build/bin/commands/build}: f+x`
```python
</3_Project_Structure/Building_Tome_Context.md#Within project context>
    <#Context aware logic>
```

## Preparations

Before Tome can run, it needs to install some dependencies. The bootstrapping command should take care of this, but it also has a project command that can be used called `dependencies`.

`{#/.tome/commands/dependencies}: f+x`
```shell
#!/bin/sh
pip install -r $PROJECT_ROOT/.tome/requirements.txt
```

TODO: Perhaps I should build support for cross-file file macros


[Marko](https://marko-py.readthedocs.io/en/latest/) helps parsing of Markdown.

`{#/.tome/requirements.txt}: f`
```
marko==2.0.0
```

## Replacing Build Directory {#replacing-build-directory}

Large projects typically rename and move around files as needs evolve and the design is refined. When this occurs, the old file can linger causing issues. To combat this, the `build` directory will be deleted as part of the process.

If there's an error in the process, either in Tome or the project being built, it's better to leave the old directory in place. So the context will be told to stage that directory in another location.

Once everything has been built, the `build` directory can be safely deleted and the new one moved into its place.

`{#Replace build directory with new version}: s`
```python
import shutil
print(f"replacing {context.absolute_path('build')} with {context.staged_context.absolute_path('build')}")

build_folder = (context.absolute_path("build"))
if build_folder.exists():
    shutil.rmtree(build_folder)

test_folder = (context.absolute_path("test"))
if test_folder.exists():
    shutil.rmtree(test_folder)

context.unstage()
```

It's perfectly valid to define files outside of the `build` directory, just keep in mind that if they are renamed or removed it will have to be addressed manually.

## Building Root Directory

Each of the files in the context needs to be [parsed](/2_Syntax). That process will identify files that should be generated, those need to be written. It's also helpful for the user to get feedback on what occurred during this process.

`{#Context aware logic}: m`
```python
</2_Syntax/README.md#Import>
parser = Parser(context)
for file in parser.output_files():
    print(f"Writing {file.path}")
    file.write()

<#Replace build directory with new version>

print("Build Finished")
```
