from flask import Flask, request
from flask_cors import CORS
import JSONGenerator
app = Flask(__name__)
CORS(app)

@app.route('/')
def get_json():
    searchword = request.args.get('key', '')
    try:
        json_to_send = JSONGenerator.JSONWrite(searchword)
    except:
        json_to_send = 'spool not found'
    return json_to_send

if __name__ == '__main__':
    app.run()
