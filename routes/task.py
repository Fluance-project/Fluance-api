from routes import app
from services.auth import check_for_token
from flask import Flask, jsonify, request, session, render_template, make_response
import json
from bson import json_util, ObjectId
import services.task as st


@app.route('/api/v1/task/by-account/<account_id>', methods=['GET'])
@check_for_token
def getTaskForAccount(account_id):
    req = st.get_task_by_account(account_id)
    if req== 409:
        return jsonify({'message': 'task id not found'}), 409
    else:
        return json_util.dumps(req), 200

@app.route('/api/v1/task/by-machine/<machine_id>', methods=['GET'])
@check_for_token
def getTaskForMachine(machine_id):
    req = st.get_task_by_machine(machine_id)
    if req== 409:
        return jsonify({'message': 'task id not found'}), 409
    else:
        return json_util.dumps(req), 200

@app.route('/api/v1/task/<task_id>', methods=['GET'])
@check_for_token
def getTask(task_id):
    # if request.headers['Content-Type'] == 'application/json':
    req = st.get_task(task_id)
    if req == 409:
        return jsonify({'message': 'task id not found'}), 409
    else:
        return json_util.dumps(req), 200
    # else:
    #     return jsonify({'error': 'Please use application/json as content type'}), 422


@app.route('/api/v1/task', methods=['POST'])
@check_for_token
def addTask():
    if request.headers['Content-Type'] == 'application/json':
        req = st.add_task(json.loads(request.data))
        return json_util.dumps(req), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422


@app.route('/api/v1/task/<task_id>', methods=['PATCH', 'PUT'])
@check_for_token
def editTask(task_id):
    if request.headers['Content-Type'] == 'application/json':
        status = st.edit_task(task_id, json.loads(request.data))
        if status== 409:
            return jsonify({'message': 'task id not found'}), 409
        else:
            return jsonify({'message': 'task has been update'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422


@app.route('/api/v1/task/<task_id>', methods=['DELETE'])
@check_for_token
def deleteTask(task_id):
        status = st.remove_task(task_id)
        if status== 409:
            return jsonify({'message': 'task id not found'}), 406

        return jsonify({'message': 'task has been deleted'}), 200


@app.route('/api/v1/task/<task_id>/comment', methods=['POST'])
@check_for_token
def addComment(task_id):
    if request.headers['Content-Type'] == 'application/json':
            status = st.add_comment(task_id, json.loads(request.data))
            if status== 409:
                return jsonify({'message': 'task id not found'}), 406

            return jsonify({'message': 'comment has been added'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422


@app.route('/api/v1/task/<task_id>/comment/<comment_id>', methods=['GET'])
@check_for_token
def getComment(task_id, comment_id):
    req = st.get_comment(comment_id)
    if req == 409:
        return jsonify({'message': 'comment id not found'}), 409
    return json_util.dumps(req), 200

@app.route('/api/v1/task/<task_id>/comment/<comment_id>', methods=['PUT', 'PATCH'])
@check_for_token
def updateComment(task_id, comment_id):
    if request.headers['Content-Type'] == 'application/json':
        req = st.update_comment(comment_id, json.loads(request.data))
        if req == 409:
            return jsonify({'message': 'comment id not found'}), 409
        return jsonify({'message': 'comment has been updated'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/task/<task_id>/comment/<comment_id>', methods=['DELETE'])
@check_for_token
def deleteComment(task_id, comment_id):
        status = st.remove_comment(task_id, comment_id)
        if status== 409:
            return jsonify({'message': 'task id not found'}), 406

        return jsonify({'message': 'task has been deleted'}), 200
