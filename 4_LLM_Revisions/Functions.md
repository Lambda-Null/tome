# Functions

ChatGPT provides a notion of functions, which nudge the LLM into being more likely to respond with structured data. Rather than generate a full response in one prompt, each one will give ChatGPT a little bit more information to build up a solution.

The return values of these functions will be a dictionariy describing what needs to be done next. If the conversation needs to be ended, it will look like this:

`{#end the conversation}: s`
```python
{ "stop": True }
```

The functions themselves will need to be collected in a variable, so the information can be passed easily to ChatGPT.

`{#functions}: m`
```python
functions = []
```

## Help

As a backstop to all of the other functions, a help function is provided that will allow ChatGPT to declare that none of the available functions provides the information it needs to complete the request.

`{#functions}: m`
```python
functions.append({
    "name": "help",
    "description": "Describe information you are unable to obtain from one of the other functions",
    "parameters": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "an explanation of the information that is needed and why it is not covered by one of the other functions",
            },
        },
    },
})
```

Since the conversation is already being printed, it doesn't have to do anything else.

`{#functions}: m`
```python
def help(description):
    return <#end the conversation>
```

## File Tree

A basic piece of information it will need in order to request information about specific files is the file tree of the project.

`{#functions}: m`
```python
functions.append({
    "name": "file_tree",
    "description": "Returns a description of the file tree for the project",
    "parameters": { "type": "object", "properties": {} },
})
```

This function has to both convey that the conversation should continue and the information about the file tree.

`{#functions}: m`
```python
</3_Project_Structure/1_Context.md#Establish project context>
def file_tree():
    return {
        "stop": False,
        "response": "\n".join([str(p) for p in context.project_root.glob("**/*.md")]),
    }
```

## Patch

Once ChatGPT is prepared to suggest a revision, it should be done in a form appropriate for the `patch` command.

`{#functions}: m`
```python
functions.append({
    "name": "patch",
    "description": "Make a revision to the codebase by describing a diff file that should be applied to the codebase using the `patch` command",
    "parameters": {
        "type": "object",
        "properties": {
            "diff": {
                "type": "string",
                "description": "The contents of a diff file describing revisions to a codebase",
            },
        },
    },
})
```

Eventually this patch will be applied to the codebase at this point, but for now we just want to see what the LLM comes up with:

`{#functions}: m`
```python
def patch(diff):
    return <#end the conversation>
```
