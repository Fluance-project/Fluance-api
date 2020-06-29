from bson.objectid import ObjectId
from services import db
import hashlib
import os
import binascii
import uuid

"""
Machine:
	- uuid
	- name
	- status
	- Account id
"""

def account_check(account):
    """
    check if the json recived is in the good format
    :param account:
    :return:
    """
    if KeysVerif(account):
        return 406

    if isNotNewEmail(account['email'], db):
        return 409

    # hash password
    account['password'] = hash_password(account['password'])
    db.accounts.insert_one(account).inserted_id
    return 200


def add_user(account_id, user):
    id_ = ObjectId(account_id)
    newUser = {
        'user_id': ObjectId(os.urandom(12)),
        'fistName' : user['firstName'],
        'lastName' : user['lastName'],
        'title' : user['intitule'],
        'role' : user['role'],
    }
    db.accounts.update(
        { "_id" : id_ },
        { "$push": { "user": newUser } }
        )
    return newUser

def get_all_account():
    req = [x for x in db.accounts.find()]
    if req is None:
        return 404
    else:
        return req

def get_account(account_id):
    req = db.accounts.find_one({ "_id": ObjectId(account_id) })
    if req is None:
        return 409
    else:
        return req

def get_user(user_id):
    rq = db.accounts.find_one(
        {'user.user_id': ObjectId(user_id)},
        {'user.$': 1}
    )
    if rq is None:
        return 409
    return rq

def update_user(user_id, update):
    query = {}
    if get_user(user_id) == 409:
        return 409

    user_id = ObjectId(user_id)
    for key,val in update.items():
        query.update({"user.$."+key:val})
    myquery =  {'user': { '$elemMatch': { 'user_id': user_id} }, 'user.user_id':user_id}
    newvalues = {"$set":query}
    db.accounts.update_one(myquery, newvalues)

def remove_user(account_id, user_id):

    acc_id = ObjectId(account_id)
    usr_id = ObjectId(user_id)
    db.accounts.update_one(
      {'_id': acc_id},
      {'$pull': {'user':{ 'user_id': usr_id}}}
    )

def update_tags(ref, new_tag, db):
    db.accounts.update_one(
        {'_id': ref},
        {'$addToSet': {'user': new_tag}},
        upsert = True)

def hash_password(password):
    """
    Hash a password for storing.
    :param password: string
    :return: string
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(account):
    """
    Verify a stored password against one provided by user
    :param account: json
    :return: boolean (true if the password is valid)
    """

    if isNotNewEmail(account['email'], db):
        provided_password = account['password']
        stored_password = db.accounts.find_one({'email': account['email']})['password']
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password


def KeysVerif(list_):
    """
    Check if all keys are correct
    :param list_:
    :return:
    """
    if {x for x in list_.keys()} == {'companyName', 'email', 'password'}:
        return False
    return True


def isNotNewEmail(name, db):
    if db.accounts.find_one({"email": name}) is not None:
        return True
    return False

