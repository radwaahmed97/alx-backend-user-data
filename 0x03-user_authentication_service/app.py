#!/usr/bin/env python3
"""basic flask application"""

from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__='app')


@app.route('/', methods=['GET'])
def Home():
    """return a JSON payload of the form"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
