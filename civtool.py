import re
import pprint
import bottle

ignorecomment = re.compile(r';.*')
unitdef = re.compile(r'\[unit_(?P<unitname>\w+)')
assignment = re.compile(r'(?P<name>\w+)\s*=\s*(?P<data>.*)')
vetnames = re.compile(r'veteran_names = _\("(\w*)"\), _\("(\w*)"\), _\("(\w*)"\), _\("(\w*)"\)')
vetpower = re.compile(r'veteran_power_fact = (\d+), (\d+), (\d+), (\d+)')


units = {}
data_to_get = ["class","attack","defense","hitpoints","firepower"]
veterankeys = []
veteranvalues = []

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
            unitname = match.group("unitname")
            #print(unitname)
            units[unitname] = {}
            unitdict = units[unitname]
            thisline = ""
            while not thisline == "\n":
                #print(thisline)

                #for stat in data_to_get:
                capture = assignment.match(thisline)
                if capture:
                    name = capture.group("name")
                    data = capture.group("data")
                    if name in data_to_get:
                        unitdict[name]=data
                try:
                    thisline = next(unitsfile)
                except StopIteration:
                    print("Iteration ran out!")
            
print(veterankeys)
print(veteranvalues)

@bottle.route('/')
def index():
    return(bottle.template("civform",unitlist=sorted(units.keys())))

@bottle.post('/combat')
def combat():
    print(bottle.request.body.read())
    data = bottle.request.forms
    for n in data: print(n,data[n])
    
    return("THANKS FOR FIGHTING!")

#print("starting server")
bottle.run(host='192.168.1.32',port=8080,debug=True,reloader=True)
