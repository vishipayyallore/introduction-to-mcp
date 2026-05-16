"""SQLite persistence for the project tracker demo."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_FILE = Path(__file__).resolve().parent / "project_tracker.db"


@dataclass
class Ticket:
    ticket_id: str
    title: str
    description: str
    status: str
    priority: str
    assignee: str
    reporter: str
    created_date: str
    updated_date: str
    due_date: Optional[str]
    project: str
    tag: str


@dataclass
class Project:
    project_id: str
    name: str
    description: str
    status: str
    created_date: str


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def ticket_from_row(row: tuple) -> Ticket:
    """Normalize SQLite NULL tag column for the dataclass."""
    values = list(row)
    if len(values) >= 12 and values[11] is None:
        values[11] = ""
    return Ticket(*values)


def init_database() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            created_date TEXT NOT NULL
        )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            assignee TEXT NOT NULL,
            reporter TEXT NOT NULL,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL,
            due_date TEXT,
            project TEXT NOT NULL,
            tag TEXT
        )
        """)

    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        sample_projects = [
            (
                "PROJ001",
                "Website Redesign",
                "Complete redesign of company website",
                "active",
                "2024-01-15",
            ),
            (
                "PROJ002",
                "Mobile App",
                "Develop mobile application for iOS and Android",
                "active",
                "2024-02-01",
            ),
            (
                "PROJ003",
                "API Integration",
                "Integrate third-party APIs for data synchronization",
                "completed",
                "2024-01-10",
            ),
            (
                "PROJ004",
                "Security Audit",
                "Comprehensive security audit and improvements",
                "on_hold",
                "2024-03-01",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO projects (project_id, name, description, status, created_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            sample_projects,
        )

        sample_tickets = [
            (
                "TK001",
                "Fix login bug",
                "Users cannot login with special characters in password",
                "pending",
                "high",
                "Alice Johnson",
                "Bob Wilson",
                "2024-02-10",
                "2024-02-10",
                None,
                "Website Redesign",
                "",
            ),
            (
                "TK002",
                "Add dark mode",
                "Implement dark mode toggle for better user experience",
                "in_progress",
                "medium",
                "John Smith",
                "Mike Chen",
                "2024-02-12",
                "2024-02-15",
                "2024-03-01",
                "Mobile App",
                "",
            ),
            (
                "TK003",
                "Database optimization",
                "Optimize database queries for better performance",
                "completed",
                "low",
                "Nick Chen",
                "Sarah Davis",
                "2024-01-20",
                "2024-01-25",
                None,
                "API Integration",
                "",
            ),
            (
                "TK004",
                "Mobile app testing",
                "Comprehensive testing on different devices",
                "pending",
                "critical",
                "Sarah Davis",
                "Mike Chen",
                "2024-02-20",
                "2024-02-20",
                None,
                "Mobile App",
                "",
            ),
            (
                "TK005",
                "Update API documentation",
                "Update API documentation with new endpoints",
                "in_progress",
                "low",
                "Bob Wilson",
                "Sarah Davis",
                "2024-01-15",
                "2024-01-18",
                None,
                "API Integration",
                "",
            ),
            (
                "TK006",
                "Security vulnerability fix",
                "Fix SQL injection vulnerability in search",
                "closed",
                "critical",
                "Alice Johnson",
                "John Smith",
                "2024-03-05",
                "2024-03-10",
                None,
                "Security Audit",
                "",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO tickets (
                ticket_id, title, description, status, priority, assignee, reporter,
                created_date, updated_date, due_date, project, tag
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_tickets,
        )

    conn.commit()
    conn.close()


def load_tickets() -> list[Ticket]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY created_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [ticket_from_row(row) for row in rows]


def load_projects() -> list[Project]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [Project(*row) for row in rows]


def get_ticket_by_id(ticket_id: str) -> Optional[Ticket]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    return ticket_from_row(row) if row else None


def get_project_by_name(project_name: str) -> Optional[Project]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE name = ?", (project_name,))
    row = cursor.fetchone()
    conn.close()
    return Project(*row) if row else None


def get_project_by_id(project_id: str) -> Optional[Project]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()
    return Project(*row) if row else None


def format_all_tickets() -> str:
    tickets = load_tickets()
    result = f"All Tickets ({len(tickets)}):\n\n"
    for ticket in tickets:
        result += f"{ticket.ticket_id}: {ticket.title}\n"
        result += f"  Status: {ticket.status.replace('_', ' ').title()}\n"
        result += f"  Priority: {ticket.priority.title()}\n"
        result += f"  Assignee: {ticket.assignee}\n"
        result += f"  Project: {ticket.project}\n"
        result += f"  Created: {ticket.created_date}\n"
        if ticket.due_date:
            result += f"  Due: {ticket.due_date}\n"
        result += "-" * 50 + "\n"
    return result


def format_ticket_details(ticket_id: str) -> str:
    ticket = get_ticket_by_id(ticket_id)
    if not ticket:
        return f"Ticket {ticket_id} not found"

    result = f"== Ticket Details: {ticket.ticket_id} ==\n\n"
    result += f"Title: {ticket.title}\n"
    result += f"Description: {ticket.description}\n"
    result += f"Status: {ticket.status.replace('_', ' ').title()}\n"
    result += f"Priority: {ticket.priority.title()}\n"
    result += f"Assignee: {ticket.assignee}\n"
    result += f"Reporter: {ticket.reporter}\n"
    result += f"Project: {ticket.project}\n"
    result += f"Created: {ticket.created_date}\n"
    result += f"Updated: {ticket.updated_date}\n"
    if ticket.due_date:
        result += f"Due Date: {ticket.due_date}\n"
    if ticket.tag:
        result += f"Tags: {ticket.tag}\n"
    return result


def format_tickets_by_project_name(project_name: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tickets WHERE project = ? ORDER BY created_date DESC",
        (project_name,),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No tickets found for project: {project_name}"

    result = f"Tickets for Project '{project_name}' ({len(rows)}):\n\n"
    for row in rows:
        ticket = ticket_from_row(row)
        result += f"{ticket.ticket_id}: {ticket.title}\n"
        result += f"  Status: {ticket.status.replace('_', ' ').title()}\n"
        result += f"  Priority: {ticket.priority.title()}\n"
        result += f"  Assignee: {ticket.assignee}\n"
        if ticket.due_date:
            result += f"  Due: {ticket.due_date}\n"
        result += "-" * 40 + "\n"
    return result


def format_tickets_for_project_id(project_id: str) -> str:
    """Stable resource URI uses PROJ00x ids (avoids spaces in project titles)."""
    project = get_project_by_id(project_id)
    if not project:
        return f"Unknown project_id: {project_id}"
    return format_tickets_by_project_name(project.name)


def format_tickets_by_status(status: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tickets WHERE LOWER(status) = LOWER(?) ORDER BY created_date DESC",
        (status,),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No tickets found with status: {status}"

    label = status.replace("_", " ").title()
    result = f"Tickets with Status '{label}' ({len(rows)}):\n\n"
    for row in rows:
        ticket = ticket_from_row(row)
        result += f"{ticket.ticket_id}: {ticket.title}\n"
        result += f"  Priority: {ticket.priority.title()}\n"
        result += f"  Assignee: {ticket.assignee}\n"
        result += f"  Project: {ticket.project}\n"
        if ticket.due_date:
            result += f"  Due: {ticket.due_date}\n"
        result += "-" * 40 + "\n"
    return result


def format_tickets_by_assignee(assignee: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tickets WHERE LOWER(assignee) = LOWER(?) ORDER BY created_date DESC",
        (assignee,),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No tickets found assigned to: {assignee}"

    result = f"Tickets assigned to '{assignee}' ({len(rows)}):\n\n"
    for row in rows:
        ticket = ticket_from_row(row)
        result += f"{ticket.ticket_id}: {ticket.title}\n"
        result += f"  Status: {ticket.status.replace('_', ' ').title()}\n"
        result += f"  Priority: {ticket.priority.title()}\n"
        result += f"  Project: {ticket.project}\n"
        if ticket.due_date:
            result += f"  Due: {ticket.due_date}\n"
        result += "-" * 40 + "\n"
    return result


def format_all_projects() -> str:
    projects = load_projects()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT project, COUNT(*) FROM tickets GROUP BY project")
    ticket_counts = {project_name: count for project_name, count in cursor.fetchall()}
    conn.close()

    result = f"All Projects ({len(projects)}):\n\n"
    for project in projects:
        ticket_count = ticket_counts.get(project.name, 0)

        result += f"{project.project_id}: {project.name}\n"
        result += f"  Description: {project.description}\n"
        result += f"  Status: {project.status.replace('_', ' ').title()}\n"
        result += f"  Tickets: {ticket_count}\n"
        result += f"  Created: {project.created_date}\n"
        result += "-" * 50 + "\n"
    return result


def format_project_details(project_id: str) -> str:
    project = get_project_by_id(project_id)
    if not project:
        return f"Project id '{project_id}' not found"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE project = ?", (project.name,))
    total_tickets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tickets WHERE project = ? AND status = 'pending'",
        (project.name,),
    )
    pending_tickets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tickets WHERE project = ? AND status = 'in_progress'",
        (project.name,),
    )
    in_progress_tickets = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tickets WHERE project = ? AND status = 'completed'",
        (project.name,),
    )
    completed_tickets = cursor.fetchone()[0]

    conn.close()

    result = f"== Project Details: {project.name} ==\n\n"
    result += f"ID: {project.project_id}\n"
    result += f"Description: {project.description}\n"
    result += f"Status: {project.status.replace('_', ' ').title()}\n"
    result += f"Created: {project.created_date}\n"
    result += f"Total Tickets: {total_tickets}\n"
    result += f"Pending: {pending_tickets}\n"
    result += f"In Progress: {in_progress_tickets}\n"
    result += f"Completed: {completed_tickets}\n"
    return result


def create_ticket_impl(
    title: str,
    description: str,
    priority: str,
    assignee: str,
    reporter: str,
    project: str,
    due_date: str = "",
    tags: str = "",
) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ticket_id FROM tickets WHERE ticket_id LIKE 'TK%' ORDER BY ticket_id DESC LIMIT 1"
    )
    last_id = cursor.fetchone()
    if last_id:
        next_num = int(last_id[0][2:]) + 1
    else:
        next_num = 1
    ticket_id = f"TK{next_num:03d}"

    current_date = datetime.now().strftime("%Y-%m-%d")
    due_val: Optional[str] = due_date if due_date.strip() else None

    cursor.execute(
        """
        INSERT INTO tickets (
            ticket_id, title, description, status, priority, assignee, reporter,
            created_date, updated_date, due_date, project, tag
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            title,
            description,
            "pending",
            priority.lower(),
            assignee,
            reporter,
            current_date,
            current_date,
            due_val,
            project,
            tags,
        ),
    )

    conn.commit()
    conn.close()
    return f"Successfully created ticket {ticket_id}: {title}"


def update_ticket_status_impl(
    ticket_id: str, new_status: str, updater: str = "System"
) -> str:
    valid_statuses = ["pending", "in_progress", "completed", "closed"]
    if new_status.lower() not in valid_statuses:
        return f"Error: Status must be one of: {', '.join(valid_statuses)}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    if not cursor.fetchone():
        conn.close()
        return f"Error: Ticket {ticket_id} not found"

    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        """
        UPDATE tickets
        SET status = ?, updated_date = ?
        WHERE ticket_id = ?
        """,
        (new_status.lower(), current_date, ticket_id),
    )

    conn.commit()
    conn.close()

    label = new_status.replace("_", " ").title()
    return f"Successfully updated ticket {ticket_id} status to: {label} (by {updater})"
