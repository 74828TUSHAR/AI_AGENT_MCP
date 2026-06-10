"""
generate_log_report.py
----------------------
Reads every *.log file from the logs directory and produces a single
self-contained log-report.html that Jenkins publishes via the
HTML Publisher plugin.

Usage:
    python scripts/generate_log_report.py \
        --logs-dir  ci-artifacts/ui/12/logs \
        --output    ci-artifacts/ui/12/log-report.html \
        --build     12 \
        --suite     UI
"""

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Log line classifier
# ---------------------------------------------------------------------------
def _classify(line: str) -> str:
    """Return a CSS class name for a single log line."""
    u = line.upper()
    if "TEST PASSED" in u:                          return "pass"
    if any(k in u for k in ("TEST FAILED", "ASSERTIONERROR", "FAILED")): return "fail"
    if " ERROR" in u or u.startswith("ERROR"):      return "error"
    if " WARNING" in u or " WARN" in u:             return "warn"
    if any(k in line for k in ("Scenario", "STEP", "scenario")): return "step"
    if " DEBUG" in u:                               return "debug"
    return "info"


def _status_from_content(content: str) -> str:
    """Derive overall test status from full log content."""
    if "TEST PASSED" in content:                    return "pass"
    if re.search(r"TEST FAILED|AssertionError|FAILED", content): return "fail"
    if "SKIPPED" in content.upper():               return "skip"
    return "info"


# ---------------------------------------------------------------------------
# HTML template helpers
# ---------------------------------------------------------------------------
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', Arial, sans-serif; background: #0d1117; color: #c9d1d9; }
header { background: #161b22; border-bottom: 1px solid #30363d;
         padding: 18px 32px; display: flex; align-items: center; gap: 14px; }
