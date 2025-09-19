{
  description = "A Nix flake for the Senate Insight Lab project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {self, nixpkgs, flake-utils, uv2nix, ...}:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python313
          uv
          # System
          git
          firefox
          playwright-driver
          # Python
          virtualenv
        ] ++ pkgs.lib.optionals pkgs.stdenv.isLinux [
          chromium
        ];

        env = {
          # Don't create venv using uv
          UV_NO_SYNC = "1";
          # Force uv to use Python interpreter from venv
          UV_PYTHON = "${pkgs.virtualenv}/bin/python";
          # Prevent uv from downloading managed Python's
          UV_PYTHON_DOWNLOADS = "never";
        };

        shellHook = ''
            echo "Python $(python --version)"
            echo "UV $(uv --version)"
            echo "Run 'uv init .' to start your project"
        '';
      };
    }
  );
}
