from flask import *
import database
import json

app = Flask("Error Logging Template")

connection = database.connect()

def getValues(request):
    try:
        values = json.loads(request.get_json()) # request.json() only works if the request mimetype is JSON
        return values
    except: # means that the request was GET or faulty
        pass

@app.route("/")
def homepage():
    return jsonify({"message" : "goodbye"}), 200

@app.route("/log", methods = ["GET", "POST", "PUT", "DELETE"]) # only allow these methods, which corrolate to the four CRUD actions
def log():
    method = request.method
    values = getValues(request)
    try:
        if method == "GET":
            return jsonify(database.retrieve(connection)), 200
        elif method == "POST":
            database.create(connection, values["id"], values["message"])
            return jsonify({"message" : "success"}), 200
    except KeyError: # means that data was not passed in the correct way
        abort(406)
    except TypeError: # means that the data that the user passed cannot be converted into the needed format
        abort(406)
    except Exception as exception: # something went wrong in this function
        return jsonify({"message" : str(exception)})

if __name__ == "__main__":
    app.run(debug = True, port = "4000")