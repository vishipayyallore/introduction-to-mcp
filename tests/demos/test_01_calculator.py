"""Tests for ``src/demos/01-calculator`` (settings + tool/resource/prompt callables).

FastMCP's ``@mcp.tool()`` returns the original function, so we exercise math and messages without
starting a server or MCP transport.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_DEMO = Path(__file__).resolve().parents[2] / "src" / "demos" / "01-calculator"
assert _DEMO.is_dir(), f"Expected demo folder: {_DEMO}"
if str(_DEMO) not in sys.path:
    sys.path.insert(0, str(_DEMO))

import server  # noqa: E402
import settings  # noqa: E402


def test_load_config_required_keys() -> None:
    cfg = settings.load_config()
    assert "host" in cfg
    assert "port" in cfg
    assert "transport" in cfg
    assert "server" in cfg and "name" in cfg["server"]
    assert "log_level" in cfg


def test_add_subtract_multiply() -> None:
    assert server.add(2.0, 3.0) == 5.0
    assert server.subtract(10.0, 3.0) == 7.0
    assert server.multiply(4.0, 2.5) == 10.0


def test_divide() -> None:
    assert server.divide(10.0, 4.0) == 2.5


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ValueError, match="Division by zero"):
        server.divide(10.0, 0.0)


def test_calculation_help_mentions_operations() -> None:
    text = server.calculation_help()
    assert "add" in text.lower()
    assert "divide" in text.lower()


def test_evaluate_prompt_includes_expression() -> None:
    expr = "2 + 2"
    prompt = server.evaluate(expr)
    assert expr in prompt
    assert "calculator" in prompt.lower()
