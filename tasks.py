import db

def add_task(title, description, priority, due_date, user_id):
    sql = """INSERT INTO tasks (title, description, priority, due_date, user_id)
             VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, priority, due_date, user_id])

def get_tasks():
    sql = "SELECT id, title FROM tasks ORDER BY id DESC"
    return db.query(sql)

def get_task(task_id):
    sql = """SELECT tasks.id,
                    tasks.status,
                    tasks.title,
                    tasks.description,
                    tasks.priority,
                    tasks.due_date,
                    users.id user_id,
                    users.username
             FROM tasks, users
             WHERE tasks.user_id = users.id AND tasks.id = ?"""
    return db.query(sql, [task_id])[0]

def update_task(task_id, title, description, priority, due_date):
    sql = """UPDATE tasks SET title = ?,
                              description = ?,
                              priority = ?,
                              due_date = ?
                          WHERE id = ?"""
    db.execute(sql, [title, description, priority, due_date, task_id])

def remove_task(task_id):
    sql = "DELETE FROM tasks WHERE id = ?"
    db.execute(sql, [task_id])

def get_pending_tasks():
    sql = "SELECT id, title FROM tasks WHERE status = 'pending' ORDER BY id DESC"
    return db.query(sql)

def get_completed_tasks():
    sql = "SELECT id, title FROM tasks WHERE status = 'completed' ORDER BY id DESC"
    return db.query(sql)

def mark_task_completed(task_id):
    sql = "UPDATE tasks SET status = 'completed' WHERE id = ?"
    db.execute(sql, [task_id])

def mark_task_pending(task_id):
    sql = "UPDATE tasks SET status = 'pending' WHERE id = ?"
    db.execute(sql, [task_id])
