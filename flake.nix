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

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {self, nixpkgs, flake-utils, uv2nix, pyproject-build-systems, pyproject-nix,...}:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python313;
      workspace = uv2nix.lib.workspace.loadWorkspace {
        workspaceRoot = ./.;
      };


      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";
      };

      # pythonSet = pythonBase.overrideScope (
      #   flake-utils.lib.composeManyExtensions [
      #     pyproject-build-systems.overlays.wheel
      #     overlay
      #   ]
      # );
      # 3. Create Python package set with build systems
      pythonSet = (pkgs.callPackage pyproject-nix.build.packages {
        inherit python;
      }).overrideScope (
        pkgs.lib.composeManyExtensions [
          pyproject-build-systems.overlays.default
          overlay
        ]
      );

      virtualEnv = pythonSet.mkVirtualEnv  "senate-insight-env" workspace.deps.default;



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
          virtualEnv
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
