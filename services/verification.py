from bson.objectid import ObjectId
from pymongo import MongoClient
import hashlib
import os
import binascii
import uuid

DATABASE_USER = os.environ.get("DATABASE_USER", "root")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "root")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "127.0.0.1:27017")
DATABASE_URI = f'mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/'

def account_check(account):
    """
    check if the json recived is in the good format
    :param account:
    :return:
    """
    if KeysVerif(account):
        return 406

    client = MongoClient(f'{DATABASE_URI}')
    db = client.fluance

    if isNotNewEmail(account['email'], db):
        return 409

    # hash password
    account['password'] = hash_password(account['password'])
    db.accounts.insert_one(account).inserted_id
    return 200


def add_user(account_id, user):

    id_ = ObjectId(account_id)

    client = MongoClient(f'{DATABASE_URI}')
    db = client.fluance

    if db.accounts.find_one({"_id": id_}) is None:
        return 409

    for item in user:
        item.update({'user_id': ObjectId(os.urandom(12))})
        update_tags(id_, item, db)


def remove_user(account_id, user_id):

    account_id = ObjectId(account_id)

    client = MongoClient(f'{DATABASE_URI}')
    db = client.fluance

    if db.accounts.find_one({"_id": account_id}) is None:
        return 409
    user_id = ObjectId(user_id)
    delete_user(account_id, user_id, db)



def update_tags(ref, new_tag, db):
    db.accounts.update_one(
        {'_id': ref},
        {'$push': {'user': new_tag}},
        upsert = True)


def delete_user(account_id, user_id, db):
    db.accounts.update_one(
      {'_id': account_id},
      {'$pull': {'user':{ 'user_id': user_id}}}
    )


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
    client = MongoClient(f'{DATABASE_URI}')
    db = client.fluance

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

