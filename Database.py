import sqlite3

def connect_db():
    return sqlite3.connect("blood_bank.db", check_same_thread=False)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        blood_group TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blood (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_group TEXT,
        collection_date TEXT,
        expiry_date TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_donor(name, age, blood_group, phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO donors (name, age, blood_group, phone)
    VALUES (?, ?, ?, ?)
    """, (name, age, blood_group, phone))

    conn.commit()
    conn.close()

def add_blood(bg, collection_date, expiry_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO blood (blood_group, collection_date, expiry_date, status)
    VALUES (?, ?, ?, 'Available')
    """, (bg, collection_date, expiry_date))

    conn.commit()
    conn.close()

def get_inventory():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT blood_group, COUNT(*) 
    FROM blood 
    WHERE status='Available'
    GROUP BY blood_group
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def issue_blood(bg):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id FROM blood 
    WHERE blood_group=? AND status='Available'
    LIMIT 1
    """, (bg,))

    result = cursor.fetchone()

    if result:
        cursor.execute("""
        UPDATE blood SET status='Used' WHERE id=?
        """, (result[0],))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False
