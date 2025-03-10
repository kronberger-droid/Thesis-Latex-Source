This is the whole source of my bachelors thesis at TU Wien.

It includes:
- every latex file used to compile main.pdf (compilation using [tectonic](https://tectonic-typesetting.github.io/en-US/))
- every non self created file is located in input folder.
- every self created figure is either compiled directly in latex (thus located in **src**) or present as a .pdf file which can be opened using [ipe](https://ipe.otfried.org/)
- a **nix flake** which can be used to recreate the development environment (for compiling latex and running code) using the [nix package manager](https://nixos.org/) (works on any modern linux/macos)
- **calc** folder will also include every program (python, matlab, smath, ... ) written in the course of writing this thesis. (but not at this moment!)

Do-To's:
- Scope and objectives
  - still some mistakes
  - make a good introduction
- Analytical Work
  - Good introduction
  - Expected flow regimes
    - continuum flow needs some work
  - finish dimension of the flow
  - one-dim insentropic
    - add interpretation
  - flow behaviours in micro-channels
    - finish the last paragraphs
    - make connection to formulation of the leak due to unknown factors inside the reactor
  - under-expanded nozzle plume
    - finish the last paragraphs
- Discusion
  - create red line through the thesis
  - make reference to what was done
  - mention things not done too.
- Conclusion
  - create it! (doesn't have to be long!)
- Formularium
  - add all the formulars used at the end and provide references.
