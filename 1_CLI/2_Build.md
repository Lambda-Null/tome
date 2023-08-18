# Build

Build the program documented in the project tree. If a root of the project cannot be identified, as identified by the `.tome` directory, an error is thrown.

## Building Root Directory

[/build/bin/commands/build]: f+x
```python
#!/usr/bin/env python
```

The [project context](/3_Project_Structure/1_Context.md) builds up a collection of files in a project, which is needed to build the project.

[/build/bin/commands/build]: f+x
```python
</3_Project_Structure/1_Context.md#Establish project context>
```

Each of the files in the context needs to be [parsed](/2_Syntax). That process will identify files that should be generated, those need to be written. It's also helpful for the user to get feedback on what occurred during this process.

[/build/bin/commands/build]: f+x
```python
</2_Syntax/1_General_Concepts.md#Import>
parser = parser.Parser(context)
parser.parse()
for file in parser.output_files:
    print(f"Writing {file.name}")
    file.write()
print("Build Finished")
```
