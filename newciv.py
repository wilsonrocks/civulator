import re
from itertools import takewhile

import peewee

db = peewee.SqliteDatabase("civstats.db")


class CivModel(peewee.Model):
    class Meta:
        database = db

class UnitClass(CivModel):
    name = peewee.CharField(max_length=20)

class VetLevel(CivModel):
    name = peewee.CharField(max_length=20)
    multiplier = peewee.IntegerField()

class Unit(CivModel):
    unit_class = peewee.ForeignKeyField(UnitClass)
    attack = peewee.IntegerField
    defence = peewee.IntegerField
    HP = peewee.IntegerField()
    FP = peewee.IntegerField()

class Terrain(CivModel):
    name = peewee.CharField(max_length=20)
    terrain_class = peewee.CharField(max_length=20)
    defence_bonus = peewee.IntegerField()


class Relationship(CivModel):
    terrain = peewee.ForeignKeyField(Terrain, related_name="native_to")
    unit_class = peewee.ForeignKeyField(UnitClass, related_name="can_enter")

    class Meta:
        database = db
        indexes = (
                (('terrain', 'unit_class'), True),)

db.create_tables([UnitClass,VetLevel,Unit,Terrain,Relationship],safe=True)
assignment = re.compile(r'(?P<name>\w+)\s*=\s*(?P<data>.*)')
#UNITS
#TODO Need to do unit classes first

unit_keys = ["class","attack","defense","hitpoints","firepower"] #as specified in the ruleset file, note spelling

with open('units.ruleset') as unitsfile:
    unitdef = re.compile(r'\[unit_(?P<unitname>\w+)')
    for line in unitsfile:
        match = unitdef.match(line)
        if match:
            new_unit = Unit()
            new_unit.name = match.group("unitname").replace("_"," ")
            print(new_unit.name)
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
                        new_unit.unit_class = UnitClass(name=data)
                    if name == "attack":
                        new_unit.attack = data
                    if name == "defense": #check spellings!!
                        new_unit.defence = data 
                    if name == "firepower":
                        new_unit.FP = data
                    if name == "hitpoints":
                        new_unit.HP = data

            new_unit.save()




