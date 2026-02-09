# Testing

Any project of substantial size will have code associated with it intended for testing. For the most part, launching these will entail a single command, so it's tempting to leave it to the individual project to create a `test` command. Nevertheless, there are a few factors pushing in the other direction:

1. It's easy to run a command without rebuilding the project, leading to the erroneous assumption that the recent changes are passing.
2. Leaving the command to the authors causes inconsistency across projects.
3. Sometimes it's a bit tough to figure out what to do to get tests running.

Tome guarantees that the command `tome test` will always run tests on the most up to date version of the system. This, of course, starts in a command:

`{#/build/bin/commands/test}: f+x`
```
#!/bin/sh

tome build
<#launch tests>
```

## Suites

If one command launched all tests, it might feel a bit like reinventing the wheel to just define the test command in a different place. In larger projects, though, there are typically many suites of tests which are used in different circumstances. These will, of course, be described in individual files:

`{#launch tests}: s`
```
suite_path=<#determine suite path>
$suite_path
```

Suite scripts are defined in `/.tome/test/suite`, with `default` used if none is specified.

`{#determine suite path}: s`
```
$PROJECT_ROOT/.tome/test/${1:-default}
```

## Tome Suite

To see how to use this, here is how Tome sets up its default suite:

`{#/.tome/test/default}: f+x`
```
#!/bin/sh

python -m unittest discover -s $PROJECT_ROOT/test -t $PROJECT_ROOT
```

Additionally, this will expect the test directory to be importable. So even though it doesn't need to contain anything, the `__init__.py` file must exist.

`{#/test/__init__.py}: f`
```
```

To make sure it's picking things up properly, there should be a few tests that test basic plumbing.

`{#/test/test_suite_detects_files.py}: f`
```
from unittest import TestCase
<#plumbing imports>

class PlumbingTest(TestCase):
    <#plumbing tests>
```

First, it should include a test that should pass as long as it's picked up.

`{#plumbing tests}: m`
```
def test_detected(self):
    self.assertEqual(4, 2 + 2)
```

It's also important to verify build code can be imported.

`{#plumbing imports}: m`
```
from context.file import FileContext
import os
from pathlib import Path
```

`{#plumbing tests}: m`
```
def test_import_build(self):
    project_root = Path(os.environ["PROJECT_ROOT"])
    c = FileContext(project_root)
    self.assertEqual(
        project_root / "file",
        c.absolute_path("/file"),
    )
```

Other tests will be distributed 
