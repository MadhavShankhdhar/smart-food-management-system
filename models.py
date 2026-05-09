import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS food_data (
        id INTEGER PRIMARY KEY,
        date TEXT,
        meal_type TEXT,
        menu_items TEXT,
        cooked REAL,
        consumed REAL,
        waste REAL,
        waste_pct REAL,
        people_served INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS ngos (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        location TEXT
    )''')
    conn.commit()
    conn.close()

def add_food_data(meal_type, menu_items, cooked, consumed, waste, waste_pct, people_served):
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('INSERT INTO food_data (date, meal_type, menu_items, cooked, consumed, waste, waste_pct, people_served) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), meal_type, menu_items, cooked, consumed, waste, waste_pct, people_served))
    conn.commit()
    conn.close()

def get_food_data():
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('SELECT * FROM food_data ORDER BY date DESC')
    data = c.fetchall()
    conn.close()
    return data

def get_dashboard_stats():
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('SELECT SUM(cooked), SUM(consumed), SUM(waste), AVG(waste_pct) FROM food_data')
    stats = c.fetchone()
    conn.close()
    return {
        'total_cooked': stats[0] or 0,
        'total_consumed': stats[1] or 0,
        'total_waste': stats[2] or 0,
        'avg_waste_pct': stats[3] or 0
    }

def get_weekly_trends():
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    # Get last 7 days data
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    c.execute('SELECT date, waste_pct FROM food_data WHERE date >= ? ORDER BY date', (week_ago,))
    data = c.fetchall()
    conn.close()
    # Group by day
    trends = {}
    for row in data:
        day = row[0][:10]  # YYYY-MM-DD
        if day not in trends:
            trends[day] = []
        trends[day].append(row[1])
    # Average per day
    avg_trends = {day: sum(pcts)/len(pcts) for day, pcts in trends.items()}
    return avg_trends

def add_ngo(name, phone, location):
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('INSERT INTO ngos (name, phone, location) VALUES (?, ?, ?)', (name, phone, location))
    conn.commit()
    conn.close()

def get_ngos():
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ngos')
    ngos = c.fetchall()
    conn.close()
    return ngos

def get_recent_data(limit=5):
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    c.execute('SELECT * FROM food_data ORDER BY date DESC LIMIT ?', (limit,))
    data = c.fetchall()
    conn.close()
    return data