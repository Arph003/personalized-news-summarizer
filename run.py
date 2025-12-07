# run.py

import os
from flask import Flask, send_from_directory
from app.backend.api import api_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    frontend_dir = os.path.join(os.path.dirname(__file__), "app", "frontend")

    @app.route("/")
    def index():
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/<path:path>")
    def frontend_files(path: str):
        """
        Serve static frontend files (CSS, JS) from app/frontend.
        """
        return send_from_directory(frontend_dir, path)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
