# Xontrib Bash Completions Dirs

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?label=License&color=%234B78E6)](https://codeberg.org/taconi/xontrib-bash-completions-dirs/raw/branch/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/xontrib-bash-completions-dirs.svg?logo=pypi&label=PyPI&color=%23FA9BFA)](https://pypi.org/project/xontrib-bash-completions-dirs/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/xontrib-bash-completions-dirs.svg?logo=python&label=Python&color=%234B78E6)](https://pypi.python.org/pypi/xontrib-bash-completions-dirs/)
[![Downloads](https://img.shields.io/pypi/dm/xontrib-bash-completions-dirs?logo=pypi&label=Downloads&color=%2373DC8C)](https://pypi.org/project/xontrib-bash-completions-dirs/)

Autocomplete loading from directories.

## Installation

To install use xpip:

```sh
xpip install xontrib-bash-completions-dirs
```

or

```sh
xpip install -U git+https://codeberg.org/taconi/xontrib-bash-completions-dirs
```

## Usage

```sh
xontrib load bash_completions_dirs
 ```

Add the variable `BASH_COMPLETIONS_DIRS` (which must be an iterable of strings) with the paths of the directories that contain the autocomplete files.

For example:

```py
$BASH_COMPLETIONS_DIRS = ['/usr/share/bash-completion/completions']
```

### Note: The file name must be the same as the command to be used in autocomplete

For example, the file `/usr/share/bash-completion/completions/git` will be used to autocomplete the `git` command
