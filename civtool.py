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

with open('units.RULESET') as unitsfile:
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

with open('terrain.RULESET') as terrainfile:
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
    terrain["defense_bonus"] = int(terrain["defense_bonus"])
    terrain["name"] = terrain["name"][3:-2].replace('_',' ')

for key in terrains.keys():
    terrains[key.replace('_',' ')]=terrains.pop(key)

def dofight(data):
    #work through the calculations, adding each one to data dictionary, so they can be referenced in the form.
    data["attackervalue"] = units[data["attacker"]]["attack"]
    data["attackerlevelmultiplier"] = veterans[data["attackerlevel"]]
    data["attackerlevelvalue"] = data["attackervalue"]*data["attackerlevelmultiplier"]

@bottle.route('/')
def index():
    return(bottle.template("civform",unitlist=sorted(units.keys()),veteranlevels=veterankeys,terrains=sorted(terrains.keys())))

@bottle.post('/combat')
def combat():

    data = bottle.request.params
    data["fortified"] = data.get("fortified","False")
    data["river"] = data.get("river","False")
    for r in data: print(r,data[r])
    dofight(data)
    return(bottle.template("civresults",data))

#print("starting server")
bottle.run(host='192.168.1.32',port=8080,debug=True,reloader=True)
