from bson.objectid import ObjectId
from services import db


def add_machine(machine):
    machine['account_id'] = ObjectId(machine['account_id'])
    db.machine.insert_one(machine)
    return 200


def get_machine(machine_id):
    req = db.machine.find_one({"_id": ObjectId(machine_id)})
    if req is None:
        return 409
    else: 
        return req

def get_machine_by_account(account_id):
    req = [x for x in db.machine.find({ "account_id": ObjectId(account_id) })]
    if req is None:
        return 409
    else: 
        return req

def remove_machine(machine_id):
    if db.machine.find_one({"_id": ObjectId(machine_id)}) is None:
        return 409
    db.machine.delete_one({'_id': ObjectId(machine_id)})
    return 200


def edit_machine(machine_id, machine):
    if db.machine.find_one({"_id": ObjectId(machine_id)}) is None:
        return 409

    if 'account_id' in machine:
        machine['account_id'] = ObjectId(machine['account_id'])
    db.machine.find_one_and_update(
      {'_id': ObjectId(machine_id)},
      { "$set": machine},
      upsert=False
    )    
    return 200