# Conventions

Here are some conventions that will need to be followed to satisfy technical requirements in Tome:

* The tangled program is placed in a directory called `build` at the root level
  + Other files within the project will also be generated, but will not be automatically removed if the name is changed or removed
* All Markdown files must end in `.md`
* There is a single line of whitespace prior to the descriptor of a code block
  + Lack of separation will cause the descriptor to get mixed up in the preceding paragraph

In addition, the following conventions are recommended to make the navigation of Tome projects easier:

* Each directory containing documentation also contains a `README.md`
  + This is rendered automatically when a directory is visited in most sites hosting source code
* If there is a natural order to how documentation should be read, include a prefix in the filename with a number
  + Example: `1_Name_for_Chapter_1.md`
  + Most sites hosting source code sort files, this allows you to control the order of directory contents
* Words indicating ownership such as "I" and "my" should be avoided
  + Larger scale projects depend on contributions by many people, who may feel discouraged from doing so if an individual is claiming ownership
* First word of macro name is capitalized and the rest of the words are lowercased
  + Macro names are case sensitive, and without some consistency this is an easy mistake to make
