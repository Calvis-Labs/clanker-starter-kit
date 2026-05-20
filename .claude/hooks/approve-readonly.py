#!/usr/bin/env python3
"""Auto-approve read-only bash, git, gh, and Linear operations so the dev loop
doesn't pepper the user with permission prompts for harmless reads."""

import json
import sys
import re

# Read-only shell command patterns
READONLY_BASH_PATTERNS = [
    r'^git\s+(status|diff|log|show|branch|worktree\s+list|remote(\s+-v)?|config\s+--get|rev-parse|merge-base)',
    r'^gh\s+(pr|issue)\s+(view|list|status)',
    r'^gh\s+repo\s+view',
    r'^ls\s+',
    r'^cat\s+',
    r'^grep\s+',
    r'^rg\s+',
    r'^find\s+',
    r'^pwd',
    r'^which\s+',
    r'^echo\s+\$',  # environment variables
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
        command = input_data.get('tool_input', {}).get('command', '')
        for pattern in READONLY_BASH_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                allow("Read-only command auto-approved")

    if tool_name.startswith('mcp__linear__'):
        operation = tool_name.replace('mcp__linear__', '')
        if operation in READONLY_LINEAR_OPS:
            allow("Read-only Linear operation auto-approved")

    # Not read-only — fall through to normal permission handling.
    sys.exit(0)

except Exception as e:
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(1)
