from peewee import *

database = SqliteDatabase('data.db')


class User(Model):
    id = IntegerField(unique=True, primary_key=True)
    nickname = CharField(max_length=33)

    class Meta:
        database = database


class Channel(Model):
    id = IntegerField(unique=True, primary_key=True)
    title = CharField(max_length=150)

    count = IntegerField(null=True)

    class Meta:
        database = database


class Mapping(Model):
    user_id = IntegerField(unique=True, index=True)
    channel_id = IntegerField(unique=True, index=True)
    join_date = DateTimeField(null=True)
    leave_date = DateTimeField(null=True)

    class Meta:
        database = database


class Status(Model):
    id = IntegerField(unique=True, primary_key=True)
    user_id = CharField(max_length=33)
    state = IntegerField()

    class Meta:
        database = database

