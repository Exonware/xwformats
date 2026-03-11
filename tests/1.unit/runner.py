#!/usr/bin/env python3
"""
#exonware/xwformats/tests/1.unit/runner.py
Runner for unit tests (1.unit layer).
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.2
Generation Date: 07-Jan-2025
"""

import sys
from pathlib import Path
import subprocess
# ⚠️ CRITICAL: Configure UTF-8 encoding for Windows console using xwsystem utility (GUIDE_DEV.md compliance)
from exonware.xwsystem.console.cli import ensure_utf8_console
ensure_utf8_console()
# Try to use xwsystem utilities
try:
    from exonware.xwsystem.utils.test_runner import run_pytest, format_path, print_header
    USE_XWSYSTEM_UTILS = True
except ImportError:
    USE_XWSYSTEM_UTILS = False


def main():
    """Run unit tests. Layer runners stream to stdout/stderr only (no files)."""
    test_dir = Path(__file__).parent
    root_dir = test_dir.parent.parent
    # Add src to Python path
    src_path = root_dir / "src"
    sys.path.insert(0, str(src_path))
    # Print header
    if USE_XWSYSTEM_UTILS:
        print_header("Unit Tests - Component-Level Tests")
        print(f"Directory: {format_path(test_dir)}")
        result = run_pytest(
            test_dir=test_dir,
            markers=["xwformats_unit"],
            cwd=root_dir
        )
        sys.exit(result.exit_code)
    else:
        # Fallback: simple pytest call
        print("=" * 80)
        print("Unit Tests - Component-Level Tests")
        print("=" * 80)
        print(f"Directory: {test_dir.resolve()}\n")
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_dir),
            "-v",
            "--tb=short",
            "-x",
            "--strict-markers",
            "-m", "xwformats_unit"
        ]
        result = subprocess.run(cmd, cwd=root_dir)
        sys.exit(result.returncode)
if __name__ == "__main__":
    main()
