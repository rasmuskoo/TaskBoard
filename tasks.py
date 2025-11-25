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
    result =  db.query(sql, [task_id])
    return result[0] if result else None

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

def find_tasks(query):
    sql = """SELECT id, title
             FROM tasks
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_progress(task_id, user_id, content):
    sql = "INSERT INTO progress (task_id, user_id, content) VALUES (?,?,?)"
    db.execute(sql, (task_id, user_id, content))

def get_progress(task_id):
    sql = """SELECT p.id, p.task_id, p.user_id, p.content, p.created_at, u.username
             FROM progress p
             JOIN users u ON u.id = p.user_id
             WHERE p.task_id = ?
             ORDER BY p.created_at DESC"""
    return db.query(sql, (task_id,))

def get_one(progress_id):
    sql = "SELECT * FROM progress WHERE id = ?"
    rows = db.query(sql, (progress_id,))
    return rows[0] if rows else None

def update_progress(progress_id, content):
    sql = "UPDATE progress SET content = ? WHERE id = ?"
    db.execute(sql, (content, progress_id))

def delete_progress(progress_id):
    sql = "DELETE FROM progress WHERE id = ?"
    db.execute(sql, (progress_id,))