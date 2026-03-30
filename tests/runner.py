#!/usr/bin/env python3
"""
#exonware/xwformats/tests/runner.py
Main test runner for xwformats - Production Excellence Edition
Orchestrates all test layer runners with Markdown output logging.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.2
Generation Date: 07-Jan-2025
Usage:
    python tests/runner.py                # Run all tests
    python tests/runner.py --core         # Run only core tests
    python tests/runner.py --unit         # Run only unit tests
    python tests/runner.py --integration  # Run only integration tests
    python tests/runner.py --advance      # Run only advance tests (v1.0.0+)
    python tests/runner.py --security     # Run only security tests
    python tests/runner.py --performance  # Run only performance tests
Output:
    - Terminal: Colored, formatted output
    - File: docs/logs/tests/TEST_<timestamp>_SUMMARY.md (Markdown-friendly format)
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
# ⚠️ CRITICAL: Configure UTF-8 encoding for Windows console using xwsystem utility (GUIDE_DEV.md compliance)
from exonware.xwsystem.console.cli import ensure_utf8_console
ensure_utf8_console()
# Try to use xwsystem utilities for better output
try:
    from exonware.xwsystem.utils.test_runner import (
        DualOutput, format_path, print_header, print_section, print_status
    )
    USE_XWSYSTEM_UTILS = True
except ImportError:
    USE_XWSYSTEM_UTILS = False


class SimpleDualOutput:
    """Simple fallback output handler."""

    def __init__(self, output_file: Path):
        self.output_file = output_file
        self.markdown_lines = []

    def print(self, text: str, markdown_format: str = None, color=None, emoji=None):
        """Print to terminal and capture for Markdown."""
        # Add emoji if provided
        if emoji and not USE_XWSYSTEM_UTILS:
            print(f"{emoji} {text}")
        else:
            print(text)
        self.markdown_lines.append(markdown_format if markdown_format else text)

    def save(self, metadata: dict = None):
        """Save Markdown output."""
        header = f"""# Test Runner Output
