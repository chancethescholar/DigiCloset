from flask import Flask, Response, request
from Closet import Closet
from OOTD import OOTD
import asyncio
from flask_cors import CORS
import json
import pymysql

app = Flask(__name__)

CORS(app)

closet = Closet()
ootd = OOTD()

def get_cur():
    db_user = "root"
    db_pwd = "password"
    db_host = "localhost"

    conn = pymysql.connect(
        user = db_user,
        password = db_pwd,
        host = db_host,
        cursorclass = pymysql.cursors.DictCursor,
        autocommit = True
    )
    return conn.cursor()

@app.route("/")
def home():
    return "DigiCloset API"

# get all clothing in closet
@app.route("/api/closet", methods = ["GET"])
def get_clothing():
    # Parse pagination requirements
    type = request.args.get('type', "")
    colors = request.args.get('colors', "")

    cur = get_cur()

    type_list = type.split(",")
    type_params = ""
    for i in range(len(type_list)):
        type_params += "'" + type_list[i] + "'"
        if i != len(type_list) - 1:
            type_params += ","

    colors_list = colors.split(",")
    color_params = "'"
    for i in range(len(colors_list)):
        color_params += colors_list[i]
        if i != len(colors_list) - 1:
            color_params += "|"
    color_params += "'"

    if type != "" and colors == "":
        cur.execute("SELECT DISTINCT * FROM digi_closet.closet WHERE type IN (" + type_params + ");")
    elif type == "" and colors != "":
        cur.execute("SELECT DISTINCT * FROM digi_closet.closet WHERE colors REGEXP" + color_params + ";")
    elif type != "" and colors != "":
        cur.execute("SELECT DISTINCT * FROM digi_closet.closet WHERE type IN (" + type_params + ") AND colors REGEXP" + color_params + ";")
    else:
        cur.execute("SELECT DISTINCT * FROM digi_closet.closet;")

    result = cur.fetchall()
    if result:
        rsp = Response(json.dumps(result, indent=4), status=200, content_type="application.json")
    else:
        rsp = Response(json.dumps([]), status=200, content_type="text/plain")

    return rsp

# add clothing item to closet db
@app.route("/api/closet/add", methods = ["POST"])
def add_clothing():
    json_data = request.get_json()
    path = json_data['path']

    path = "/Users/chanceonyiorah/Documents/Spring2023/Visual Interfaces/Final Project/flask-server/Clothing/" + path
    #path = "/Users/chanceonyiorah/Documents/Spring2023/Visual Interfaces/Final Project/flask-server/Clothing/BlackShirt.jpeg"
    #print("path", path)

    cur = get_cur()
    cur.execute("SELECT id FROM digi_closet.closet ORDER BY id DESC LIMIT 1;")
    next_id = cur.fetchone()
    print("NEXT ID", next_id)

    if next_id is None:
        next_id = 0

    else:
        next_id = next_id['id'] + 1

    clothing = closet.add_clothing(path, next_id)
    #print(clothing)

    try:
        if len(clothing['colors']) == 0:
            colors = None
        else:
            colors = ', '.join(clothing['colors'])
        cur.execute("""INSERT INTO digi_closet.closet (type, colors, image) VALUES (%s, %s, %s)""", (clothing["type"], colors, clothing["image_path"]))
    except pymysql.err.IntegrityError as err:
        return Response("There was a problem adding", status=404, content_type="text/plain")
    
    return get_clothing_by_id(next_id)

# get clothing item from closet db
@app.route("/api/closet/<id>/get", methods = ["GET"])
def get_clothing_by_id(id):
    cur = get_cur()
    cur.execute(f'SELECT * FROM digi_closet.closet WHERE id={id}')
    result = cur.fetchone()
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

# update clothing item in closet db
@app.route("/api/closet/<id>/update", methods = ["POST"])
def update(id):
    json_data = request.get_json()

    type = json_data['type']
    colors = json_data['colors']
    image = json_data['image']

    print("JSON", type, colors)

    cur = get_cur()
    cur.execute("""UPDATE digi_closet.closet SET type=%s, colors=%s WHERE id=%s;""", (type, colors, id))
    result = cur.fetchone()
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("Updated successfully", status=200, content_type="text/plain")

    return rsp

# delete clothing item in closet db
@app.route("/api/closet/<id>/delete", methods = ["POST"])
def delete(id):
    cur = get_cur()
    
    try:
        cur.execute(f'DELETE FROM digi_closet.closet WHERE id={id}')
    except pymysql.err.IntegrityError as err:
        return Response("There was a problem deleting", status=404, content_type="text/plain")
    
    return Response("clothing deleted successfully", status=200, content_type="application.json")

# get current location
@app.route("/api/ootd/location")
def get_location():
    location = ootd.get_location()
    return Response(json.dumps(location), status=200, content_type="application.json")

# get the current temperature in current location
@app.route("/api/ootd/weather")
def get_temperature():
    weather = asyncio.run(ootd.get_weather())
    return Response(json.dumps(weather), status=200, content_type="application.json")

# generate outfit based on weather
@app.route("/api/ootd")
def get_ootd():
    cur = get_cur()
    cur.execute("SELECT * FROM digi_closet.closet")
    clothing = cur.fetchall()

    outfit = ootd.get_ootd(clothing)

    if outfit:
        rsp = Response(json.dumps(outfit, indent=4), status = 200, content_type = "application.json")
    else:
        rsp = Response("NOT FOUND", status = 404, content_type = "text/plain")
    
    return rsp

if __name__ == "__main__":
    app.run(port=8000, debug=True)