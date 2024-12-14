{
  description = "Environment with named dev environments and inherited shell specs.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in
  {
    devShells = {
      ${system} = {
        default = pkgs.mkShell {
          buildInputs = [
            (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
              python-lsp-server
              tabulate
            ]))
            pkgs.tectonic
            pkgs.imagemagick
            pkgs.inkscape
            pkgs.nushell
          ];
          shellHook = ''
            zathura ./build/main.pdf &
            hx README.md
          '';
        };
      };
    };
  };
}
