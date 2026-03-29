import sqlite3

def upgrade_schema():
    conn = sqlite3.connect(r'r:\Vehicle IQ\instance\vehicle.db')
    cursor = conn.cursor()
    
    # Add created_at to Prediction
    try:
        cursor.execute("ALTER TABLE prediction ADD COLUMN created_at DATETIME")
        print("Added created_at to prediction table.")
    except sqlite3.OperationalError as e:
        print("Prediction error:", e)

    # Add created_at to Vehicles
    try:
        cursor.execute("ALTER TABLE vehicles ADD COLUMN created_at DATETIME")
        print("Added created_at to vehicles table.")
    except sqlite3.OperationalError as e:
        print("Vehicles error:", e)

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == '__main__':
    upgrade_schema()
