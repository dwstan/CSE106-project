from flask import Flask, jsonify
from website import create_app
from api import create_api
from website.model import db
from sqlalchemy import text

app = create_app()
api = create_api(app)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app_context = app.app_context()
    with app_context:
        db.create_all()
    
    app.run()


