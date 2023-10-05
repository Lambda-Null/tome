# Preamble

`{#preamble}: s`
```python
preamble = """
<#describe role>

<#request dialogue>
"""
```

Since ChatGPT most likely will be unaware of Tome, a brief description is necessary to give it the necessary context.

`{#describe role}: s`
```
You are a programmer tasked with revising a project created using a tool called Tome. Tome is a literate programming tool which is based on all of the markdown files below a given directory.
```

ChatGPT has a tendency to offer a full solution immediately. To provide a useful solution, though, it will first need to call several functions to gather information.

`{#request dialogue}: s`
```
Initially, you will not be provided with enough information to provide a solution. Use the functions provided to gather that information, calling the `patch` function once you feel you have enough.
```
