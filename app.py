from flask import Flask,render_template,request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb+srv://signatureresourcehub:signature@cluster0.ww1qbms.mongodb.net/')
db = client['db_project1']
buses = db['buses']

@app.route('/', methods=['GET', 'POST'])
def home():
    bus_from = buses.distinct('busFrom')
    bus_to = buses.distinct('busTo')
    ac_type = buses.distinct('acNonAc')
    bus_type = buses.distinct('busType')
    if request.method == 'POST':
        bus_f = request.form['bus_from']
        bus_t = request.form['bus_to']
        ac_ty = request.form['ac_type']
        bus_ty = request.form['bus_type']
        cost = float(request.form['cost'])
        bus_list = buses.find({"busFrom" : bus_f, "busTo" : bus_t, "acNonAc" : ac_ty, "busType" : bus_ty, 'cost' : {'$lte' : cost}})
        return render_template('index.html', bus_list=bus_list, bus_from=bus_from, bus_to=bus_to, ac_type=ac_type, bus_type=bus_type)
    return render_template('index.html', bus_from=bus_from, bus_to=bus_to, ac_type=ac_type, bus_type=bus_type)

if __name__ == '__main__':
    app.run(debug=True)