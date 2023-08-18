# Conventions

Tome makes assumes that particular conventions are followed:

* The tangled program is placed in a directory called `build` at the root level
* All Markdown files end in `.md`
* Each directory containing documentation also contains a `README.md`, which includes a table of contents for the contents of that directory
* There is a single line of whitespace prior to the descriptor of a code block and immediately following the codeblock
* Additional work that is needed is flagged with the word `TODO`
* Possessive words like "I"
* First word of macro name is capitalized and the rest of the words are lowercased
* If a file creates a file meant to imported, the import statement is provided in a macro called `Import`

There are some decent reasons to break these, Tome certainly needs to in some cases. Just be aware that things might get a bit wonky if this is done.
