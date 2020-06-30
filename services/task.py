from bson.objectid import ObjectId
from services import db
import datetime
import os

def add_task(task):
    task['account_id'] = ObjectId(task['account_id'])
    task['machine_id'] = ObjectId(task['machine_id'])
    task['start_date'] = datetime.datetime.strptime(task['start_date'], '%Y-%m-%dT%H:%M:%SZ%z').timestamp()
    if task['end_date'] is not None:
        task['end_date'] = datetime.datetime.strptime(task['end_date'], '%Y-%m-%dT%H:%M:%SZ%z').timestamp()
    id_ = db.task.insert_one(task)
    return id_.inserted_id


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

    if 'start_date' in task:
        task['start_date'] = datetime.datetime.strptime(task['start_date'], '%Y-%m-%dT%H:%M:%SZ%z').timestamp()
    if 'end_date' in task:
        task['end_date'] = datetime.datetime.strptime(task['end_date'], '%Y-%m-%dT%H:%M:%SZ%z').timestamp()
    if 'account_id' in task:
        task['account_id'] = ObjectId(task['account_id'])
    if 'machine_id' in task:
        task['machine_id'] = ObjectId(task['machine_id'])
    db.task.find_one_and_update(
      {'_id': ObjectId(task_id)},
      { "$set": task},
      upsert=False
    )
    return 200


def add_comment(task_id, comment):
    id_ = ObjectId(task_id)
    if db.task.find_one({"_id": id_}) is None:
        return 409
    for item in comment:
        item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%SZ%z').timestamp()
        item.update({'comment_id': ObjectId(os.urandom(12))})
        update_tags(id_, item, db)

def get_comment(comment_id):
    rq = db.task.find_one(
        {'comment.comment_id': ObjectId(comment_id)},
        {'comment.$': 1}
    )
    if rq is None:
        return 409
    return rq


def update_comment(comment_id, update):
    query = {}
    if get_comment(comment_id) == 409:
        return 409

    comment_id = ObjectId(comment_id)

    update['time'] = datetime.datetime.strptime(update['time'], '%Y-%m-%dT%H:%M:%SZ%z').timestamp()
    for key,val in update.items():
        query.update({"comment.$."+key:val})
    myquery =  {'comment': { '$elemMatch': { 'comment_id': comment_id} }, 'comment.comment_id':comment_id}
    newvalues = {"$set":query}
    db.task.update_one(myquery, newvalues)

def update_tags(ref, new_tag, db):
    db.task.update_one(
        {'_id': ref},
        {'$addToSet': {'comment': new_tag}},
        upsert = True)

def remove_comment(task_id, comment_id):
    task_id = ObjectId(task_id)

    if db.task.find_one({"_id": task_id}) is None:
        return 409

    comment_id = ObjectId(comment_id)
    delete_comment_query(task_id, comment_id, db)


def delete_comment_query(task_id, comment_id, db):
    db.task.update_one(
      {'_id': task_id},
      {'$pull': {'comment':{ 'comment_id': comment_id}}}
    )