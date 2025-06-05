{
  description = "Computer Graphics Development Environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    # Custom Python environment with dependencies
    pythonEnv = pkgs.python3.withPackages (ps:
      with ps; [
        glfw
        jupyter
        numpy
        mypy
        pyglm
        pyopengl
        tabulate
        toml
        pyyaml
      ]);

    # Native dependencies (OpenGL, GLFW requirements)
    nativeDeps = with pkgs; [
      mesa
      libGL
      libGLU
      xorg.libX11
      xorg.libXrandr
      xorg.libXi
    ];

    # Combine Python + native dependencies
    allDeps = nativeDeps ++ [pythonEnv];

    # Derivable app (for `nix run`)
    app = pkgs.writeShellApplication {
      name = "project_2";
      runtimeInputs = allDeps;
      text = ''
        python ${self}/src/main.py
      '';
    };
  in {
    # For `nix develop`
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = allDeps;
      shellHook = ''
        echo "🚀 Welcome to the Computer Graphics dev environment!"
      '';
    };

    # For `nix run`
    packages.${system}.default = app;
  };
}
