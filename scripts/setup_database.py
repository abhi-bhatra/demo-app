import sqlite3

def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create a 'users' table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Insert some test data
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('testuser', 'hashedpassword123'))
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()
