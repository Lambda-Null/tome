# Revision

The user can make a request either in the form of a series of files or STDIN. The `fileinput` module does the heavy lifting here:

`{#prompt}: m`
```python
import fileinput
import sys
revision = "\n".join([l for l in fileinput.input(encoding="utf-8")])
```

In addition, the initial response to this prompt should be a command.

`{#prompt}: m`
```python
prompt = f"""
{revision}

<Preamble.md#request command>
"""
```
