from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://mongo:27017")
db = client["mydb"]
fnf_coll = db["fnf"]


@app.route("/")
def home():
    return render_template('index.html', members=fnf_coll.find())


@app.route("/fnf/create")
def create():
    return render_template('create.html')


@app.route("/fnf/save", methods=['POST'])
def save():
    name = request.form['name']
    relation = request.form['relation']
    phone = request.form['phone']
    email = request.form['email']

    data = {"name": name, "relation": relation, "phone": phone, "email": email}

    fnf_coll.insert_one(data)
    return redirect(url_for('home'))


@app.route("/fnf/edit/<string:id>")
def edit(id):
    result = fnf_coll.find_one({"_id": ObjectId(id)})
    return render_template('edit.html', member=result)


@app.route("/fnf/update", methods=['POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    relation = request.form['relation']
    phone = request.form['phone']
    email = request.form['email']

    data = {"name": name, "relation": relation, "phone": phone, "email": email}

    fnf_coll.update_one({'_id': ObjectId(id)}, {"$set": data}, upsert=False)
    return redirect(url_for('home'))


@app.route("/fnf/delete/<string:id>", methods=['GET', 'DELETE'])
def delete(id):
    if request.method == 'DELETE':
        if request.json:
            params = request.json
        else:
            params = request.form

        id = params.get('id')

    fnf_coll.remove({"_id": ObjectId(id)})
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
