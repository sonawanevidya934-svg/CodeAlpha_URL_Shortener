from flask import Flask, request, redirect, jsonify
import sqlite3
import string
import random

app = Flask(__name__)

DATABASE = "urls.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/")
def home():
    return """
    <h1>Simple URL Shortener</h1>
    <p>Backend API is running successfully!</p>
    """


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]

    short_code = generate_short_code()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "original_url": original_url,
        "short_url": f"http://127.0.0.1:5000/{short_code}"
    })


@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])

    return jsonify({"error": "Short URL not found"}), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
