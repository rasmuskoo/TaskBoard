import db

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_tasks(user_id):
    sql = "SELECT id, title FROM tasks WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def get_pending_tasks(user_id):
    sql = "SELECT id, title FROM tasks WHERE user_id = ? AND status = 'pending' ORDER BY id DESC"
    return db.query(sql, [user_id])

def get_completed_tasks(user_id):
    sql = "SELECT id, title FROM tasks WHERE user_id = ? AND status = 'completed' ORDER BY id DESC"
    return db.query(sql, [user_id])