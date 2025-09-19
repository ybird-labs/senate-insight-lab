{
  description = "A Nix flake for the Senate Insight Lab project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {self, nixpkgs, flake-utils}:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python314
          uv
          # System
          chromium
          firefox
          playwright-driver
        ];

        shellHook = ''
            echo "Python $(python --version)"
            echo "UV $(uv --version)"
            echo "Run 'uv init .' to start your project"
        '';
      };
    }
  );
}
