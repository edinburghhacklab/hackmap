{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pkgs.ruff
    pkgs.pyright
  ];
}
