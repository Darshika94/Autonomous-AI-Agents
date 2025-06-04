import sqlite3

def init_db():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flagged_txns
                 (txn_id TEXT, user_id TEXT, reason TEXT)''')
    conn.commit()
    conn.close()

def log_flag(txn_id, user_id, reason):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("INSERT INTO flagged_txns VALUES (?, ?, ?)", (txn_id, user_id, reason))
    conn.commit()
    conn.close()
