import os
# Change working directory so relative paths (and template lookup) work again
#os.chdir(os.path.dirname(__file__))


import re
import pprint
import bottle

ignorecomment = re.compile(r';.*')
unitdef = re.compile(r'\[unit_(?P<unitname>\w+)')
assignment = re.compile(r'(?P<name>\w+)\s*=\s*(?P<data>.*)')
vetnames = re.compile(r'veteran_names = _\("(\w*)"\), _\("(\w*)"\), _\("(\w*)"\), _\("(\w*)"\)')
vetpower = re.compile(r'veteran_power_fact = (\d+), (\d+), (\d+), (\d+)')

terrainblock = re.compile(r'\[terrain_(?P<terrainname>\w+)\]')



units = {}
unit_data_to_get = ["class","attack","defense","hitpoints","firepower"]
terrain_data_to_get = ["name","class","defense_bonus","native_to"]
terrains = {}
veterankeys = []
veteranvalues = []

#Do all the stuff for UNITS

with open('units.ruleset') as unitsfile:
    for line in unitsfile:


        if vetnames.match(line):
            for n in range(1,5):
                veterankeys.append(vetnames.match(line).group(n))

        if vetpower.match(line):
            for n in range(1,5):
                value = (int(vetpower.match(line).group(n))/100)
                veteranvalues.append(value)

        match = unitdef.match(line)
        if match: # if we have a unit definition, do the following:
            unitname = match.group("unitname").replace("_"," ")
            unitname = unitname.replace("aegis","AEGIS")
            units[unitname] = {}
            unitdict = units[unitname]
            thisline = ""
            while not thisline == "\n":

                capture = assignment.match(thisline)
                if capture:
                    name = capture.group("name")
                    data = capture.group("data")
                    if name in unit_data_to_get:
                        try:
                            data = int(data)
                        except ValueError:
                            pass

                        unitdict[name]=data
                try:
                    thisline = next(unitsfile)
                except StopIteration:
                    print("Iteration ran out!")

veterans=dict(zip(veterankeys,veteranvalues))

# do all the stuff for TERRAIN

with open('terrain.ruleset') as terrainfile:
    for line in terrainfile:
        match = terrainblock.match(line)
        if match:
            terrainname = match.group("terrainname")
            terrains[terrainname] = {}
            terraindict = terrains[terrainname]
            thisline = ""
            while not thisline == "\n":
                capture = assignment.match(thisline)

                if capture:
                    name = capture.group("name")
                    data = capture.group("data")
                    if name in terrain_data_to_get:
                        terraindict[name]=data
                try:
                    thisline = next(terrainfile)
                except StopIteration:
                    print("Iteration ran out!")

# strip extra stuff

for terrainname in terrains:
    terrain = terrains[terrainname]
    terrain["class"] = terrain["class"][1:-1] #strip first and last character (remove "s)
    terrain["defense_bonus"] = (int(terrain["defense_bonus"])+100)/100
    terrain["name"] = terrain["name"][3:-2].replace('_',' ')

for key in terrains.keys():
    terrains[key.replace('_',' ')]=terrains.pop(key)

import json


open("civJSON","w").write(json.dumps([data,terrains,veterans,units])) #TODO change so that it loads from this instead of ruleset files if ruleset files haven't been updated

#print(data)
#print(terrains)
#print(veterans)
print(units)


def dofight(data):
    #work through the calculations, adding each one to data dictionary, so they can be referenced in the form.
    #attacker stuff
    data["attackervalue"] = units[data["attacker"]]["attack"]
    data["attackerlevelmultiplier"] = veterans[data["attackerlevel"]]
    data["attackerlevelvalue"] = data["attackervalue"]*data["attackerlevelmultiplier"]
    #defender stuff
    data["defendervalue"] = units[data["defender"]]["defense"]
    data["defenderlevelmultiplier"] = veterans[data["defenderlevel"]]
    data["defenderlevelvalue"] = data["attackervalue"]*data["defenderlevelmultiplier"]

    #terrain stuff
    for d in data: print(d,data[d])
    data["terrainmultiplier"] = terrains[data["terrain"]]["defense_bonus"]#TODO should only be if Land not Big Land
    data["terrainvalue"] = data["terrainmultiplier"] * data["defenderlevelvalue"]

    #fortified
    if data["fortified"] and data["location"] != "in_city":
        data["fortifiedmultiplier"] = 1.5
    else:
        data["fortifiedmultiplier"] = 1
    data["fortifiedvalue"] = data["fortifiedmultiplier"] * data["terrainvalue"]

def do_checkbox(data,fieldname):
    if data.get(fieldname,False):
        data[fieldname] = True
    else:
        data[fieldname] = False

@bottle.route('/')
def index():
    return(bottle.template("civform",unitlist=sorted(units.keys()),veteranlevels=veterankeys,terrains=sorted(terrains.keys())))

@bottle.post('/combat')
def combat():

    data = bottle.request.params

    checkboxes = ["greater_8", "walls", "coastal", "great_wall", "river","fortified"]

    for box in checkboxes:
        do_checkbox(data,box)

    data["attackerclass"] = units["attacker"]["class"]
    

    for d in data:
        print(d,data[d])
    


    dofight(data)
    return(bottle.template("civresults",data))

#print("starting server")
bottle.run(host='192.168.1.32',port=8080,debug=True,reloader=True)
#application = bottle.default_app()
