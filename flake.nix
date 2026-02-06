{
  description = "Dev shell for ESP-IDF / ESP-Matter Ansible automation";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            ansible
            ansible-lint
            yamllint
            prek
            uv
            python3
            git
            wget
          ];
        };
      });
}