header h1 { font-size: 20px; font-weight: 600; color: #f0f6fc; }
.badge { padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
.badge-build { background: #1f6feb33; color: #58a6ff; border: 1px solid #1f6feb; }
.badge-suite { background: #388bfd1a; color: #79c0ff; border: 1px solid #388bfd55; }
.summary { display: flex; gap: 14px; padding: 18px 32px;
           background: #161b22; border-bottom: 1px solid #30363d; flex-wrap: wrap; }
.stat { background: #0d1117; border: 1px solid #30363d; border-radius: 8px;
        padding: 12px 20px; min-width: 110px; }
.stat-val   { font-size: 26px; font-weight: 700; }
.stat-label { font-size: 12px; color: #8b949e; margin-top: 2px; }
.passed  .stat-val { color: #3fb950; }
.failed  .stat-val { color: #f85149; }
.skipped .stat-val { color: #d29922; }
.total   .stat-val { color: #58a6ff; }
.container { padding: 22px 32px; }
.search-bar { width: 100%; padding: 10px 14px; background: #161b22;
  border: 1px solid #30363d; border-radius: 8px; color: #c9d1d9;
  font-size: 14px; margin-bottom: 16px; outline: none; }
.search-bar:focus { border-color: #58a6ff; }
.filter-bar { display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap; }
.filter-btn { padding: 5px 14px; border-radius: 20px; border: 1px solid #30363d;
  background: #0d1117; color: #8b949e; font-size: 12px; cursor: pointer; }
.filter-btn.active { border-color: #58a6ff; color: #58a6ff; background: #1f6feb22; }
.test-card { background: #161b22; border: 1px solid #30363d;
  border-radius: 8px; margin-bottom: 10px; overflow: hidden; }
.test-header { display: flex; align-items: center; gap: 12px;
  padding: 13px 18px; cursor: pointer; user-select: none; }
.test-header:hover { background: #1c2128; }
.status-icon { width: 22px; height: 22px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; flex-shrink: 0; }
.icon-pass  { background:#3fb95022; color:#3fb950; border:1.5px solid #3fb950; }
.icon-fail  { background:#f8514922; color:#f85149; border:1.5px solid #f85149; }
.icon-skip  { background:#d2992222; color:#d29922; border:1.5px solid #d29922; }
.icon-info  { background:#58a6ff22; color:#58a6ff; border:1.5px solid #58a6ff; }
.test-name  { font-size: 14px; font-weight: 500; color: #f0f6fc; flex: 1; }
.test-file  { font-size: 12px; color: #8b949e; }
.chevron    { color: #8b949e; font-size: 11px; transition: transform .2s; margin-left: 8px; }
.chevron.open { transform: rotate(90deg); }
.log-body   { display: none; border-top: 1px solid #30363d; }
.log-body.open { display: block; }
pre { background: #0d1117; padding: 14px 18px; overflow-x: auto;
  font-size: 12px; line-height: 1.75; white-space: pre-wrap; word-break: break-all; }
.l-pass  { color: #3fb950; }
.l-fail  { color: #f85149; font-weight: 600; }
.l-error { color: #ff7b72; font-weight: 600; }
.l-warn  { color: #d29922; }
.l-step  { color: #58a6ff; }
.l-debug { color: #484f58; }
.l-info  { color: #c9d1d9; }
.no-results { text-align:center; padding:40px; color:#8b949e; }
"""

JS = """
let currentFilter = 'all';

const icons = {
  pass: {cls:'icon-pass', sym:'&#10003;'},
  fail: {cls:'icon-fail', sym:'&#10007;'},
  skip: {cls:'icon-skip', sym:'&mdash;'},
  info: {cls:'icon-info', sym:'&#8505;'}
};

function renderSummary() {
  const s = SUMMARY;
  document.getElementById('summary').innerHTML =
    stat('total',   s.total,   'Total') +
    stat('passed',  s.passed,  'Passed') +
    stat('failed',  s.failed,  'Failed') +
    stat('skipped', s.skipped, 'Skipped');
}

function stat(cls, val, label) {
  return `<div class="stat ${cls}"><div class="stat-val">${val}</div><div class="stat-label">${label}</div></div>`;
}

function renderCards(list) {
  const c = document.getElementById('cards');
  const nr = document.getElementById('noResults');
  if (!list.length) { c.innerHTML=''; nr.style.display='block'; return; }
  nr.style.display = 'none';
  c.innerHTML = list.map((t, i) => {
    const ic = icons[t.status] || icons.info;
    return `<div class="test-card" data-status="${t.status}" data-idx="${i}">
      <div class="test-header" onclick="toggle(${i})">
        <div class="status-icon ${ic.cls}">${ic.sym}</div>
        <div class="test-name">${escHtml(t.name)}</div>
        <div class="test-file">${escHtml(t.file)}</div>
        <div class="chevron" id="chev-${i}">&#9654;</div>
      </div>
      <div class="log-body" id="body-${i}"><pre>${t.coloredHtml}</pre></div>
    </div>`;
  }).join('');
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function toggle(i) {
  const b = document.getElementById('body-'+i);
  const c = document.getElementById('chev-'+i);
  const open = b.classList.toggle('open');
  c.classList.toggle('open', open);
}

function getFiltered() {
  const q = document.getElementById('search').value.toLowerCase();
  return TESTS.filter(t => {
    const mf = currentFilter === 'all' || t.status === currentFilter;
    const ms = !q || t.name.toLowerCase().includes(q) || t.rawText.toLowerCase().includes(q);
    return mf && ms;
  });
}

function doFilter()   { renderCards(getFiltered()); }
function doSearch()   { renderCards(getFiltered()); }

function setFilter(f, btn) {
  currentFilter = f;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  doFilter();
}

renderSummary();
renderCards(TESTS);
"""


def _colored_html(content: str) -> str:
    """Convert raw log text to color-coded HTML spans (already html-escaped)."""
    lines = []
    for line in content.splitlines():
        cls = _classify(line)
        lines.append(f"<span class='l-{cls}'>{html.escape(line)}</span>")
    return "\n".join(lines)


def build_report(logs_dir: Path, output: Path, build_num: str, suite: str):
    log_files = sorted(logs_dir.glob("*.log"))
    if not log_files:
        print(f"WARNING: no .log files found in {logs_dir}")

    tests = []
    passed = failed = skipped = 0

    for lf in log_files:
        raw = lf.read_text(encoding="utf-8", errors="replace")
        status = _status_from_content(raw)
        name = re.sub(r"_test$", "", lf.stem)   # strip _test suffix
        colored = _colored_html(raw)
        tests.append({
            "name":       name,
            "file":       lf.name,
            "status":     status,
            "coloredHtml": colored,
            "rawText":    raw,
        })
        if status == "pass":   passed  += 1
        elif status == "fail": failed  += 1
        elif status == "skip": skipped += 1

    total = len(tests)
    summary = {"total": total, "passed": passed, "failed": failed, "skipped": skipped}

    # Build the JS data payload — we embed coloredHtml directly (already escaped)
    # rawText is lowercased for search; we strip HTML tags for plain-text search
    js_tests = []
    for t in tests:
        raw_plain = re.sub(r"<[^>]+>", "", t["coloredHtml"]).lower()
        entry = {
            "name":       t["name"],
            "file":       t["file"],
            "status":     t["status"],
            "coloredHtml": t["coloredHtml"],
            "rawText":    raw_plain,
        }
        js_tests.append(entry)

    # Serialize — coloredHtml is raw HTML so we cannot JSON-encode it naively;
    # instead we build a JS array literal where coloredHtml is a template-free string.
    js_array_items = []
    for t in js_tests:
        js_array_items.append(
            "{name:" + json.dumps(t["name"]) +
            ",file:" + json.dumps(t["file"]) +
            ",status:" + json.dumps(t["status"]) +
            ",rawText:" + json.dumps(t["rawText"]) +
            ",coloredHtml:" + json.dumps(t["coloredHtml"]) +
            "}"
        )
    js_array = "[" + ",\n".join(js_array_items) + "]"

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Test Log Report - Build {html.escape(build_num)}</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>&#128203; Test Log Report</h1>
  <span class="badge badge-build">Build #{html.escape(build_num)}</span>
  <span class="badge badge-suite">{html.escape(suite)} Suite</span>
</header>
<div id="summary" class="summary"></div>
<div class="container">
  <input class="search-bar" type="text" id="search"
         placeholder="Search test name or log content..." oninput="doSearch()">
  <div class="filter-bar">
    <button class="filter-btn active" onclick="setFilter('all',this)">All</button>
    <button class="filter-btn" onclick="setFilter('pass',this)">&#10003; Passed</button>
    <button class="filter-btn" onclick="setFilter('fail',this)">&#10007; Failed</button>
    <button class="filter-btn" onclick="setFilter('skip',this)">&mdash; Skipped</button>
  </div>
  <div id="cards"></div>
  <div class="no-results" id="noResults" style="display:none">No matching tests found.</div>
</div>
<script>
const SUMMARY = {json.dumps(summary)};
const TESTS   = {js_array};
{JS}
</script>
</body>
</html>
"""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(f"Log report written to: {output}  ({total} tests: {passed} passed, {failed} failed, {skipped} skipped)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML log report from pytest log files")
    parser.add_argument("--logs-dir",  required=True,  help="Directory containing *.log files")
    parser.add_argument("--output",    required=True,  help="Output HTML file path")
    parser.add_argument("--build",     default="?",    help="Jenkins build number")
    parser.add_argument("--suite",     default="UI",   help="Suite name (UI or API)")
    args = parser.parse_args()

    logs_path  = Path(args.logs_dir)
    output_path = Path(args.output)

    if not logs_path.exists():
        print(f"WARNING: logs directory does not exist: {logs_path}")
        sys.exit(0)   # soft exit — don't fail the build

    build_report(logs_path, output_path, args.build, args.suite)
