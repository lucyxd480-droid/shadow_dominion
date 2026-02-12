import sqlite3

conn = sqlite3.connect("shadow_v2.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    rating INTEGER DEFAULT 1000,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0
)
""")

conn.commit()


def ensure_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (user_id,))
    conn.commit()


def add_win(user_id, survive=False):
    ensure_user(user_id)
    bonus = 5 if survive else 0
    cursor.execute("""
        UPDATE users
        SET wins = wins + 1,
            rating = rating + ?
        WHERE user_id = ?
    """, (25 + bonus, user_id))
    conn.commit()


def add_loss(user_id):
    ensure_user(user_id)
    cursor.execute("""
        UPDATE users
        SET losses = losses + 1,
            rating = rating - 20
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()


def get_rating(user_id):
    ensure_user(user_id)
    cursor.execute("SELECT rating FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0]


def leaderboard(limit=10):
    cursor.execute("""
        SELECT user_id, rating, wins
        FROM users
        ORDER BY rating DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()
