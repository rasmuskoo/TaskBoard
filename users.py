import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_pending_tasks(user_id):
    sql = """SELECT id, title, priority, due_date
             FROM tasks
             WHERE user_id = ? AND status = 'pending'
             ORDER BY DATE(due_date) ASC, id DESC"""
    return db.query(sql, [user_id])

def get_completed_tasks(user_id):
    sql = """SELECT id, title, priority, due_date
             FROM tasks
             WHERE user_id = ? AND status = 'completed'
             ORDER BY DATE(due_date) DESC, id DESC"""
    return db.query(sql, [user_id])

def get_user_comments(user_id):
    sql = """SELECT p.id,
                    p.content,
                    p.created_at,
                    p.task_id,
                    t.title AS task_title
             FROM progress p
             JOIN tasks t ON t.id = p.task_id
             WHERE p.user_id = ?
             ORDER BY p.created_at DESC"""
    return db.query(sql, [user_id])
