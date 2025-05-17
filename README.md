This is the whole source of my Bachelor's thesis at Technical University Vienna.

It includes:
- every latex file used to compile main.pdf (compilation using [tectonic](https://tectonic-typesetting.github.io/en-US/))
- every self created figure is either compiled directly in latex (thus located in **src**) or present as a .pdf file which can be opened using [ipe](https://ipe.otfried.org/)
- a **nix flake** which can be used to recreate the development environment (for compiling latex and running python code) using the [nix package manager](https://nixos.org/) (works on any modern Linux/macOS)
- **calc** folder will also include every program (python, SMath) written and used in the course of writing this thesis.
