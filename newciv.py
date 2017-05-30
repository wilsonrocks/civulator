import re
from itertools import takewhile

import peewee

db = peewee.SqliteDatabase("civstats.db")


class CivModel(peewee.Model):
    class Meta:
        database = db

class VetLevel(CivModel):
    name = peewee.CharField(max_length=20)
    multiplier = peewee.IntegerField()

class Unit(CivModel):
    name = peewee.CharField(max_length=20)
    unit_class = peewee.CharField(max_length=20)
    attack = peewee.IntegerField()
    defence = peewee.IntegerField()
    HP = peewee.IntegerField()
    FP = peewee.IntegerField()

class Terrain(CivModel):
    name = peewee.CharField(max_length=20)
    terrain_class = peewee.CharField(max_length=20)
    defence_bonus = peewee.IntegerField()

db.create_tables([VetLevel,Unit,Terrain],safe=True)
assignment = re.compile(r'(?P<name>\w+)\s*=\s*(?P<data>.*)')

#UNITS

with open('units.ruleset') as unitsfile:
    unitdef = re.compile(r'\[unit_(?P<unitname>\w+)')

    for line in unitsfile:
        match = unitdef.match(line)
        if match:
            new_unit = Unit()
            new_unit.name = match.group("unitname").replace("_"," ").title()
            for stat in takewhile(lambda x: x != "\n" ,unitsfile):
                capture = assignment.match(stat)
                if capture:
                    name = capture.group("name")
                    data = capture.group("data")
                    try:
                        data = int(data)
                    except ValueError:
                        pass
                    if name == "class":
                        new_unit.unit_class = data[1:-1]
                    if name == "attack":
                        new_unit.attack = data
                    if name == "defense": #check spellings!!
                        new_unit.defence = data 
                    if name == "firepower":
                        new_unit.FP = data
                    if name == "hitpoints":
                        new_unit.HP = data

            new_unit.save()

        #VETLEVELS STUFF

VetLevel(name="Green",multiplier=0).save()
VetLevel(name="Veteran",multiplier=50).save()
VetLevel(name="Hardened",multiplier=75).save()
VetLevel(name="Elite",multiplier=100).save()














#TERRAIN
with open('terrain.ruleset') as terrainfile:
    terrainblock = re.compile(r'\[terrain_(?P<terrainname>\w+)\]')
    for line in terrainfile:
        match = terrainblock.match(line)
        if match:
            new_terrain = Terrain()
            new_terrain.name = match.group("terrainname").replace("_"," ").title()

            for stat in takewhile(lambda x: x!= "\n", terrainfile):
                capture = assignment.match(stat)
                if capture:
                    name = capture.group("name")
                    data = capture.group("data")
                    try:
                        data = int(data)
                    except ValueError:
                        pass
                    if name == "class":
                        new_terrain.terrain_class = data[1:-1]
                    if name == "defense_bonus":
                        new_terrain.defence_bonus = data
            new_terrain.save()


