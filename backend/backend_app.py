from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Aktiviert CORS für alle Routen

# Beispielhafte Blogposts (startet hartkodiert, später durch JSON ersetzt)
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."}
]

@app.route("/api/posts", methods=["GET"])
def get_posts():
    return jsonify(POSTS), 200


@app.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json()

    # Validierung: title und content müssen vorhanden sein
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Missing title or content"}), 400

    # Neue ID generieren: Max-ID aus vorhandenen Posts + 1
    new_id = max((post["id"] for post in POSTS), default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    # Suche nach dem Post anhand der ID
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    data = request.get_json()
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    # Nur vorhandene Felder überschreiben
    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]

    return jsonify(post), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

