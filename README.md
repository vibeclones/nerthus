# nerthus (Vibeclones mirror)

Hosted browser builds of [Nerthus](https://github.com/danemadsen/nerthus), a clean-room reimplementation of Gaea 2, the node-based terrain generator, written in Rust, by [danemadsen](https://github.com/danemadsen). The code is theirs; this repo only builds and hosts it. The project's own web app is at https://nerthus.app, and it also ships desktop downloads.

- Latest: `/nerthus/latest/`
- A specific version: `/nerthus/v<version>/`, for example `/nerthus/v1.0.0/`
- Version list: `/nerthus/versions.json`

The author's releases carry only desktop downloads, so each version is built from its release tag with the project's own web build (`crates/nerthus-app/web/build.sh`): the editor compiled to WebAssembly, wasm-bindgen's JavaScript and the start page. One change: the WebAssembly is over GitHub's 100 MB file limit, so it is stored in parts and the start page joins them as it loads. A scheduled workflow builds new releases.

**License:** Nerthus is MIT. Every version folder includes the license file and a `SOURCE.txt` naming the exact upstream tag it was built from.
