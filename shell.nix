{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pkgs.ruff
    pkgs.pyright
    pkgs.sqlite
    pkgs.openldap.dev
    pkgs.cyrus_sasl.dev
  ];
}
