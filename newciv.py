import re

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

#UNITS

unit_keys = ["class","attack","defense","hitpoints","firepower"] #as specified in the ruleset file, note spelling

with open('units.ruleset') as unitsfile:
    unitdef = re.compile(r'\[unit_(?P<unitname>\w+)')
    for line in unitsfile:
        match = unitdef.match(line)
        if match:
            new_unit = Unit()
            new_unit.name = match.group("unitname").replace("_"," ")
            print(new_unit.name)




