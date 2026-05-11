import sqlite3
import pandas as pd
import hashlib
from datetime import datetime, date

class DatabaseManager:
    def __init__(self, db_name="clientpulse.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def init_tables(self):
        # Using DATETIME ensures hours and minutes are safely stored
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                company TEXT,
                category TEXT,
                source TEXT,
                last_contacted DATETIME,
                followup_days INTEGER,
                next_followup DATETIME,
                deal_value REAL,
                notes TEXT,
                discussion TEXT,
                created_by INTEGER
            )
        ''')
        self.conn.commit()

    def init_user_tables(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        self.conn.commit()

    def ensure_default_admin(self):
        self.c.execute("SELECT COUNT(*) FROM users")
        if self.c.fetchone()[0] == 0:
            default_hash = hashlib.sha256("admin123".encode()).hexdigest()
            self.c.execute('''
                INSERT INTO users (full_name, username, password_hash, role, is_active)
                VALUES (?, ?, ?, ?, ?)
            ''', ("System Admin", "admin", default_hash, "admin", 1))
            self.conn.commit()

    def authenticate_user(self, username, password_hash):
        self.c.execute("SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1", 
                       (username, password_hash))
        row = self.c.fetchone()
        return dict(row) if row else None

    # --- Client Methods ---
    def get_total_clients(self):
        self.c.execute("SELECT COUNT(*) FROM clients")
        return self.c.fetchone()[0]

    def get_todays_followups(self):
        today_str = date.today().strftime("%Y-%m-%d")
        query = "SELECT * FROM clients WHERE date(next_followup) = ?"
        return pd.read_sql_query(query, self.conn, params=(today_str,))

    def get_overdue_followups(self):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "SELECT * FROM clients WHERE next_followup < ?"
        return pd.read_sql_query(query, self.conn, params=(now_str,))

    def get_all_clients(self, search=None, category=None, sort_by="Next Follow-up"):
        query = "SELECT * FROM clients WHERE 1=1"
        params = []

        if search:
            query += " AND (name LIKE ? OR company LIKE ? OR email LIKE ?)"
            s = f"%{search}%"
            params.extend([s, s, s])
        
        if category:
            query += " AND category = ?"
            params.append(category)

        if sort_by == "Next Follow-up":
            query += " ORDER BY next_followup ASC"
        elif sort_by == "Name":
            query += " ORDER BY name ASC"
        elif sort_by == "Company":
            query += " ORDER BY company ASC"
        elif sort_by == "Deal Value":
            query += " ORDER BY deal_value DESC"

        return pd.read_sql_query(query, self.conn, params=params)

    def add_client(self, data):
        try:
            cols = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            sql = f"INSERT INTO clients ({cols}) VALUES ({placeholders})"
            self.c.execute(sql, tuple(data.values()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding client: {e}")
            return False

    def update_followup(self, cid, new_dt_str):
        self.c.execute("UPDATE clients SET next_followup = ? WHERE id = ?", (new_dt_str, cid))
        self.conn.commit()

    def delete_client(self, cid):
        self.c.execute("DELETE FROM clients WHERE id = ?", (cid,))
        self.conn.commit()

    # --- User Methods ---
    def get_all_users(self):
        return pd.read_sql_query("SELECT * FROM users", self.conn)

    def add_user(self, data):
        cols = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO users ({cols}) VALUES ({placeholders})"
        self.c.execute(sql, tuple(data.values()))
        self.conn.commit()

    def username_exists(self, username):
        self.c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return self.c.fetchone() is not None

    def toggle_user_status(self, uid):
        self.c.execute("UPDATE users SET is_active = NOT is_active WHERE id = ?", (uid,))
        self.conn.commit()

    def delete_user(self, uid):
        self.c.execute("DELETE FROM users WHERE id = ?", (uid,))
        self.conn.commit()s
