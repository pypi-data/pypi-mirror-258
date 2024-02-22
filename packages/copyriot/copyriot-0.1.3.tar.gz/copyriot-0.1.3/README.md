# CopyRiot

## Introduction

CopyRiot simplifies the process of adding copyright and license information to your digital content. It supports various file formats, helping to ensure that intellectual property is properly documented across codebase.

## Getting Started

### Prerequisites and installation

CopyRiot is available on PyPi.

```bash
python -m pip install copyriot
```

Ensure you have met the following requirements:

- Python 3.8 or later

### Usage

For a directory: To apply copyright or license headers to all files within a directory, use

```bash
copyriot --header "Copyright YEAR. All Rights Reserved" --directory <directory_path>
```

For individual files: To target a specific file, the command is

```bash
copyriot --header "Copyright YEAR. All Rights Reserved" --file <file_path>
```

For multiple lines: To include multiple lines of copyright or license information, simply:

```bash
copyriot --header "Copyright YEAR. All Rights Reserved" "License information" --directory <directory_path>
copyriot --header "Copyright YEAR. All Rights Reserved" "License information" --file <file_path>
```

### Use CopyRiot as pre-commit hook

To add a copyright pre-commit hook, add these lines in your .pre-commit-configs.yaml

```yaml
  - repo: https://gitlab.com/jeeeunit/copyriot.git
    rev: 0.1.2
    hooks:
      - id: copyriot
        args: [-t, "Add copyright", "Add license", -f]
        alias: copyriot
        name: Add copyrights
        log_file: lint_output/copyriot_results
```

You can also configure the pattern of files to run on or exclude by setting 'files' or 'exclude' using regular expressions. Please
refer [pre-commit documentation](https://pre-commit.com/)

## Support

If you encounter any issues or have questions, please create an issue on [our git
repo](https://gitlab.com/jeeeunit/copyriot/-/issues) and we'll get back to you shortly.

## Contributing

We welcome contributions to CopyRiot! If you have suggestions for improvements or want to contribute code, please open a MR.
