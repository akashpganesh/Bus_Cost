from flask import Flask, jsonify,render_template,request
from pymongo import MongoClient
from Algortithms.gradient_boost_regressor import minimal_cost

app = Flask(__name__)

client = MongoClient('mongodb+srv://signatureresourcehub:signature@cluster0.ww1qbms.mongodb.net/')
db = client['db_project1']
buses = db['buses']

@app.route('/', methods=['GET'])
def home():
    bus_from = buses.distinct('busFrom')
    bus_to = buses.distinct('busTo')
    ac_type = buses.distinct('acNonAc')
    bus_type = buses.distinct('busType')
    return render_template('index.html', bus_from=bus_from, bus_to=bus_to, ac_type=ac_type, bus_type=bus_type)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    bus_from = data.get('bus_from')
    bus_to = data.get('bus_to')
    ac_type = data.get('ac_type')
    bus_type = data.get('bus_type')
    cost = float(data.get('cost'))
    bus_list = list(buses.find({"busFrom" : bus_from, "busTo" : bus_to, "acNonAc" : ac_type, "busType" : bus_type}))
    for bus in bus_list:
        bus['_id'] = str(bus['_id'])
    if bus_list:
        bus_list = minimal_cost(bus_list,cost)
    return jsonify({'status': 'success', 'bus_list': bus_list})

if __name__ == '__main__':
    app.run(debug=True)