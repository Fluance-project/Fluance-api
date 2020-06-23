from routes import app
from services.auth import check_for_token
from flask import Flask, jsonify, request, session, render_template, make_response
import json
from bson import json_util, ObjectId
import services.machine as sm


@app.route('/api/v1/machine/<machine_id>', methods=['GET'])
@check_for_token
def getMachine(machine_id):
    if request.headers['Content-Type'] == 'application/json':
        req = sm.get_machine(machine_id)
        if req== 409:
            return jsonify({'message': 'machine id not found'}), 409
        else:
            return json_util.dumps(req), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/machine', methods=['POST'])
@check_for_token
def addMachine():
    if request.headers['Content-Type'] == 'application/json':
        sm.add_machine(json.loads(request.data))
        return jsonify({'message': 'machine has been added'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/machine/<machine_id>', methods=['PATCH', 'PUT'])
@check_for_token
def editMachine(machine_id):
    if request.headers['Content-Type'] == 'application/json':
        status = sm.edit_machine(machine_id, json.loads(request.data))
        if status== 409:
            return jsonify({'message': 'machine id not found'}), 409
        else:
            return jsonify({'message': 'machine has been update'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/machine/<machine_id>', methods=['DELETE'])
@check_for_token
def deleteMachine(machine_id):
        status = sm.remove_machine(machine_id)
        if status== 409:
            return jsonify({'message': 'machine id not found'}), 406

        return jsonify({'message': 'machine has been deleted'}), 200

