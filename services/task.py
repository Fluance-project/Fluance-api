from bson.objectid import ObjectId
from services import db


def add_task(task):
    task['account_id'] = ObjectId(task['account_id'])
    db.task.insert_one(task)
    return 200


def get_task(task_id):
    req = db.task.find_one({"_id": ObjectId(task_id)})
    if req is None:
        return 409
    else:
        return req

def get_task_by_account(account_id):
    req = [x for x in db.task.find({ "account_id": ObjectId(account_id) })]
    if req is None:
        return 409
    else:
        return req

def get_task_by_machine(machine_id):
    req = [x for x in db.task.find({ "machine_id": ObjectId(machine_id) })]
    if req is None:
        return 409
    else:
        return req

def remove_task(task_id):
    if db.task.find_one({"_id": ObjectId(task_id)}) is None:
        return 409
    db.task.delete_one({'_id': ObjectId(task_id)})
    return 200


def edit_task(task_id, task):
    if db.task.find_one({"_id": ObjectId(task_id)}) is None:
        return 409

    task['account_id'] = ObjectId(task['account_id'])
    db.task.find_one_and_update(
      {'_id': ObjectId(task_id)},
      { "$set": task},
      upsert=False
    )
    return 200