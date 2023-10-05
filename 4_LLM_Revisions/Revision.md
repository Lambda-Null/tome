# Revision

The user can make a request either in the form of a series of files or STDIN. The `fileinput` module does the heavy lifting here:

`{#prompt}: m`
```python
import fileinput
import sys
prompt = "\n".join([l for l in fileinput.input(encoding="utf-8")])
```
