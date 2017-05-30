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
