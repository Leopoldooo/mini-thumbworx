from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
data = []

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Logistics Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 40px auto;
            padding: 20px;
            background: #f4f6f8;
        }
        .box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        h1 {
            margin-top: 0;
        }
        input {
            padding: 10px;
            width: 70%;
        }
        button {
            padding: 10px 14px;
            cursor: pointer;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin: 8px 0;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>Mini Logistics Tracker</h1>
        <p>Add and view delivery items.</p>

        <input id="itemInput" type="text" placeholder="Enter item name">
        <button onclick="addItem()">Add Item</button>

        <h2>Items</h2>
        <ul id="itemList"></ul>
    </div>

    <script>
        async function loadItems() {
            const response = await fetch('/items');
            const items = await response.json();

            const list = document.getElementById('itemList');
            list.innerHTML = '';

            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.name;
                list.appendChild(li);
            });
        }

        async function addItem() {
            const input = document.getElementById('itemInput');
            const itemName = input.value.trim();

            if (!itemName) {
                alert('Please enter an item.');
                return;
            }

            await fetch('/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: itemName })
            });

            input.value = '';
            loadItems();
        }

        loadItems();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/add", methods=["POST"])
def add():
    item = request.json
    data.append(item)
    return jsonify({"message": "Item added", "items": data})

@app.route("/items")
def items():
    return jsonify(data)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

app.run(host="0.0.0.0", port=5000)
