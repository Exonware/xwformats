#!/usr/bin/env python3
"""
Pytest configuration for xwformats tests.
Tests align with REF_01_REQ and REF_51_TEST. Key code paths per REF_14_DX
(XWFormats, convert, list_formats, get_serializer).
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 04-Nov-2025
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


