import sqlite3

conn = sqlite3.connect("GoalTracker.db")
pen = conn.cursor()


# ================ Database Functions ==================

def create_table(table_name):
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        title TEXT,
        description TEXT,
        progress INTEGER,
        max INTEGER,
        done INTEGER
    )
    """
    pen.execute(sql)
    conn.commit()

def table_exists(table_name):
    pen.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (table_name,))
    return pen.fetchone() is not None

def read_goals(goalname):
    pen.execute(f"SELECT * FROM {goalname}")
    return pen.fetchall()

def add_goal(goal_type="", title="", description="", progress=0, max=0, table="Goals", done=0):
    pen.execute(f"""
        INSERT INTO {table} (type, title, description, progress, max, done)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (goal_type, title, description, progress, max, done))
    conn.commit()

def modify_current(table, id, new_progress):
    pen.execute(f"""
        UPDATE {table}
        SET progress = ?
        WHERE id= ?
    """, (new_progress, id))
    conn.commit()

def modify_done(table, title, done_value):
    pen.execute(f"""
        UPDATE {table}
        SET done = ?
        WHERE title = ?
    """, (done_value, title))
    conn.commit()

def return_tables():
    pen.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = pen.fetchall()
    return tables

def delete_completed_tasks(table):
    pen.execute(f"""
        DELETE FROM {table}
        WHERE progress = max
    """)
    conn.commit()

def delete_table(table_name):
    pen.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
