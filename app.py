from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as s

app = Flask(__name__)
DATABASE = 'carSales.db'

def connection():
    try:
        conn = s.connect(DATABASE)
        conn.row_factory = s.Row
        return conn
    except s.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL
            )
        ''')
    except s.Error as e:
        print(f"Error creating table: {e}")

@app.route('/')
def index():
    conn = connection()
    if conn is None:
        return "Error connecting to database"
    create_table(conn)
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        year = request.form['year']
        price = request.form['price']
        
        conn = connection()
        if conn is None:
            return "Error connecting to database"
        create_table(conn)
        conn.execute('INSERT INTO items (id, name, year, price) VALUES (?, ?, ?, ?)', (id, name, year, price))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('create.html')

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    conn = connection()
    if conn is None:
        return "Error connecting to database"
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        price = request.form['price']
        
        conn.execute('UPDATE items SET name = ?, year = ?, price = ? WHERE id = ?', (name, year, price, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = connection()
    if conn is None:
        return "Error connecting to database"
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)