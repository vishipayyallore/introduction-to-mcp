"""SQLite persistence and sync helpers for the leave manager demo."""

from __future__ import annotations

import difflib
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_FILE = Path(__file__).resolve().parent / "leave_manager.db"


@dataclass
class Employee:
    employee_id: str
    name: str
    department: str
    manager: str
    annual_leave_balance: int
    sick_leave_balance: int


@dataclass
class LeaveRequest:
    request_id: str
    employee_id: str
    employee_name: str
    start_date: str
    end_date: str
    leave_type: str
    status: str
    reason: str
    days_requested: int
    submitted_date: str
    approved_by: Optional[str] = None


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_FILE)


def init_database() -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            manager TEXT NOT NULL,
            annual_leave_balance INTEGER NOT NULL,
            sick_leave_balance INTEGER NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leave_requests (
            request_id TEXT PRIMARY KEY,
            employee_id TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            leave_type TEXT NOT NULL,
            status TEXT NOT NULL,
            reason TEXT NOT NULL,
            days_requested INTEGER NOT NULL,
            submitted_date TEXT NOT NULL,
            approved_by TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        )
        """
    )

    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        sample_employees = [
            ("EMP001", "John Smith", "Engineering", "Jane Doe", 25, 10),
            ("EMP002", "Alice Johnson", "Marketing", "Bob Wilson", 20, 10),
            ("EMP003", "Bob Wilson", "Marketing", "Jane Doe", 25, 10),
            ("EMP004", "Sarah Davis", "HR", "Jane Doe", 22, 11),
            ("EMP005", "Nick Chen", "Engineering", "John Smith", 18, 10),
        ]
        cursor.executemany(
            """
            INSERT INTO employees (
                employee_id, name, department, manager,
                annual_leave_balance, sick_leave_balance
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            sample_employees,
        )

        sample_requests = [
            (
                "REQ001",
                "EMP001",
                "John Smith",
                "2024-07-01",
                "2024-07-05",
                "annual",
                "approved",
                "Family vacation",
                5,
                "2024-06-15",
                "Jane Doe",
            ),
            (
                "REQ002",
                "EMP002",
                "Alice Johnson",
                "2024-07-10",
                "2024-07-12",
                "sick",
                "approved",
                "Doctor appointment",
                3,
                "2024-07-09",
                "Bob Wilson",
            ),
            (
                "REQ003",
                "EMP003",
                "Bob Wilson",
                "2024-08-01",
                "2024-08-03",
                "annual",
                "pending",
                "Trip vacation",
                3,
                "2024-07-20",
                None,
            ),
            (
                "REQ004",
                "EMP004",
                "Sarah Davis",
                "2024-07-15",
                "2024-07-16",
                "personal",
                "denied",
                "Personal matters",
                2,
                "2024-07-10",
                "Jane Doe",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO leave_requests (
                request_id, employee_id, employee_name, start_date, end_date,
                leave_type, status, reason, days_requested, submitted_date, approved_by
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_requests,
        )

    conn.commit()
    conn.close()


def load_employees() -> list[Employee]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return [Employee(*row) for row in rows]


def load_leave_requests() -> list[LeaveRequest]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leave_requests")
    rows = cursor.fetchall()
    conn.close()
    return [LeaveRequest(*row) for row in rows]


def get_employee_by_id(employee_id: str) -> Optional[Employee]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    row = cursor.fetchone()
    conn.close()
    return Employee(*row) if row else None


def find_similar_employees(name: str, threshold: float = 0.6) -> list[Employee]:
    employees = load_employees()
    similar: list[tuple[Employee, float]] = []
    for emp in employees:
        similarity = difflib.SequenceMatcher(None, name.lower(), emp.name.lower()).ratio()
        if similarity >= threshold:
            similar.append((emp, similarity))
    similar.sort(key=lambda x: x[1], reverse=True)
    return [emp for emp, _ in similar]


def get_employee_by_name(name: str) -> Optional[Employee]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE LOWER(name) = LOWER(?)", (name,))
    row = cursor.fetchone()
    conn.close()
    return Employee(*row) if row else None


def format_all_employees() -> str:
    employees = load_employees()
    result = "Employee Directory:\n\n"
    for emp in employees:
        result += f"ID: {emp.employee_id}\n"
        result += f"Name: {emp.name}\n"
        result += f"Department: {emp.department}\n"
        result += f"Manager: {emp.manager}\n"
        result += f"Annual Leave Balance: {emp.annual_leave_balance} days\n"
        result += f"Sick Leave Balance: {emp.sick_leave_balance} days\n"
        result += "_" * 40 + "\n"
    return result


def format_employee_info(employee_id: str) -> str:
    employee = get_employee_by_id(employee_id)
    if not employee:
        return f"Employee {employee_id} not found"
    return (
        f"Employee Information:\n"
        f"ID: {employee.employee_id}\n"
        f"Name: {employee.name}\n"
        f"Department: {employee.department}\n"
        f"Manager: {employee.manager}\n"
        f"Annual Leave Balance: {employee.annual_leave_balance} days\n"
        f"Sick Leave Balance: {employee.sick_leave_balance} days\n"
    )


def format_all_leave_requests() -> str:
    requests = load_leave_requests()
    result = "All Leave Requests:\n\n"
    for req in requests:
        result += f"Request ID: {req.request_id}\n"
        result += f"Employee: {req.employee_name} ({req.employee_id})\n"
        result += f"Dates: {req.start_date} to {req.end_date}\n"
        result += f"Type: {req.leave_type.title()}\n"
        result += f"Days: {req.days_requested}\n"
        result += f"Status: {req.status.title()}\n"
        result += f"Reason: {req.reason}\n"
        result += f"Submitted: {req.submitted_date}\n"
        if req.approved_by:
            result += f"Approved by: {req.approved_by}\n"
        result += "_" * 40 + "\n"
    return result


def format_employee_leave_requests(employee_id: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leave_requests WHERE employee_id = ?", (employee_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No leave requests found for employee {employee_id}"

    requests = [LeaveRequest(*row) for row in rows]
    result = f"Leave Requests for Employee {employee_id}:\n\n"
    for req in requests:
        result += f"Request ID: {req.request_id}\n"
        result += f"Dates: {req.start_date} to {req.end_date}\n"
        result += f"Type: {req.leave_type.title()}\n"
        result += f"Days: {req.days_requested}\n"
        result += f"Status: {req.status.title()}\n"
        result += f"Reason: {req.reason}\n"
        result += f"Submitted: {req.submitted_date}\n"
        if req.approved_by:
            result += f"Approved by: {req.approved_by}\n"
        result += "_" * 40 + "\n"
    return result


def format_requests_by_status(status: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM leave_requests WHERE LOWER(status) = LOWER(?)",
        (status,),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No {status} leave requests found"

    result = f"{status.title()} Leave Requests:\n\n"
    for row in rows:
        req = LeaveRequest(*row)
        result += f"Request ID: {req.request_id}\n"
        result += f"Employee: {req.employee_name} ({req.employee_id})\n"
        result += f"Dates: {req.start_date} to {req.end_date}\n"
        result += f"Type: {req.leave_type.title()}\n"
        result += f"Days: {req.days_requested}\n"
        result += f"Status: {req.status.title()}\n"
        result += f"Reason: {req.reason}\n"
        result += f"Submitted: {req.submitted_date}\n"
        if req.approved_by:
            result += f"Approved by: {req.approved_by}\n"
        result += "_" * 40 + "\n"
    return result


def submit_leave_request_impl(
    employee_id: str,
    start_date: str,
    end_date: str,
    leave_type: str,
    reason: str,
    days_requested: int,
) -> str:
    employee = get_employee_by_id(employee_id)
    if not employee:
        return f"Error: Employee {employee_id} not found"

    valid_types = ["annual", "sick", "personal", "emergency"]
    if leave_type.lower() not in valid_types:
        return f"Error: Invalid leave type. Must be one of: {', '.join(valid_types)}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT request_id FROM leave_requests
        WHERE request_id LIKE 'REQ%' ORDER BY request_id DESC LIMIT 1
        """
    )
    last_id = cursor.fetchone()
    if last_id:
        next_num = int(last_id[0][3:]) + 1
    else:
        next_num = 1
    request_id = f"REQ{next_num:03d}"

    cursor.execute(
        """
        INSERT INTO leave_requests (
            request_id, employee_id, employee_name, start_date, end_date,
            leave_type, status, reason, days_requested, submitted_date, approved_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            request_id,
            employee_id,
            employee.name,
            start_date,
            end_date,
            leave_type.lower(),
            "pending",
            reason,
            days_requested,
            datetime.now().strftime("%Y-%m-%d"),
            None,
        ),
    )

    conn.commit()
    conn.close()

    return f"Leave request ({request_id}) submitted successfully for {employee.name}"


def approve_leave_request_impl(request_id: str, approver_name: str) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leave_requests WHERE request_id = ?", (request_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return f"Error: Leave request {request_id} not found"

    request = LeaveRequest(*row)

    if request.status != "pending":
        conn.close()
        return f"Error: Leave request {request_id} is already {request.status}"

    cursor.execute(
        """
        UPDATE leave_requests
        SET status = 'approved', approved_by = ?
        WHERE request_id = ?
        """,
        (approver_name, request_id),
    )

    if request.leave_type == "annual":
        cursor.execute(
            """
            UPDATE employees
            SET annual_leave_balance = MAX(0, annual_leave_balance - ?)
            WHERE employee_id = ?
            """,
            (request.days_requested, request.employee_id),
        )
    elif request.leave_type == "sick":
        cursor.execute(
            """
            UPDATE employees
            SET sick_leave_balance = MAX(0, sick_leave_balance - ?)
            WHERE employee_id = ?
            """,
            (request.days_requested, request.employee_id),
        )

    conn.commit()
    conn.close()

    return f"Leave request {request_id} approved by {approver_name}"


def check_leave_balance_impl(employee_id: str) -> str:
    employee = get_employee_by_id(employee_id)
    if not employee:
        return f"Error: Employee {employee_id} not found"

    return (
        f"Leave Balance for {employee.name} ({employee_id}):\n"
        f"Annual Leave: {employee.annual_leave_balance} days remaining\n"
        f"Sick Leave: {employee.sick_leave_balance} days remaining"
    )


def get_pending_approvals_impl() -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leave_requests WHERE status = 'pending'")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return "No pending leave requests requiring approval"

    result = f"Pending Leave Requests ({len(rows)}):\n\n"
    for row in rows:
        req = LeaveRequest(*row)
        result += f"Request ID: {req.request_id}\n"
        result += f"Employee: {req.employee_name} ({req.employee_id})\n"
        result += f"Dates: {req.start_date} to {req.end_date}\n"
        result += f"Type: {req.leave_type.title()}\n"
        result += f"Days: {req.days_requested}\n"
        result += f"Reason: {req.reason}\n"
        result += f"Submitted: {req.submitted_date}\n"
        result += "_" * 40 + "\n"
    return result


def get_database_stats_impl() -> str:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leave_requests")
    total_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leave_requests WHERE status = 'pending'")
    pending_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leave_requests WHERE status = 'approved'")
    approved_requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leave_requests WHERE status = 'denied'")
    denied_requests = cursor.fetchone()[0]

    conn.close()

    return (
        f"Database Statistics:\n"
        f"Employees: {employee_count}\n"
        f"Total Leave Requests: {total_requests}\n"
        f"Pending Requests: {pending_requests}\n"
        f"Approved Requests: {approved_requests}\n"
        f"Denied Requests: {denied_requests}\n"
    )


def add_employee_impl(
    name: str,
    department: str,
    manager: str,
    annual_leave_balance: int = 25,
    sick_leave_balance: int = 10,
    force_create: bool = False,
) -> str:
    existing_employee = get_employee_by_name(name)
    if existing_employee and not force_create:
        return (
            f"Employee with exact name '{name}' already exists:\n"
            f"ID: {existing_employee.employee_id}\n"
            f"Department: {existing_employee.department}\n"
            f"Manager: {existing_employee.manager}\n"
            "If you want to create a new employee anyway, call this function again "
            "with force_create=True"
        )

    if not force_create:
        similar_employees = find_similar_employees(name, threshold=0.7)
        if similar_employees:
            result = f"Found employees with similar names to '{name}':\n"
            for emp in similar_employees[:3]:
                result += f"ID: {emp.employee_id} | Name: {emp.name} | Dept: {emp.department}\n"
            result += "\nDo you want to:\n"
            result += "#1. Use an existing employee above, or\n"
            result += "#2. Create new employee anyway by calling add_employee with "
            result += "force_create=True\n"
            result += "#3. Cancel and choose a different name"
            return result

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT employee_id FROM employees
        WHERE employee_id LIKE 'EMP%' ORDER BY employee_id DESC LIMIT 1
        """
    )
    last_id = cursor.fetchone()
    if last_id:
        next_num = int(last_id[0][3:]) + 1
    else:
        next_num = 1
    employee_id = f"EMP{next_num:03d}"

    try:
        cursor.execute(
            """
            INSERT INTO employees (
                employee_id, name, department, manager,
                annual_leave_balance, sick_leave_balance
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                employee_id,
                name,
                department,
                manager,
                annual_leave_balance,
                sick_leave_balance,
            ),
        )
        conn.commit()
        conn.close()
        return (
            f"New employee created successfully:\n"
            f"ID: {employee_id}\n"
            f"Name: {name}\n"
            f"Department: {department}\n"
            f"Manager: {manager}\n"
            f"Annual Leave Balance: {annual_leave_balance} days\n"
            f"Sick Leave Balance: {sick_leave_balance} days"
        )
    except Exception as e:
        conn.close()
        return f"Error creating employee: {e!s}"
