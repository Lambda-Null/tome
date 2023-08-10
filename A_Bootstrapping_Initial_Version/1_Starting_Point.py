# This script should be the only code directly checked in to the
# codebase. It was generated from 1_Starting_Point.md, see read that
# page to better understand this script.
import sys
doc_file = sys.argv[1]
import re
code_file = re.sub(r"[.]md$", ".py", doc_file)
with open(code_file, "w") as f:
    writing = False
    for line in open(doc_file, "r").readlines():
        if re.match(r"^```", line):
            writing = not writing
        elif writing:
            f.write(line)
