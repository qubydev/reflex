"""Regression tests for reflex/utils/exec.py."""

import re

import pytest
from reflex_base.constants import ReactRouter


@pytest.mark.parametrize(
    ("vite_log_line", "expected_url"),
    [
        ("  Local:   http://localhost:3000/", "http://localhost:3000/"),
        ("  Local:   http://localhost:3000/withslash/", "http://localhost:3000/withslash/"),
        # No leading slash: Vite still bakes the path, must not be doubled.
        ("  Local:   http://localhost:3000/noslash/", "http://localhost:3000/noslash/"),
        ("  Local:   http://localhost:3000/a/b/", "http://localhost:3000/a/b/"),
    ],
)
def test_vite_url_captured_without_doubling(vite_log_line: str, expected_url: str):
    """Vite's log URL already contains the frontend_path; exec.py must not append it again.

    Args:
        vite_log_line: A simulated line from the Vite dev-server stdout.
        expected_url: The URL that should be extracted from the log line.
    """
    match = re.search(ReactRouter.FRONTEND_LISTENING_REGEX, vite_log_line)
    assert match is not None
    assert match.group(1) == expected_url
