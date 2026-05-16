"""Project Tracker MCP server - SQLite tickets/projects with templated resources (Demo 04).

HTTP mode (http://127.0.0.1:8003/mcp):

    uv run python src/demos/04-project-tracker/server.py

Stdio:

    uv run python src/demos/04-project-tracker/server.py --transport stdio

Resources use URI templates (for example ``ticket://TK001``, ``tickets://for-project/PROJ001``)
so clients resolve **stable paths over evolving database state** - the focus of Demo 04.
"""

from __future__ import annotations

import argparse

import tracker_db
from mcp.server.fastmcp import FastMCP
from settings import load_config

_CONFIG = load_config()

mcp = FastMCP(
    _CONFIG["server"]["name"],
    host=_CONFIG["host"],
    port=_CONFIG["port"],
    log_level=_CONFIG["log_level"],
    json_response=True,
)


@mcp.resource("tickets://all")
def resource_all_tickets() -> str:
    """List every ticket (snapshot of DB state)."""
    return tracker_db.format_all_tickets()


@mcp.resource("ticket://{ticket_id}")
def resource_ticket_detail(ticket_id: str) -> str:
    """Single ticket by id (dynamic URI segment)."""
    return tracker_db.format_ticket_details(ticket_id)


@mcp.resource("tickets://for-project/{project_id}")
def resource_tickets_for_project(project_id: str) -> str:
    """Tickets belonging to a project; ``project_id`` is ``PROJ001``-style (stable in URIs)."""
    return tracker_db.format_tickets_for_project_id(project_id)


@mcp.resource("tickets://status/{status}")
def resource_tickets_by_status(status: str) -> str:
    """Filter by workflow status (pending, in_progress, completed, closed)."""
    return tracker_db.format_tickets_by_status(status)


@mcp.resource("tickets://assignee/{assignee}")
def resource_tickets_by_assignee(assignee: str) -> str:
    """Tickets assigned to a person (name segment)."""
    return tracker_db.format_tickets_by_assignee(assignee)


@mcp.resource("projects://all")
def resource_all_projects() -> str:
    """Project directory with ticket counts."""
    return tracker_db.format_all_projects()


@mcp.resource("project://{project_id}")
def resource_project_detail(project_id: str) -> str:
    """Project summary and per-status ticket counts."""
    return tracker_db.format_project_details(project_id)


@mcp.tool()
def create_ticket(
    title: str,
    description: str,
    priority: str,
    assignee: str,
    reporter: str,
    project: str,
    due_date: str = "",
    tags: str = "",
) -> str:
    """Create a ticket (mutates SQLite state; resources reflect changes on next read)."""
    return tracker_db.create_ticket_impl(
        title,
        description,
        priority,
        assignee,
        reporter,
        project,
        due_date,
        tags,
    )


@mcp.tool()
def update_ticket_status(
    ticket_id: str, new_status: str, updater: str = "System"
) -> str:
    """Update ticket workflow status."""
    return tracker_db.update_ticket_status_impl(ticket_id, new_status, updater)


if __name__ == "__main__":
    tracker_db.init_database()
    parser = argparse.ArgumentParser(
        description="Project Tracker MCP server (FastMCP)."
    )
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
