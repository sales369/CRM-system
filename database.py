import os
import hashlib
import pandas as pd
from datetime import date, timedelta, datetime
import psycopg2

class DatabaseManager:

    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set.")

    def _connect(self):
        return psycopg2.connect(self.database_url, sslmode="require")

    def _query_df(self, sql: str, params=None) -> pd.DataFrame:
        try:
            with self._connect() as conn:
                return pd.read_sql_query(sql, conn, params=params)
        except Exception as e:
            print(f"[DB] query error: {e}")
            return pd.DataFrame()

    # ══════════════════════════════════════════════════════════════════════════
    #  SCHEMA INIT
    # ══════════════════════════════════════════════════════════════════════════

    def init_user_tables(self):
        ddl = """
        CREATE TABLE IF NOT EXISTS users (
            id            SERIAL PRIMARY KEY,
            full_name     VARCHAR(255) NOT NULL,
            username      VARCHAR(100) UNIQUE NOT NULL,
            email         VARCHAR(255),
            password_hash VARCHAR(255) NOT NULL,
            role          VARCHAR(20)  DEFAULT 'user',
            is_active     BOOLEAN      DEFAULT TRUE,
            created_at    TIMESTAMP    DEFAULT NOW()
        );
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(ddl)
                conn.commit()
        except Exception as e:
            print(f"[DB] init_user_tables error: {e}")

    def init_tables(self):
        ddl = """
        CREATE TABLE IF NOT EXISTS clients (
            id               SERIAL PRIMARY KEY,
            name             VARCHAR(255) NOT NULL,
            email            VARCHAR(255),
            phone            VARCHAR(50),
            company          VARCHAR(255),
            category         VARCHAR(100)  DEFAULT 'Lead',
            source           VARCHAR(100)  DEFAULT 'Other',
            last_contacted   TIMESTAMP,
            followup_days    INTEGER       DEFAULT 7,
            next_followup    TIMESTAMP,
            deal_value       NUMERIC(12,2) DEFAULT 0,
            notes            TEXT,
            discussion       TEXT,
            created_by       INTEGER,
            created_at       TIMESTAMP     DEFAULT NOW(),
            updated_at       TIMESTAMP     DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_next_followup ON clients(next_followup);
        CREATE INDEX IF NOT EXISTS idx_category        ON clients(category);
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(ddl)
                    cur.execute("""
                        ALTER TABLE clients ADD COLUMN IF NOT EXISTS created_by INTEGER;
                        ALTER TABLE clients ADD COLUMN IF NOT EXISTS discussion TEXT;
                        ALTER TABLE clients ALTER COLUMN next_followup TYPE TIMESTAMP USING next_followup::timestamp;
                        ALTER TABLE clients ALTER COLUMN last_contacted TYPE TIMESTAMP USING last_contacted::timestamp;
                    """)
                conn.commit()
        except Exception as e:
            print(f"[DB] init_tables error: {e}")

    def ensure_default_admin(self):
        try:
            df = self._query_df("SELECT COUNT(*) AS cnt FROM users")
            if df.empty or int(df["cnt"].iloc[0]) == 0:
                default_hash = hashlib.sha256("admin123".encode()).hexdigest()
                self.add_user({
                    "full_name":     "System Admin",
                    "username":      "admin",
                    "email":         "admin@clientpulse.com",
                    "password_hash": default_hash,
                    "role":          "admin",
                })
                print("[DB] Default admin created — username: admin, password: admin123")
        except Exception as e:
            print(f"[DB] ensure_default_admin error: {e}")

    # ══════════════════════════════════════════════════════════════════════════
    #  USER MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════

    def authenticate_user(self, username: str, password_hash: str):
        df = self._query_df(
            "SELECT * FROM users WHERE username=%s AND password_hash=%s AND is_active=TRUE",
            (username, password_hash)
        )
        if df.empty:
            return None
        return df.iloc[0].to_dict()

    def add_user(self, data: dict) -> bool:
        sql = """
        INSERT INTO users (full_name, username, email, password_hash, role)
        VALUES (%(full_name)s, %(username)s, %(email)s, %(password_hash)s, %(role)s)
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, data)
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] add_user error: {e}")
            return False

    def get_all_users(self) -> pd.DataFrame:
        return self._query_df(
            "SELECT id, full_name, username, email, role, is_active, created_at "
            "FROM users ORDER BY created_at ASC"
        )

    def username_exists(self, username: str) -> bool:
        df = self._query_df(
            "SELECT id FROM users WHERE username=%s", (username,)
        )
        return not df.empty

    def toggle_user_status(self, user_id: int) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE users SET is_active = NOT is_active WHERE id=%s",
                        (user_id,)
                    )
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] toggle_user_status error: {e}")
            return False

    def delete_user(self, user_id: int) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] delete_user error: {e}")
            return False

    def update_user_password(self, user_id: int, new_hash: str) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE users SET password_hash=%s WHERE id=%s",
                        (new_hash, user_id)
                    )
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] update_user_password error: {e}")
            return False

    # ══════════════════════════════════════════════════════════════════════════
    #  CLIENT MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════════

    def add_client(self, data: dict) -> bool:
        sql = """
        INSERT INTO clients
            (name, email, phone, company, category, source,
             last_contacted, followup_days, next_followup,
             deal_value, notes, discussion, created_by)
        VALUES
            (%(name)s, %(email)s, %(phone)s, %(company)s, %(category)s, %(source)s,
             %(last_contacted)s, %(followup_days)s, %(next_followup)s,
             %(deal_value)s, %(notes)s, %(discussion)s, %(created_by)s)
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, data)
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] add_client error: {e}")
            return False

    def update_followup(self, client_id: int, new_date: str,
                        update_last_contacted: bool = False) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    if update_last_contacted:
                        cur.execute(
                            """UPDATE clients
                               SET next_followup=%s, last_contacted=%s, updated_at=NOW()
                             WHERE id=%s""",
                            (new_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), client_id)
                        )
                    else:
                        cur.execute(
                            """UPDATE clients
                               SET next_followup=%s, updated_at=NOW()
                             WHERE id=%s""",
                            (new_date, client_id)
                        )
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] update_followup error: {e}")
            return False

    def delete_client(self, client_id: int) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM clients WHERE id=%s", (client_id,))
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] delete_client error: {e}")
            return False

    def delete_multiple_clients(self, client_ids: list) -> bool:
        """Deletes multiple clients based on a list of IDs."""
        if not client_ids: return True
        # Create a string of placeholders: %s, %s, %s...
        placeholders = ', '.join(['%s'] * len(client_ids))
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"DELETE FROM clients WHERE id IN ({placeholders})", tuple(client_ids))
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] delete_multiple_clients error: {e}")
            return False

    def update_client_notes(self, client_id: int, notes: str) -> bool:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE clients SET notes=%s, updated_at=NOW() WHERE id=%s",
                        (notes, client_id)
                    )
                conn.commit()
            return True
        except Exception as e:
            print(f"[DB] update_client_notes error: {e}")
            return False

    # ══════════════════════════════════════════════════════════════════════════
    #  CLIENT QUERIES
    # ══════════════════════════════════════════════════════════════════════════

    def get_all_clients(self, search: str = None,
                        category: str = None,
                        sort_by: str = "Next Follow-up") -> pd.DataFrame:
        sort_map = {
            "Next Follow-up": "next_followup ASC NULLS LAST",
            "Name":           "name ASC",
            "Company":        "company ASC",
            "Deal Value":     "deal_value DESC NULLS LAST",
        }
        order = sort_map.get(sort_by, "next_followup ASC NULLS LAST")

        conditions, params = [], []
        if search:
            conditions.append(
                "(name ILIKE %s OR company ILIKE %s OR email ILIKE %s OR phone ILIKE %s)"
            )
            like = f"%{search}%"
            params.extend([like, like, like, like])
        if category:
            conditions.append("category = %s")
            params.append(category)

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        sql   = f"SELECT * FROM clients {where} ORDER BY {order}"
        return self._query_df(sql, params or None)

    def get_todays_followups(self) -> pd.DataFrame:
        return self._query_df(
            "SELECT * FROM clients WHERE DATE(next_followup) = %s ORDER BY name",
            (str(date.today()),)
        )

    def get_overdue_followups(self) -> pd.DataFrame:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self._query_df(
            "SELECT * FROM clients WHERE next_followup < %s ORDER BY next_followup ASC",
            (now_str,)
        )

    def get_upcoming_followups(self, days: int = 7) -> pd.DataFrame:
        end = date.today() + timedelta(days=days)
        return self._query_df(
            """SELECT * FROM clients
                WHERE DATE(next_followup) > %s
                  AND DATE(next_followup) <= %s
                ORDER BY next_followup ASC""",
            (str(date.today()), str(end))
        )

    def get_total_clients(self) -> int:
        df = self._query_df("SELECT COUNT(*) AS cnt FROM clients")
        return int(df["cnt"].iloc[0]) if not df.empty else 0

    def get_clients_by_category(self) -> pd.DataFrame:
        return self._query_df(
            "SELECT category, COUNT(*) AS count FROM clients GROUP BY category ORDER BY count DESC"
        )

    def get_clients_by_source(self) -> pd.DataFrame:
        return self._query_df(
            "SELECT source, COUNT(*) AS count FROM clients GROUP BY source ORDER BY count DESC"
        )

    def get_deal_value_by_category(self) -> pd.DataFrame:
        return self._query_df(
            "SELECT category, SUM(deal_value) AS total FROM clients GROUP BY category ORDER BY total DESC"
        )
