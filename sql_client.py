import sqlite3
def setup_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
             (thread_id text, role text, content text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS full_chat_history
                (thread_id text, content text)''')
    conn.commit()
    conn.close()

def add_history(thread_id, role, text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_history VALUES (?, ?, ?)", (thread_id, role, text))
    conn.commit()
    conn.close()

def add_full_history(thread_id, text):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO full_chat_history VALUES (?, ?)", (thread_id, text))
    conn.commit()
    conn.close()