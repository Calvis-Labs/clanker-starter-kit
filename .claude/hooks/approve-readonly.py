#!/usr/bin/env python3
"""Auto-approve read-only bash, git, gh, and Linear operations so the dev loop
doesn't pepper the user with permission prompts for harmless reads.

Safety model: a command is auto-approved only if it (a) contains no shell
metacharacters that could chain/redirect/substitute another command, and
(b) matches a read-only pattern as a WHOLE command. Anything else falls
through to normal permission handling — we never widen access, only skip
prompts for things that are provably read-only."""

import json
import sys
import re

# Reject anything that could chain, redirect, substitute, or background a
# second command (e.g. `git status && rm -rf .`, `cat x > y`, `ls $(...)`).
SHELL_META = re.compile(r'[;&|`$(){}<>\n\\]')

# Read-only command patterns, matched against the FULL command with re.fullmatch.
# Trailing args are allowed via (\s.*)? but metacharacters are already excluded
# above, so args can only be plain words/paths/flags.
READONLY_BASH_PATTERNS = [
    r'git\s+(status|diff|log|show|branch|worktree\s+list|remote(\s+-v)?|config\s+--get|rev-parse|merge-base)(\s.*)?',
    r'gh\s+(pr|issue)\s+(view|list|status)(\s.*)?',
    r'gh\s+repo\s+view(\s.*)?',
    r'ls(\s.*)?',
    r'cat\s.+',
    r'grep\s.+',
    r'rg\s.+',
    r'find\s.+',
    r'pwd',
    r'which\s+\S.*',
]

# Read-only Linear operations (only relevant when the tracker is Linear)
READONLY_LINEAR_OPS = [
    'get_issue',
    'list_issues',
    'get_project',
    'list_projects',
    'get_team',
    'list_teams',
    'get_user',
    'list_users',
    'list_comments',
    'list_cycles',
    'get_document',
    'list_documents',
    'list_issue_statuses',
    'get_issue_status',
    'list_issue_labels',
    'list_project_labels',
    'search_documentation',
]


def allow(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "permissionDecision": "allow",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


try:
    input_data = json.load(sys.stdin)
    tool_name = input_data.get('tool_name', '')

    if tool_name == 'Bash':
        command = input_data.get('tool_input', {}).get('command', '').strip()
        # Only auto-approve a single, metacharacter-free, fully-matched command.
        if command and not SHELL_META.search(command):
            for pattern in READONLY_BASH_PATTERNS:
                if re.fullmatch(pattern, command, re.IGNORECASE):
                    allow("Read-only command auto-approved")

    if tool_name.startswith('mcp__linear__'):
        operation = tool_name.replace('mcp__linear__', '')
        if operation in READONLY_LINEAR_OPS:
            allow("Read-only Linear operation auto-approved")

    # Not provably read-only — fall through to normal permission handling.
    sys.exit(0)

except Exception as e:
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)