**Library:** xwformats
**Generated:** {datetime.now().strftime("%d-%b-%Y %H:%M:%S")}
**Runner:** Main Orchestrator
---
"""
        content = header + "\n".join(self.markdown_lines) + "\n"
        self.output_file.write_text(content, encoding='utf-8')


def run_sub_runner(runner_path: Path, description: str, output) -> int:
    """Run a sub-runner and return exit code."""
    if USE_XWSYSTEM_UTILS:
        print_section(description, output)
    else:
        print(f"\n{'='*80}")
        print(f"📂 {description}")
        print(f"{'='*80}\n")
    result = subprocess.run(
        [sys.executable, str(runner_path)],
        cwd=runner_path.parent,
        capture_output=True,
        text=True
    )
    # Print sub-runner output
    if result.stdout:
        print(result.stdout)
        if not USE_XWSYSTEM_UTILS:
            output.print(result.stdout, f"```\n{result.stdout}\n```")
    if result.stderr:
        print(result.stderr, file=sys.stderr)
        if not USE_XWSYSTEM_UTILS:
            output.print(result.stderr, f"**Errors:**\n```\n{result.stderr}\n```")
    status = "✅ PASSED" if result.returncode == 0 else "❌ FAILED"
    if USE_XWSYSTEM_UTILS:
        print_status(result.returncode == 0, status, output)
    else:
        output.print(f"\n{status}", f"\n**Result:** {status}\n")
    return result.returncode


def main():
    """Main test runner function following GUIDE_TEST.md."""
    test_dir = Path(__file__).parent
    root_dir = test_dir.parent
    # Canonical test evidence: docs/logs/tests/ (GUIDE_51_TEST / GUIDE_41_DOCS)
    reports_dir = root_dir / "docs" / "logs" / "tests"
    reports_dir.mkdir(parents=True, exist_ok=True)
    try:
        from exonware.xwsystem.utils.test_runner import timestamp_for_filename
    except ImportError:
        def timestamp_for_filename():
            n = datetime.now()
            return n.strftime("%Y%m%d_%H%M%S") + "_" + f"{n.microsecond//1000:03d}"
    timestamp = timestamp_for_filename()
    output_file = reports_dir / f"TEST_{timestamp}_SUMMARY.md"
    # Create output handler
    if USE_XWSYSTEM_UTILS:
        output = DualOutput(output_file)
        print_header("xwformats Test Runner - Hierarchical Orchestrator", output)
    else:
        output = SimpleDualOutput(output_file)
        output.print("="*80, "# Test Execution Report")
        output.print("xwformats Test Runner - Hierarchical Orchestrator",
                    "**Library:** xwformats\n**Type:** Main Orchestrator - Hierarchical Test Execution")
        output.print("="*80, "---")
    # Add src to Python path
    src_path = root_dir / "src"
    sys.path.insert(0, str(src_path))
    # Print test directory path
    if USE_XWSYSTEM_UTILS:
        output.print(
            f"Test Directory: {format_path(test_dir)}",
            f"**Test Directory:** `{format_path(test_dir)}`",
            emoji="📂"
        )
        output.print(
            f"Output File: {format_path(output_file)}",
            f"**Output File:** `{format_path(output_file)}`",
            emoji="📝"
        )
    else:
        output.print(f"Test Directory: {test_dir.resolve()}", 
                    f"**Test Directory:** `{test_dir.resolve()}`")
        output.print(f"Output File: {output_file.resolve()}",
                    f"**Output File:** `{output_file.resolve()}`")
    # Parse arguments
    args = sys.argv[1:]
    # Define sub-runners
    core_runner = test_dir / "0.core" / "runner.py"
    unit_runner = test_dir / "1.unit" / "runner.py"
    integration_runner = test_dir / "2.integration" / "runner.py"
    advance_runner = test_dir / "3.advance" / "runner.py"
    exit_codes = []
    # Determine which tests to run
    if "--core" in args:
        if core_runner.exists():
            exit_codes.append(run_sub_runner(core_runner, "Layer 0: Core Tests", output))
    elif "--unit" in args:
        if unit_runner.exists():
            exit_codes.append(run_sub_runner(unit_runner, "Layer 1: Unit Tests", output))
    elif "--integration" in args:
        if integration_runner.exists():
            exit_codes.append(run_sub_runner(integration_runner, "Layer 2: Integration Tests", output))
    elif "--advance" in args:
        if advance_runner.exists():
            exit_codes.append(run_sub_runner(advance_runner, "Layer 3: Advance Tests", output))
        else:
            msg = "⚠️  Advance tests not available (requires v1.0.0)"
            output.print(msg, f"> {msg}")
    elif "--security" in args or "--performance" in args:
        # Forward to advance runner if exists
        if advance_runner.exists():
            result = subprocess.run([sys.executable, str(advance_runner)] + args)
            exit_codes.append(result.returncode)
        else:
            msg = "⚠️  Advance tests not available (requires v1.0.0)"
            output.print(msg, f"> {msg}")
    else:
        # Run all tests in sequence
        output.print("\n🚀 Running: ALL Tests", "\n## Running All Test Layers")
        output.print("   Layers: 0.core → 1.unit → 2.integration → 3.advance", 
                    "**Execution Order:** 0.core → 1.unit → 2.integration → 3.advance\n")
        # Core tests
        if core_runner.exists():
            exit_codes.append(run_sub_runner(core_runner, "Layer 0: Core Tests", output))
        # Unit tests
        if unit_runner.exists():
            exit_codes.append(run_sub_runner(unit_runner, "Layer 1: Unit Tests", output))
        # Integration tests
        if integration_runner.exists():
            exit_codes.append(run_sub_runner(integration_runner, "Layer 2: Integration Tests", output))
        # Advance tests (if available)
        if advance_runner.exists():
            exit_codes.append(run_sub_runner(advance_runner, "Layer 3: Advance Tests", output))
    # Print summary
    output.print(f"\n{'='*80}", "\n---\n\n## 📊 Test Execution Summary")
    output.print("📊 TEST EXECUTION SUMMARY", "")
    output.print(f"{'='*80}", "")
    total_runs = len(exit_codes)
    passed = sum(1 for code in exit_codes if code == 0)
    failed = total_runs - passed
    output.print(f"Total Layers: {total_runs}", f"- **Total Layers:** {total_runs}")
    output.print(f"Passed: {passed}", f"- **Passed:** {passed}")
    output.print(f"Failed: {failed}", f"- **Failed:** {failed}")
    # Final status
    if all(code == 0 for code in exit_codes):
        final_msg = "✅ ALL TESTS PASSED!"
        output.print(f"\n{final_msg}", f"\n### {final_msg}\n")
        if USE_XWSYSTEM_UTILS:
            output.save({'library': 'xwformats', 'layer': 'main', 'description': 'Main Orchestrator'})
        else:
            output.save()
        print(f"\n📝 Test results saved to: {output_file}")
        sys.exit(0)
    else:
        final_msg = "❌ SOME TESTS FAILED!"
        output.print(f"\n{final_msg}", f"\n### {final_msg}\n")
        if USE_XWSYSTEM_UTILS:
            output.save({'library': 'xwformats', 'layer': 'main', 'description': 'Main Orchestrator'})
        else:
            output.save()
        print(f"\n📝 Test results saved to: {output_file}")
        sys.exit(1)
if __name__ == "__main__":
    main()
