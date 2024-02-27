# Contributing

## Prerequisites

### Bash Shell

- Ensure you're using **Bash** as your shell.
- Verify with `echo $BASH_VERSION` in your terminal.

### Bash Version

- This project requires **Bash version 4.0 or higher**.
- Check with `bash --version`.
- Update Bash if your version is below 4.0.

### Python Requirements

- Some commands in this project require Python.
- Currently, the `install_requires` includes the following package:
  - `awscli` - AWS Command Line Interface for interacting with Amazon Web Services.
- Install the required Python packages using the following command:

```bash
pip install awscli
```

## Installing from source

ou can install the qBraid-CLI from source by cloning this repository and running a pip install command in the root directory:

```bash
git clone https://github.com/qBraid/qBraid-CLI.git
cd qBraid-CLI
pip install -e .
```

*Note*: The current CLI configuration assumes a Linux-based filesystem. However, our goal is to move towards a platform agnostic version soon.

You can verify that the setup has been successful by checking the qBraid-CLI version with the following command:

```bash
qbraid --version
```

## Build docs

To generate the API reference documentation locally, install the necessary requirements:

```shell
pip install -r docs/requirements.txt
```

Build the docs:

```shell
sphinx-build -W -b html docs docs/build/html
```

You can view the generated documentation in your browser (on OS X) using:

```shell
open docs/build/html/index.html
```
