# Preamble

`{#system}: s`
```python
system = """
<#preamble>

<#commands>
"""
```

Since ChatGPT most likely will be unaware of Tome, a brief description is necessary to give it the necessary context.

`{#preamble}: s`
```
You are a programmer tasked with revising a project created using a tool called Tome. Tome is a literate programming tool which is based on all of the markdown files below a given directory.
```

Rather than provide a full primer, the prompt will provide a series of commands the LLM can respond with, one of which is the final output. To keep from putting together too much ahead of time, a `HELP` command will allow the LLM to express what functionality to focus on next.

`{#commands}: s`
```
Throughout this conversation, you will occasionally be asked to provide a command. In those cases, only respond with one of the following words:

* TREE - You need the directory tree of the project
* HELP - You need more information and the other commands are insufficient
* PATCH - You have enough information to make the requested revision
```

When a command must be requested, the following sentence should be used:

`{#request command}: s`
```
Please respond with one word, a valid command, and nothing else.
```

This was a prompt that didn't work:

```
Your response should be in the following format:

~~~
COMMAND
Parameters for the command
~~~

Here are the following commands, along with the form the parameters should take:

* TREE - Provides the file tree of the project, no parameters are necessary
* HELP - Description of additional information that is needed in order to complete the request
* PATCH - Text appropriate to pass to the `patch` command to revise the project

For example, if you want to know about the syntax Tome uses, you would use the following response:

~~~
HELP
I need more information about the syntax, what format are the files in?
~~~
```
