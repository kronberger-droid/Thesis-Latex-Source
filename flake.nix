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
            pkgs.tectonic
            pkgs.zathura
            (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
              python-lsp-server
              numpy
              matplotlib
              scipy
              scikit-learn
              pandas
            ]))
          ];
          shellHook = ''
            zathura main.pdf > zathura.log 2>&1 &
            ZATHURA_PID=$!
            trap "kill $ZATHURA_PID" EXIT
            hx README.md
          '';
        };
      };
    };
  };
}
