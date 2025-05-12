This is the whole source of my Bachelor's thesis at Technical University Vienna.

It includes:
- every latex file used to compile main.pdf (compilation using [tectonic](https://tectonic-typesetting.github.io/en-US/))
- every non self created file is located in input folder.
- every self created figure is either compiled directly in latex (thus located in **src**) or present as a .pdf file which can be opened using [ipe](https://ipe.otfried.org/)
- a **nix flake** which can be used to recreate the development environment (for compiling latex and running code) using the [nix package manager](https://nixos.org/) (works on any modern Linux/macOS)
- **calc** folder will also include every program (python, SMath, ... ) written in the course of writing this thesis. (but not at this moment!)

To-Do:

- Go over everything and make important thing's italic.
- Typst calculator and table at the end.
  - Table at the end of the main results and for specific gases.
- Paragraph about time constant and product to the mass spec.
