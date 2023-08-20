# Bootstrapping Initial Version

Obviously Tome wasn't written in Tome originally, it started as an extremely simplistic program that grew into the full project. This directory provides intermediate forms which allow a path from something extremely simple that is easily assembled by hand all the way to the full program. The sections of this appendix are divided into stages:

* [Stage 1: Starting Point](1_Starting_Point.md)
* [Stage 2: Named Macros](2_Named_Macros.md)
* [Stage 3: External Links](3_External_Links.md)
* [Stage 4: Final Bootstrapping Version](4_Final_Bootstrapping_Version.md)

In general, each stage produces a Python script bearing the same name which can be used on the subsequent stages documentation. Stage 1 is also self-referential, running it on its own documentation will produce itself. The only exception is that stage 4 does not take an argument, running a stripped down version of the [build command](/1_CLI/2_Build.md) to produce the full program.

## Installing

Once the bootstrap process is complete, you will have an executable at `/path/to/tome/build/bin/tome`. Adding the `bin` directory to your `PATH` is the most straightforward way to start using it in other projects.
