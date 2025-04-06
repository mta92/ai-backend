from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import extract_receipt_data
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    return conn

@app.route('/api/upload', methods=['POST'])
def upload_receipt():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    data = extract_receipt_data(file)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO receipts (merchant_name, total_amount, transaction_date, raw_text) VALUES (%s, %s, %s, %s)",
        (data["merchant"], data["total"], data["date"], data["raw_text"])
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run()