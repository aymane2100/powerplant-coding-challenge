import flask
import json

''' Calculate the merit order. The plants are ordered chronogically in the list by merit order '''    
def calculate_meritorder(data):
  powerplantslist = []
  for powerplant in data["powerplants"]:
    if powerplant["type"] == "windturbine":
      if data["fuels"]["wind(%)"] == 0:
        powerplant["order_merit"] = 10000
      else:
        powerplant["order_merit"] = 1
    elif powerplant["type"] == "gasfired":
      gasprice = data["fuels"]["gas(euro/MWh)"] / powerplant["efficiency"]
      powerplant["order_merit"] = gasprice
    elif powerplant["type"] == "turbojet":
      kerosineprice = data["fuels"]["kerosine(euro/MWh)"] / powerplant["efficiency"]
      powerplant["order_merit"] = kerosineprice
    else:
      print("Type is not valid")
    powerplantslist.append(powerplant)
  powerplantslist.sort(key=lambda x: (x["order_merit"], -x["pmax"]))
  return powerplantslist

''' The main algorithm for calculating how much power to allocate to a plant'''
def process(load):
  powertoProduce = 0 #should be equal to load in the end
  final_response = []
  powerplantslist = calculate_meritorder(load)
  for i in range(len(powerplantslist)):
    power_left_till_load = (load["load"] - powertoProduce)
    print(f''' power left till max load: {power_left_till_load} -> (plant index {i})''')

    if (power_left_till_load == 0):
      final_response.append({"name" : powerplantslist[i]["name"], "p" : 0})


    elif(powerplantslist[i]["type"] == "windturbine"):
      powerGenerated = (powerplantslist[i]["pmax"] / 100) * load["fuels"]["wind(%)"]
      if powerGenerated < power_left_till_load:
        powertoProduce += powerGenerated
        powerplantslist[i]["P"] = powerGenerated
        final_response.append({"name" : powerplantslist[i]["name"], "p" : powerGenerated})

      print(f'''{powertoProduce} power from windturbine"''')

    else:
      powerGenerated = powerplantslist[i]["pmax"]
      if powerGenerated < power_left_till_load:
        if ((power_left_till_load - powerGenerated) < powerplantslist[i+1]["pmin"]): # if the power left till max load is smaller than the minimum of the next plant, reduce the powergeneration of current plant
          powerGenerated = powerGenerated - (powerplantslist[i+1]["pmin"] - (power_left_till_load - powerGenerated))
          powertoProduce += powerGenerated
          powerplantslist[i]["P"] = powerGenerated
          final_response.append({"name" : powerplantslist[i]["name"], "p" : powerGenerated})
        else:
          powertoProduce += powerGenerated
          powerplantslist[i]["P"] = powerGenerated
          final_response.append({"name" : powerplantslist[i]["name"], "p" : powerGenerated})

      elif power_left_till_load >= powerplantslist[i]["pmin"]:
        powertoProduce += power_left_till_load
        powerplantslist[i]["P"] = power_left_till_load
        final_response.append({"name" : powerplantslist[i]["name"], "p" : power_left_till_load})
      
      else:
        powerplantslist[i]["P"] = 0
        final_response.append({"name" : powerplantslist[i]["name"], "p" : 0})
  return final_response

app = flask.Flask(__name__)


@app.route("/")
def main_page():
  return "Main page."


@app.route('/productionplan', endpoint='productionplan', methods=['POST'])
def production_plan():
    load = flask.request.get_json()
    response = process(load)
    return flask.jsonify(response)


app.run(host="0.0.0.0", port=8888)