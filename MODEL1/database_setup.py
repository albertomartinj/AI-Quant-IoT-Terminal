import sqlite3
import os
from datetime import datetime

# -----------------------------------------------------------------------------
# Database Configuration
# -----------------------------------------------------------------------------

# Define the absolute or relative path where the database will be stored.
# To match the Express server configuration (path.join(__dirname, '../quant_data.db')),
# the database must be placed in the project root folder.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'quant_data.db')

def initialize_database():
    """
    Creates the SQLite database file and the 'portfolio_metrics' table 
    if it doesn't exist. The schema exactly matches the Node.js API expectations.
    """
    # Connect to the SQLite database (this creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the table with strict column names matching the frontend contract
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            asset_symbol TEXT NOT NULL,
            current_price REAL NOT NULL,
            entry_price REAL NOT NULL,
            stop_loss_threshold REAL NOT NULL,
            sentiment_label TEXT NOT NULL,
            action_signal TEXT NOT NULL,
            alert_severity TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"[Database] Successfully initialized table at {DB_PATH}")

def insert_mock_alert():
    """
    Inserts a simulated critical alert row (e.g., AAPL dropping significantly 
    with PANIC sentiment) to test the Node.js Dashboard API.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Generate current UTC timestamp in ISO 8601 format
    current_time = datetime.utcnow().isoformat() + "Z"

    # Define a mock critical scenario for Apple stock
    mock_data = (
        current_time,                # timestamp
        'AAPL',                      # asset_symbol
        135.50,                      # current_price (Dropped significantly)
        150.00,                      # entry_price
        5.0,                         # stop_loss_threshold (5%)
        'PANIC',                     # sentiment_label
        'SELL / TRIGGER IOT ALERT',  # action_signal
        'CRITICAL'                   # alert_severity
    )

    # Insert the mock row into the table
    cursor.execute('''
        INSERT INTO portfolio_metrics (
            timestamp, asset_symbol, current_price, entry_price, 
            stop_loss_threshold, sentiment_label, action_signal, alert_severity
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', mock_data)

    conn.commit()
    conn.close()
    print(f"[Database] Mock data for {mock_data[1]} inserted successfully.")

if __name__ == "__main__":
    # Execute the initialization and insert a test row
    initialize_database()
    insert_mock_alert()
