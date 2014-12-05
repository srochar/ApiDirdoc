from flask import Response,Flask,request
import dirdoc
import json
app = Flask(__name__)

@app.route('/ApiDirdoc', methods = ['GET'])
def api_hello():
    d = None
    if "rut" in request.args and 'password' in request.args:
        rut = request.args['rut']
        password = request.args['password']
        d = dirdoc.Dirdoc(rut,password)
        d = d.info
    js = json.dumps(d)
    resp = Response(js, status=200, mimetype='application/json')
    return resp
    
    
if __name__ == '__main__':
    app.run()