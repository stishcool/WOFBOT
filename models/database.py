import sqlite3

class Database:
    def __init__(self, db_path='bot_database.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Таблица пользователей
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            full_name TEXT,
            tickets INTEGER DEFAULT 0,
            referral_link TEXT,
            referrer_id INTEGER,
            subscribed INTEGER DEFAULT 0
        )
        ''')
        # Таблица каналов
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name TEXT,
            channel_link TEXT
        )
        ''')
        # Таблица игр
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_text TEXT,
            probability REAL
        )
        ''')
        self.connection.commit()

    def get_games(self):
        self.cursor.execute("SELECT game_text, probability FROM games")
        rows = self.cursor.fetchall()
        games = [{'game_text': row[0], 'probability': row[1]} for row in rows]
        return games

    # Другие методы для работы с пользователями, каналами и играми
    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'user_id': row[1],
                'username': row[2],
                'full_name': row[3],
                'tickets': row[4],
                'referral_link': row[5],
                'referrer_id': row[6],
                'subscribed': row[7]
            }
        return None

    def add_user(self, user_id, username, full_name, referrer_id=None):
        self.cursor.execute("""
            INSERT INTO users (user_id, username, full_name, referrer_id)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, full_name, referrer_id))
        self.connection.commit()

    def add_ticket(self, user_id, amount=1):
        self.cursor.execute("""
            UPDATE users SET tickets = tickets + ? WHERE user_id = ?
        """, (amount, user_id))
        self.connection.commit()

    def update_subscription_status(self, user_id, status):
        self.cursor.execute("""
            UPDATE users SET subscribed = ? WHERE user_id = ?
        """, (status, user_id))
        self.connection.commit()

    def get_channels(self):
        self.cursor.execute("SELECT * FROM channels")
        return self.cursor.fetchall()

    # Методы для добавления и удаления каналов, игр и т.д.
