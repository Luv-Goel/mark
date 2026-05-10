# Mark ðŸ“

<div align="center">

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-lightgrey)]()

**Markdown toolkit â€” generate TOC, lint, check-links, format, and get stats. Zero dependencies.**

</div>

---

## Features

- **Table of Contents** â€” Auto-generate TOC from heading structure
- **Lint** â€” Check markdown for style issues, broken syntax, common errors
- **Check Links** â€” Validate all internal and external links
- **Format** â€” Normalize whitespace, heading styles, list formatting
- **Stats** â€” Word count, heading analysis, reading time estimates
- **Merge** â€” Combine multiple markdown files with TOC generation
- **Zero dependencies** â€” Pure Python 3.8+, stdlib only

## Quick Start

```bash
pip install mark-toolkit

# Generate table of contents
mark toc README.md

# Lint markdown file
mark lint README.md

# Check all links
mark check-links README.md

# Get document stats
mark stats README.md

# Format markdown
mark format README.md
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `mark toc [file]` | Generate table of contents |
| `mark lint [file]` | Lint markdown for style and syntax issues |
| `mark check-links [file]` | Validate all links in document |
| `mark format [file]` | Normalize and format markdown |
| `mark stats [file]` | Word count, heading analysis, reading time |
| `mark merge [files...]` | Merge multiple markdown files |

## Architecture

```
mark/
â”œâ”€â”€ mark/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ cli.py       # CLI entry point
â”‚   â””â”€â”€ core.py      # TOC, lint, links, format, stats
â”œâ”€â”€ pyproject.toml
â””â”€â”€ README.md
```

## License

MIT â€” see [LICENSE](LICENSE).
