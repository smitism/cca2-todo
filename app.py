
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = os.environ.get(
    "TODO_DB",
    str(Path(__file__).parent / "todos.db")
)


@contextmanager
def get_db():
    """Open a database connection and always close it."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)


@app.get("/")
def index():
    init_db()

    with get_db() as conn:
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "index.html",
        tasks=tasks,
        total=len(tasks),
        done=sum(task["completed"] for task in tasks)
    )


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()

    if title:
        init_db()

        with get_db() as conn:
            conn.execute(
                "INSERT INTO tasks (title) VALUES (?)",
                (title,)
            )

    return redirect(url_for("index"))


@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    init_db()

    with get_db() as conn:
        conn.execute("""
            UPDATE tasks
            SET completed = CASE completed
                WHEN 1 THEN 0
                ELSE 1
            END
            WHERE id = ?
        """, (task_id,))

    return redirect(url_for("index"))


@app.post("/delete/<int:task_id>")
def delete(task_id):
    init_db()

    with get_db() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

    return redirect(url_for("index"))


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000"))
    )
