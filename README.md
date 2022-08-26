<div align="center">

[![CodeQL Scan](https://github.com/thoroc/py-documentation-generator/actions/workflows/codeql.yml/badge.svg)](https://github.com/thoroc/py-documentation-generator/actions/workflows/codeql.yml)

</div>

This project aim to provide documentation generator.

- mailmap: generate mailmap file
- module listing: generate markdown file listing modules (see [example](docs/MODULES.md))
- logger message: generate markdown file listing all log calls (see [example](docs/LOGGED_MESSAGES.md))


run the test using pytest runner: `pytest .\py-documentation-generator\ -x -vvv -s -o log_cli=true`
