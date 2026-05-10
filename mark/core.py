"""Mark — Markdown toolkit core."""

import re
import os
from typing import List, Dict, Optional
from collections import Counter


def parse_headings(content: str) -> List[Dict]:
    """Extract headings from markdown content."""
    headings = []
    for i, line in enumerate(content.split("\n"), 1):
        m = re.match(r'^(#{1,6})\s+(.+?)(?:\s+#+)?$', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            anchor = text.lower().replace(" ", "-").replace(/[^a-z0-9-]/g, "")
            headings.append({"level": level, "text": text, "line": i, "anchor": anchor})
    return headings


def generate_toc(content: str, max_depth: int = 6, include_top: bool = False) -> str:
    """Generate a table of contents from markdown."""
    headings = parse_headings(content)
    if not include_top and headings and headings[0]["level"] == 1:
        headings = headings[1:]
    
    lines = []
    for h in headings:
        if h["level"] > max_depth:
            continue
        indent = "  " * (h["level"] - 1)
        anchor = h["text"].lower().replace(" ", "-")
        anchor = re.sub(r'[^a-z0-9-]', "", anchor)
        lines.append(f"{indent}- [{h['text']}](#{anchor})")
    
    return "\n".join(lines)


def find_links(content: str) -> List[Dict]:
    """Find all markdown links."""
    links = []
    # Inline links: [text](url)
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
        links.append({"type": "inline", "text": m.group(1), "url": m.group(2)})
    # Reference-style links: [text][ref]
    for m in re.finditer(r'\[([^\]]+)\]\[([^\]]*)\]', content):
        links.append({"type": "reference", "text": m.group(1), "ref": m.group(2)})
    # Auto links: <url>
    for m in re.finditer(r'<([a-zA-Z][a-zA-Z0-9+.-]*://[^>]+)>', content):
        links.append({"type": "auto", "url": m.group(1)})
    return links


def check_links(content: str) -> List[Dict]:
    """Check for broken reference links."""
    links = find_links(content)
    
    # Build reference definitions
    refs = {}
    for m in re.finditer(r'^\[([^\]]+)\]:\s*(\S+)(?:\s+"[^"]*")?', content, re.MULTILINE):
        refs[m.group(1).lower()] = m.group(2)
    
    issues = []
    for link in links:
        if link["type"] == "reference":
            ref_key = link["ref"].lower() if link["ref"] else link["text"].lower()
            if ref_key not in refs:
                issues.append({"type": "broken_ref", "text": link["text"], "ref": link["ref"]})
        elif link["type"] == "inline":
            url = link["url"]
            # Check for local files
            if url.startswith("./") or url.startswith("../") or url == url:
                if not url.startswith("http") and not url.startswith("#"):
                    resolved = os.path.join(os.path.dirname(os.path.abspath(".")), url)
                    if not os.path.exists(url):
                        issues.append({"type": "broken_local", "url": url, "text": link["text"]})
    
    return issues


def lint_markdown(content: str) -> List[Dict]:
    """Lint markdown for common issues."""
    issues = []
    lines = content.split("\n")
    
    for i, line in enumerate(lines, 1):
        # Check for trailing whitespace
        if line != line.rstrip():
            issues.append({"line": i, "severity": "warning", "message": "Trailing whitespace"})
        
        # Check for multiple blank lines
        if i > 1 and line == "" and lines[i-2] == "":
            issues.append({"line": i, "severity": "warning", "message": "Multiple consecutive blank lines"})
        
        # Check for very long lines
        if len(line) > 200:
            issues.append({"line": i, "severity": "info", "message": f"Line too long ({len(line)} chars)"})
        
    # Check for missing final newline
    if lines and lines[-1] != "":
        issues.append({"line": len(lines), "severity": "warning", "message": "No trailing newline"})
    
    # Check heading levels (don't skip levels)
    headings = parse_headings(content)
    prev_level = 0
    for h in headings:
        if h["level"] > prev_level + 1 and prev_level > 0:
            issues.append({"line": h["line"], "severity": "warning",
                           "message": f"Skipped heading level: h{prev_level} -> h{h['level']}"})
        prev_level = h["level"]
    
    return issues


def compute_stats(content: str) -> Dict:
    """Compute markdown document statistics."""
    lines = content.split("\n")
    headings = parse_headings(content)
    links = find_links(content)
    
    total_chars = len(content)
    total_lines = len(lines)
    non_empty = sum(1 for l in lines if l.strip())
    
    code_blocks = len(re.findall(r'```', content)) // 2
    lists = len(re.findall(r'^[\s]*[-*+]\s', content, re.MULTILINE))
    tables = len(re.findall(r'^\|.*\|$', content, re.MULTILINE))
    
    word_count = len(content.split())
    
    return {
        "lines": total_lines,
        "non_empty": non_empty,
        "characters": total_chars,
        "words": word_count,
        "headings": len(headings),
        "links": len(links),
        "code_blocks": code_blocks,
        "list_items": lists,
        "table_rows": tables,
        "avg_line_length": round(total_chars / max(total_lines, 1), 1),
    }


def format_stats(stats: Dict) -> str:
    """Format markdown statistics."""
    lines = [
        "=" * 48,
        "  Markdown Document Statistics",
        "=" * 48,
        f"  Lines:       {stats['lines']} ({stats['non_empty']} non-empty)",
        f"  Words:       {stats['words']}",
        f"  Characters:  {stats['characters']}",
        f"  Avg line:    {stats['avg_line_length']} chars",
        f"  Headings:    {stats['headings']}",
        f"  Links:       {stats['links']}",
        f"  Code blocks: {stats['code_blocks']}",
        f"  List items:  {stats['list_items']}",
        f"  Table rows:  {stats['table_rows']}",
    ]
    return "\n".join(lines)


def format_toc(toc: str) -> str:
    """Format TOC output."""
    lines = ["Table of Contents", "=" * 20, ""]
    lines.append(toc)
    lines.append("")
    return "\n".join(lines)
