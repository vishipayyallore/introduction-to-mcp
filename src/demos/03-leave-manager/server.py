"""Leave Manager MCP server — SQLite-backed HR demo with **async tools** (Demo 03).

HTTP mode (http://127.0.0.1:8002/mcp):

    uv run python src/demos/03-leave-manager/server.py

Stdio (Inspector / subprocess clients):

    uv run python src/demos/03-leave-manager/server.py --transport stdio

Mutating tools await a short sleep (simulated HR latency) and run SQLite work in a worker
thread via ``asyncio.to_thread`` so the event loop stays responsive — the pattern this demo
teaches for async MCP servers backed by blocking I/O.
"""

from __future__ import annotations

import argparse
import asyncio
from functools import partial

from mcp.server.fastmcp import FastMCP

import leave_db
from settings import load_config

_CONFIG = load_config()

mcp = FastMCP(
    _CONFIG["server"]["name"],
    host=_CONFIG["host"],
    port=_CONFIG["port"],
    log_level=_CONFIG["log_level"],
    json_response=True,
)

# Tunable delays so Inspector / clients visibly interleave concurrent calls (try two clients).
_SIM_HR_ROUND_TRIP_S = 0.22
_SIM_QUERY_S = 0.06


# --- Resources (sync reads; FastMCP runs them on the server thread pool as needed) -----------


@mcp.resource("employees://all")
def resource_all_employees() -> str:
    """Directory of employees and leave balances."""
    return leave_db.format_all_employees()


@mcp.resource("employee://{employee_id}")
def resource_employee(employee_id: str) -> str:
    """Single employee profile and balances."""
    return leave_db.format_employee_info(employee_id)


@mcp.resource("leave-requests://all")
def resource_all_leave_requests() -> str:
    """All leave requests in the database."""
    return leave_db.format_all_leave_requests()


@mcp.resource("leave-requests://employee/{employee_id}")
def resource_leave_for_employee(employee_id: str) -> str:
    """Leave requests for one employee."""
    return leave_db.format_employee_leave_requests(employee_id)


@mcp.resource("leave-requests://status/{status}")
def resource_leave_by_status(status: str) -> str:
    """Filter requests by status (pending, approved, denied)."""
    return leave_db.format_requests_by_status(status)


# --- Async tools (blocking SQLite executed in ``asyncio.to_thread``) ----------------------------


@mcp.tool()
async def submit_leave_request(
    employee_id: str,
    start_date: str,
    end_date: str,
    leave_type: str,
    reason: str,
    days_requested: int,
) -> str:
    """Submit a new leave request (async — simulated HR round-trip + background DB write)."""
    await asyncio.sleep(_SIM_HR_ROUND_TRIP_S)
    return await asyncio.to_thread(
        leave_db.submit_leave_request_impl,
        employee_id,
        start_date,
        end_date,
        leave_type,
        reason,
        days_requested,
    )


@mcp.tool()
async def approve_leave_request(request_id: str, approver_name: str) -> str:
    """Approve a pending request and adjust balances (async)."""
    await asyncio.sleep(_SIM_HR_ROUND_TRIP_S)
    return await asyncio.to_thread(
        leave_db.approve_leave_request_impl,
        request_id,
        approver_name,
    )


@mcp.tool()
async def check_leave_balance(employee_id: str) -> str:
    """Return remaining annual/sick leave for an employee (async query)."""
    await asyncio.sleep(_SIM_QUERY_S)
    return await asyncio.to_thread(leave_db.check_leave_balance_impl, employee_id)


@mcp.tool()
async def get_pending_approvals() -> str:
    """List pending requests awaiting approval (async query)."""
    await asyncio.sleep(_SIM_QUERY_S)
    return await asyncio.to_thread(leave_db.get_pending_approvals_impl)


@mcp.tool()
async def get_database_stats() -> str:
    """Aggregate counts for employees and requests (async query)."""
    await asyncio.sleep(_SIM_QUERY_S)
    return await asyncio.to_thread(leave_db.get_database_stats_impl)


@mcp.tool()
async def add_employee(
    name: str,
    department: str,
    manager: str,
    annual_leave_balance: int = 25,
    sick_leave_balance: int = 10,
    force_create: bool = False,
) -> str:
    """Add an employee with fuzzy duplicate detection (async HR + DB)."""
    await asyncio.sleep(_SIM_HR_ROUND_TRIP_S)
    fn = partial(
        leave_db.add_employee_impl,
        name,
        department,
        manager,
        annual_leave_balance,
        sick_leave_balance,
        force_create,
    )
    return await asyncio.to_thread(fn)


if __name__ == "__main__":
    leave_db.init_database()
    parser = argparse.ArgumentParser(description="Leave Manager MCP server (FastMCP).")
    parser.add_argument(
        "--transport",
        default=None,
        metavar="NAME",
        help='Override config transport (e.g. "stdio" or "streamable-http"). '
        "Default: value from config/settings.json.",
    )
    ns = parser.parse_args()
    transport = ns.transport if ns.transport is not None else _CONFIG["transport"]
    mcp.run(transport=transport)
