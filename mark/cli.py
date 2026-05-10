"""Mark CLI."""

import argparse
import sys
import os
from . import __version__
from .core import (
    generate_toc, compute_stats, format_stats, format_toc,
    lint_markdown, check_links,
)


def main():
    parser = argparse.ArgumentParser(prog="mark", description="Markdown toolkit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("toc", help="Generate table of contents")
    p.add_argument("file")
    p.add_argument("--max-depth", type=int, default=6)
    p.add_argument("--include-top", action="store_true")

    p = sub.add_parser("stats", help="Document statistics")
    p.add_argument("file")

    p = sub.add_parser("lint", help="Lint markdown for issues")
    p.add_argument("file")

    p = sub.add_parser("check-links", help="Check for broken links")
    p.add_argument("file")

    p = sub.add_parser("format", help="Format markdown (basic)")
    p.add_argument("file")
    p.add_argument("-o", "--output", default=None)

    p = sub.add_parser("merge", help="Merge markdown files")
    p.add_argument("files", nargs="+")
    p.add_argument("-o", "--output", required=True)

    args = parser.parse_args()

    if args.command in ("toc", "stats", "lint", "check-links", "format"):
        if not os.path.exists(args.file):
            print(f"[ERR] File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

        if args.command == "toc":
            toc = generate_toc(content, args.max_depth, args.include_top)
            if toc:
                print(format_toc(toc))
            else:
                print("  No headings found.")

        elif args.command == "stats":
            print(format_stats(compute_stats(content)))

        elif args.command == "lint":
            issues = lint_markdown(content)
            if issues:
                sev_count = Counter(i["severity"] for i in issues)
                print(f"  Issues: {len(issues)} ({sev_count.get('warning', 0)} warnings, {sev_count.get('info', 0)} info)")
                for issue in issues:
                    print(f"  [{issue['severity'].upper():>7}] L{issue['line']}: {issue['message']}")
            else:
                print("  [OK] No issues found.")

        elif args.command == "check-links":
            issues = check_links(content)
            if issues:
                print(f"  Link issues: {len(issues)}")
                for issue in issues:
                    if issue["type"] == "broken_ref":
                        print(f"    Broken reference: [{issue['text']}][{issue.get('ref', '')}]")
                    elif issue["type"] == "broken_local":
                        print(f"    Broken local link: [{issue['text']}]({issue.get('url', '')})")
            else:
                print("  [OK] All links appear valid.")

        elif args.command == "format":
            from .core import lint_markdown
            # Basic formatting: normalize trailing whitespace, ensure final newline
            lines = content.split("\n")
            # Remove trailing whitespace
            lines = [l.rstrip() for l in lines]
            # Remove excessive blank lines (max 1)
            result = []
            prev_blank = False
            for l in lines:
                if l == "":
                    if prev_blank:
                        continue
                    prev_blank = True
                else:
                    prev_blank = False
                result.append(l)
            # Ensure trailing newline
            result.append("")
            formatted = "\n".join(result)
            out_path = args.output or args.file
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"[OK] Formatted {out_path}")

    elif args.command == "merge":
        all_content = []
        for f in args.files:
            if not os.path.exists(f):
                print(f"[ERR] File not found: {f}", file=sys.stderr)
                sys.exit(1)
            with open(f, "r", encoding="utf-8") as fh:
                all_content.append(fh.read().rstrip())
        merged = "\n\n---\n\n".join(all_content)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(merged)
            f.write("\n")
        print(f"[OK] Merged {len(args.files)} files into {args.output}")


if __name__ == "__main__":
    main()
