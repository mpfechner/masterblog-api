import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

DATA_FILE = "posts.json"

def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=2)


@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = load_posts()

    sort_field = request.args.get("sort")
    direction = request.args.get("direction", "asc")

    # Nur sortieren, wenn gültiges Feld übergeben wurde
    if sort_field in {"title", "content", "author", "date"}:
        reverse = direction == "desc"
        try:
            # Bei Datum optional Umwandlung für korrektes Sortieren
            if sort_field == "date":
                posts.sort(key=lambda p: p.get("date", ""), reverse=reverse)
            else:
                posts.sort(key=lambda p: p.get(sort_field, "").lower(), reverse=reverse)
        except Exception as e:
            return jsonify({"error": f"Sorting failed: {str(e)}"}), 400
    elif sort_field:
        return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400

    return jsonify(posts), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json()

    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Missing title or content"}), 400

    posts = load_posts()
    new_id = max((post["id"] for post in posts), default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(new_post)
    save_posts(posts)
    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    posts.remove(post)
    save_posts(posts)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]

    save_posts(posts)
    return jsonify(post), 200


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()
    author_query = request.args.get("author", "").lower()
    date_query = request.args.get("date", "").lower()
    posts = load_posts()

    results = [
        post for post in posts
        if (title_query in post.get("title", "").lower() if title_query else True) and
           (content_query in post.get("content", "").lower() if content_query else True) and
           (author_query in post.get("author", "").lower() if author_query else True) and
           (date_query in post.get("date", "").lower() if date_query else True)
    ]

    return jsonify(results), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

