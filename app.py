from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime, timedelta
from models import init_db, add_food_data, get_food_data, get_dashboard_stats, get_weekly_trends, add_ngo, get_ngos, get_recent_data
from utils.waste import calculate_waste
from utils.predictor import predict_next_day
from utils.sms import send_ngo_alerts

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'smart_mess_secret_key_2024'

# Initialize database
init_db()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    stats = get_dashboard_stats()
    trends = get_weekly_trends()
    prediction = predict_next_day()
    recent_data = get_recent_data()
    return render_template('dashboard.html', 
                         stats=stats, 
                         trends=trends, 
                         prediction=prediction,
                         recent_data=recent_data)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        meal_type = request.form['meal_type']
        menu_items = request.form['menu_items']
        cooked = float(request.form['cooked'])
        consumed = float(request.form['consumed'])
        people_served = int(request.form['people_served'])
        
        waste, waste_pct = calculate_waste(cooked, consumed)
        
        # Add to database
        add_food_data(meal_type, menu_items, cooked, consumed, waste, waste_pct, people_served)
        
        # Check for NGO alert if waste percentage > 20%
        if waste_pct > 20:
            send_ngo_alerts(meal_type, waste, menu_items, people_served)
            flash('Data added and NGO alert sent!', 'success')
        else:
            flash('Data added successfully!', 'success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_data.html')

@app.route('/ngos')
def ngos():
    ngo_list = get_ngos()
    return render_template('ngos.html', ngos=ngo_list)

@app.route('/add_ngo', methods=['POST'])
def add_ngo_route():
    name = request.form['name']
    phone = request.form['phone']
    location = request.form['location']
    add_ngo(name, phone, location)
    flash('NGO added successfully!', 'success')
    return redirect(url_for('ngos'))

@app.route('/reports')
def reports():
    all_data = get_food_data()
    return render_template('reports.html', data=all_data)

@app.route('/api/trends')
def api_trends():
    trends = get_weekly_trends()
    return jsonify(trends)

if __name__ == '__main__':
    app.run(debug=True)