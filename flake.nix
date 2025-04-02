{
  description = "Development environment for a Computer Graphics course";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};

      # Define a custom Python environment with the required packages
      pythonWithPackages = pkgs.python3.withPackages (ps:
        with ps; [
          glfw
          jupyter
          numpy
          pyglm
          python-lsp-server
          pyopengl
        ]);
    in {
      # Define the development shell
      devShells.default = with pkgs;
        mkShell {
          buildInputs = [
            pythonWithPackages
            # Add any additional tools or dependencies here
            pyright
            mesa # For OpenGL support
            libGL # OpenGL libraries
            libGLU # OpenGL utility library
            xorg.libX11 # X11 libraries (needed for GLFW)
            xorg.libXrandr # Xrandr (needed for GLFW)
            xorg.libXi # Xi (needed for GLFW)
          ];

          shellHook = ''
            echo "Welcome to the Computer Graphics development environment!"
            echo "Jupyter is available. Run 'jupyter notebook' to start."
          '';
        };
    });
}
