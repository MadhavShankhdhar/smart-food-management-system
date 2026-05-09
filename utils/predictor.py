def predict_next_day():
    # Simple prediction: average waste percentage from last 7 days
    import sqlite3
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect('smart_food.db')
    c = conn.cursor()
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    c.execute('SELECT AVG(waste_pct) FROM food_data WHERE date >= ?', (week_ago,))
    avg = c.fetchone()[0]
    conn.close()
    return avg or 0