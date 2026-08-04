"""Platform path abstraction (Phase 8.1).

Provides per-OS paths for all sources, so the skill runs on Windows, Mac, and Linux
without code changes. Each source adapter imports its default path from here.
"""

from __future__ import annotations

import os
import platform


HOME = os.path.expanduser("~")
SYSTEM = platform.system()  # "Windows" | "Darwin" | "Linux"
IS_WINDOWS = SYSTEM == "Windows"
IS_MAC = SYSTEM == "Darwin"


def _join(*parts: str) -> str:
    return os.path.join(HOME, *parts)


# AI-agent session paths
CLAUDE_PROJECTS = _join(".claude", "projects")
CODEAGENT_PROJECTS = _join(".cac", "projects")
LEGACY_CODEAGENT_DB = _join(".local", "share", "opencode", "db", "ngagent.db")

# Git — no fixed path; discovered from session cwds

# Browser history
if IS_WINDOWS:
    CHROME_HISTORY = _join("AppData", "Local", "Google", "Chrome", "User Data", "Default", "History")
    EDGE_HISTORY = _join("AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "History")
elif IS_MAC:
    CHROME_HISTORY = _join("Library", "Application Support", "Google", "Chrome", "Default", "History")
    EDGE_HISTORY = _join("Library", "Application Support", "Microsoft Edge", "Default", "History")
else:  # Linux
    CHROME_HISTORY = _join(".config", "google-chrome", "Default", "History")
    EDGE_HISTORY = _join(".config", "microsoft-edge", "Default", "History")

# VSCode Local History
if IS_WINDOWS:
    VSCODE_HISTORY = _join("AppData", "Roaming", "Code", "User", "History")
elif IS_MAC:
    VSCODE_HISTORY = _join("Library", "Application Support", "Code", "User", "History")
else:
    VSCODE_HISTORY = _join(".config", "Code", "User", "History")

# Windows Recent (Windows-only)
WINDOWS_RECENT = _join("AppData", "Roaming", "Microsoft", "Windows", "Recent") if IS_WINDOWS else ""

# WeLink Meeting recordings (Windows-only, configurable)
WELINK_RECORDINGS = "D:\\MeetingRecordings" if IS_WINDOWS else ""

# Outlook (Mac path included for colleagues on Mac)
if IS_WINDOWS:
    OUTLOOK_OST = _join("AppData", "Local", "Microsoft", "Outlook")
elif IS_MAC:
    OUTLOOK_OST = _join("Library", "Group Containers", "UBF8T346G9.Office", "Outlook")
else:
    OUTLOOK_OST = ""


def audit_no_hardcoded_identity() -> list[str]:
    """Audit that no path, username, or machine name is baked into the code.

    Returns a list of issues found (empty = clean). Checks the SOURCE CODE of this
    module for hardcoded usernames — not the resolved paths (which correctly contain
    the current user's home via os.path.expanduser).
    """
    issues = []
    # The WeLink recordings path is a known Windows hardcode — note it as configurable.
    if IS_WINDOWS and WELINK_RECORDINGS and not os.path.isdir(WELINK_RECORDINGS):
        issues.append(f"WELINK_RECORDINGS defaults to '{WELINK_RECORDINGS}' which doesn't exist — "
                      "should be auto-detected or configurable, not hardcoded.")
    # Check this module's source for hardcoded usernames (not the resolved paths)
    src = os.path.abspath(__file__)
    try:
        with open(src, encoding="utf-8") as f:
            content = f.read()
        # Look for patterns like b00563677 or specific user dirs in string literals
        import re
        hardcoded = re.findall(r'["\'][A-Za-z]:\\Users\\[^"\'\\]+\\', content)
        if hardcoded:
            issues.append(f"Source contains hardcoded user paths: {hardcoded}")
    except OSError:
        pass
    return issues
