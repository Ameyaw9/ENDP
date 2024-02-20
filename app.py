from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os

app = Flask(__name__, template_folder='templates')


def create_user_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Create the User table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            activation_status INTEGER NOT NULL
        )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()
    

def create_deliver_receipt_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Create the Deliver Receipt table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deliver_receipt_scm_to_cp (
            OfferCode TEXT PRIMARY KEY,
            Msisdn TEXT NOT NULL,
            CorrelatorId TEXT NOT NULL,
            Status TEXT NOT NULL,
            LinkId TEXT NOT NULL,
            Refund TEXT NOT NULL
        )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()

# Create the User and Deliver Receipt tables if not exists
create_user_table()
create_deliver_receipt_table()

def create_activation_deactivation_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Create the Activation & Deactivation table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activation_deactivation (
            NextBillDate TEXT NOT NULL,
            BillingId TEXT NOT NULL,
            ChargeAmount TEXT NOT NULL,
            SubscriptionStatus TEXT NOT NULL,
            SubscriberLifeCycle TEXT NOT NULL,
            TransactionId TEXT NOT NULL,
            ClientTransactionID TEXT NOT NULL,
            Channel TEXT NOT NULL,
            Reason TEXT NOT NULL,
            Language TEXT NOT NULL,
            OfferCode TEXT NOT NULL,
            Msisdn TEXT NOT NULL,
            PRIMARY KEY (BillingId)
        )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()

def create_content_charge_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Create the Content Charge table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_charge (
            BillingId TEXT NOT NULL,
            ChargeAmount TEXT NOT NULL,
            SubscriptionStatus TEXT NOT NULL,
            SubscriberLifeCycle TEXT NOT NULL,
            TransactionId TEXT NOT NULL,
            ClientTransactionID TEXT NOT NULL,
            Channel TEXT NOT NULL,
            Reason TEXT DEFAULT NULL,
            Language TEXT NOT NULL,
            OfferCode TEXT NOT NULL,
            Msisdn TEXT NOT NULL,
            PRIMARY KEY (BillingId)
        )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()

# Create the User, Deliver Receipt, Activation & Deactivation, and Content Charge tables if not exists
create_user_table()
create_deliver_receipt_table()
create_activation_deactivation_table()
create_content_charge_table()



@app.route('/user', methods=['GET', 'POST'])
def handle_user():
    if request.method == 'GET':
        # Fetch all users from the User table
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()
        conn.close()
        return render_template('user_form.html', users=users)

    elif request.method == 'POST':
        try:
            data = request.form

            # Ensuring that all required fields are present
            if not all(key in data for key in ('name', 'phone_number', 'activation_status')):
                return jsonify({'error': 'Missing required fields'}), 400

            # Convert activation_status to 1 (True) or 0 (False)
            activation_status = 1 if data['activation_status'].lower() == 'yes' else 0

            # Insert a new user into the User table
            conn = sqlite3.connect('example.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user (name, phone_number, activation_status) VALUES (?, ?, ?)',
                           (data['name'], data['phone_number'], activation_status))
            conn.commit()
            conn.close()

            # Redirect to the user form with a success message
            return redirect('/user')

        except Exception as e:
            # Handle unexpected errors gracefully
            return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

@app.route('/deliver_receipt_data', methods=['GET'])
def deliver_receipt_data():
    # Fetch all data from the Deliver Receipt table
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM deliver_receipt_scm_to_cp')
    deliver_receipts = cursor.fetchall()
    conn.close()

    return render_template('deliver_receipt_data.html', deliver_receipts=deliver_receipts)

@app.route('/activation_deactivation_data', methods=['GET'])
def activation_deactivation_data():
    # Fetch all data from the Activation & Deactivation table
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activation_deactivation')
    activation_deactivation_data = cursor.fetchall()
    conn.close()

    return render_template('activation_deactivation_data.html', activation_deactivation_data=activation_deactivation_data)

@app.route('/content_charge_data', methods=['GET'])
def content_charge_data():
    # Fetch all data from the Content Charge table
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM content_charge')
    content_charge_data = cursor.fetchall()
    conn.close()

    return render_template('content_charge_data.html', content_charge_data=content_charge_data)


if __name__ == '__main__':
    app.run(debug=True)
