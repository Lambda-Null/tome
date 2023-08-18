# Tome: Large Scale Literate Programming

Tome is a literate programming tool aimed at working effectively in large scale projects. Documentation is written is Markdown, stitching together fenced code blocks to produce the actual code.

## Table of Contents

* [Chapter 1 - CLI](/1_CLI/README.md)
* [Chapter 2 - Syntax](/2_Syntax/README.md)
* [Chapter 3 - Project Structure](/3_Project_Structure/README.md)
* [Appendix A - Bootstrapping Initial Version](A_Bootstrapping_Initial_Version/README.md)
* [Appendix B - Loose Ends](/B_Loose_Ends/README.md)

## Getting Started

Right now, installing Tome is a manual process. There's some [future work](/B_Loose_Ends/Future_Work.md) to package executables for various operating systems, but for now you will have to [bootstrap the program yourself](A_Bootstrapping_Initial_Version/README.md). Also be aware that this has only been tested on Ubuntu 23.04, if you run into issues using it in other contexts feel free to submit a Pull Request.

TODO: Narrate the basic usage
* Init
* Write a file
* Write/use a macro
* Write a second file
* Use the second file in the first
* Provide pointers to various parts of the documentation

## What is Literate Programming

[Literate Programming](https://en.wikipedia.org/wiki/Literate_programming) is a concept [introduced by Donald Knuth](http://literateprogramming.com/) in which the code for a program is embedded in its documentation. In its original form, the source file could either be "tangled" to produce an executable or "woven" to produce documentation.

GitHub, along with many other popular sites for hosting source code, automatically render markdown files, eliminating the need to weave the source into documentation. Tome, along with a few other Literate Programming tools, take advantage of this to focus on tangling its code blocks.

For the most part, Literate Programming has lived in the realm of the hobbyist, and the tooling generally reflects that. There are a few large programs written using it, most notably [TeX](https://en.wikipedia.org/wiki/TeX), but many of the tools really begin to feel cumbersome as a project grows. Tome strives to grow more naturally as projects become larger.
