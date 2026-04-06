from flask import Flask, request, jsonify, render_template_string, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
data = []

REQUEST_COUNT = Counter("app_requests_total", "Total app requests")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini Logistics Tracker</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #dbeafe, #eff6ff, #e0f2fe);
            color: #1f2937;
        }

        .container {
            max-width: 1050px;
            margin: 40px auto;
            padding: 20px;
        }

        .hero {
            background: linear-gradient(135deg, #1d4ed8, #2563eb, #38bdf8);
            color: white;
            border-radius: 28px;
            padding: 40px 30px;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.12);
            text-align: center;
            margin-bottom: 24px;
        }

        .hero-icon {
            font-size: 54px;
            margin-bottom: 10px;
        }

        .hero h1 {
            margin: 0 0 10px 0;
            font-size: 42px;
        }

        .hero p {
            margin: 0;
            font-size: 18px;
            opacity: 0.96;
        }

        .section {
            background: white;
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
            margin-bottom: 24px;
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 0;
            margin-bottom: 18px;
            font-size: 28px;
            color: #0f172a;
        }

        .section-icon {
            font-size: 28px;
        }

        .input-row {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
            margin-top: 18px;
        }

        .item-input {
            flex: 1;
            min-width: 260px;
            padding: 18px 20px;
            font-size: 18px;
            border: 2px solid #cbd5e1;
            border-radius: 16px;
            outline: none;
            background: #f8fafc;
        }

        .item-input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
            background: white;
        }

        .btn {
            border: none;
            border-radius: 16px;
            padding: 16px 22px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.12s ease, opacity 0.12s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn:hover {
            transform: translateY(-1px);
            opacity: 0.96;
        }

        .btn-add {
            background: #2563eb;
            color: white;
            min-width: 150px;
        }

        .btn-remove {
            background: #dc2626;
            color: white;
            padding: 12px 18px;
            font-size: 16px;
        }

        .item-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin-top: 22px;
        }

        .item-card {
            background: linear-gradient(180deg, #f8fafc, #eff6ff);
            border: 1px solid #dbeafe;
            border-radius: 20px;
            padding: 18px;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08);
        }

        .item-top {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }

        .item-emoji {
            font-size: 24px;
        }

        .item-name {
            font-size: 19px;
            font-weight: bold;
            color: #0f172a;
            word-wrap: break-word;
        }

        .item-qty {
            display: inline-block;
            margin-top: 6px;
            margin-bottom: 14px;
            background: #dbeafe;
            color: #1d4ed8;
            padding: 8px 12px;
            border-radius: 999px;
            font-weight: bold;
            font-size: 14px;
        }

        .empty-state {
            margin-top: 20px;
            padding: 28px;
            text-align: center;
            background: #f8fafc;
            border-radius: 18px;
            color: #64748b;
            font-size: 17px;
            border: 1px dashed #cbd5e1;
        }

        .about-box, .contact-box {
            background: #f8fafc;
            border-radius: 18px;
            padding: 18px 20px;
            margin-top: 14px;
            border: 1px solid #e2e8f0;
        }

        .contact-box p,
        .about-box p {
            margin: 10px 0;
            font-size: 17px;
            line-height: 1.6;
        }

        .label {
            font-weight: bold;
            color: #0f172a;
        }

        .contact-line {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .contact-icon {
            font-size: 18px;
            width: 24px;
            text-align: center;
        }

        a {
            color: #2563eb;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .footer-note {
            text-align: center;
            color: #64748b;
            margin-top: 12px;
            font-size: 15px;
        }

        @media (max-width: 640px) {
            .hero h1 {
                font-size: 32px;
            }

            .btn,
            .item-input {
                width: 100%;
            }

            .input-row {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="hero-icon">📦</div>
            <h1>Mini Logistics Tracker</h1>
            <p>A simple item tracking system for logistics entries and monitoring.</p>
        </div>

        <div class="section">
            <h2 class="section-title"><span class="section-icon">➕</span> Add Item</h2>
            <div class="input-row">
                <input id="itemInput" class="item-input" type="text" placeholder="Enter item name">
                <button class="btn btn-add" onclick="addItem()">➕ Add Item</button>
            </div>

            <div id="itemsContainer"></div>
        </div>

        <div class="section">
            <h2 class="section-title"><span class="section-icon">ℹ️</span> About</h2>
            <div class="about-box">
                <p>This project is my final project for Cloud Computing Internship. It demonstrates a simple logistics tracking web application deployed using Docker, monitored through Prometheus and Grafana, and supported by GitHub Actions.</p>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title"><span class="section-icon">📱</span> Contacts / Socials</h2>
            <div class="contact-box">
                <p class="contact-line"><span class="contact-icon">💼</span> <span class="label">LinkedIn:</span> <a href="https://www.linkedin.com/in/phol-vidallon/" target="_blank">phol-vidallon</a></p>
                <p class="contact-line"><span class="contact-icon">📘</span> <span class="label">Facebook:</span> Phol Vidallon</p>
                <p class="contact-line"><span class="contact-icon">✉️</span> <span class="label">Gmail:</span> pholvidallon@gmail.com</p>
                <p class="contact-line"><span class="contact-icon">📞</span> <span class="label">Mobile Number:</span> 0999-380-9056</p>
            </div>
        </div>

        <div class="footer-note">
            Mini Logistics Tracker Dashboard
        </div>
    </div>

<script>
async function loadItems() {
    const res = await fetch('/items');
    const items = await res.json();

    const container = document.getElementById('itemsContainer');

    if (items.length === 0) {
        container.innerHTML = '<div class="empty-state">📭 No items added yet.</div>';
        return;
    }

    let html = '<div class="item-grid">';
    items.forEach((item, index) => {
        html += `
            <div class="item-card">
                <div class="item-top">
                    <div class="item-emoji">📦</div>
                    <div class="item-name">${item.name}</div>
                </div>
                <div class="item-qty">${item.quantity}x item</div><br>
                <button class="btn btn-remove" onclick="removeItem(${index})">🗑 Remove</button>
            </div>
        `;
    });
    html += '</div>';

    container.innerHTML = html;
}

async function addItem() {
    const input = document.getElementById('itemInput');
    const itemName = input.value.trim();

    if (!itemName) {
        alert('Please enter an item name.');
        return;
    }

    await fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: itemName })
    });

    input.value = '';
    loadItems();
}

async function removeItem(index) {
    await fetch('/remove/' + index, {
        method: 'DELETE'
    });

    loadItems();
}

loadItems();
</script>
</body>
</html>
"""

@app.before_request
def count():
    REQUEST_COUNT.inc()

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/add", methods=["POST"])
def add():
    item = request.json
    item_name = item.get("name", "").strip()

    if not item_name:
        return jsonify({"message": "Item name is required"}), 400

    for existing_item in data:
        if existing_item["name"].lower() == item_name.lower():
            existing_item["quantity"] += 1
            return jsonify(data)

    data.append({
        "name": item_name,
        "quantity": 1
    })
    return jsonify(data)

@app.route("/items")
def items():
    return jsonify(data)

@app.route("/remove/<int:index>", methods=["DELETE"])
def remove(index):
    if 0 <= index < len(data):
        if data[index]["quantity"] > 1:
            data[index]["quantity"] -= 1
        else:
            data.pop(index)
        return jsonify({"message": "Item removed", "items": data})
    return jsonify({"message": "Invalid item index"}), 404

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

app.run(host="0.0.0.0", port=5000)
