import requests
from threading import Timer
from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from dateutil import parser as date_parser

from message_info import MessageType
from message_tag import MessageTag
import message_info as mi
# if you want to change to ml sentence tagger, you should replace tagger.tagger_rule_based with tagger.tagger_ml_based
from tagger.tagger_rule_based import sentence_tagger
from alerter import alerter as alerter_component

VCS_REST_URI = 'http://www.vcs-team.tk/report'
TIMER_INTERVAL_IN_SEC = 30

app = Flask(__name__)
api = Api(app)

tagger = sentence_tagger.SentenceTagger()
alerter = alerter_component.Alerter()


class TextMessage(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        message_text = json_data['message_text']
        room_id = int(json_data['room_id'])
        user_id = json_data['user_id']
        timestamp = json_data['timestamp']

        message_tag = tagger.tag_sentence(message_text)
        message_info = mi.MessageInfo(message_tag, MessageType.TEXT, room_id, user_id, date_parser.parse(timestamp, dayfirst=True))
        critical_moment = alerter.handle_message_tag(message_info)

        return jsonify(critical_moment=critical_moment.value)


class DragMessage(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        room_id = int(json_data['room_id'])
        user_id = json_data['user_id']
        timestamp = json_data['timestamp']

        message_info = mi.MessageInfo(MessageTag.NONE, MessageType.DRAG, room_id, user_id, date_parser.parse(timestamp, dayfirst=True))
        critical_moment = alerter.handle_message_tag(message_info)

        return jsonify(critical_moment=critical_moment.value)


class CheckDirectSolutionMessage(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        room_id = int(json_data['room_id'])
        timestamp = json_data['timestamp']

        message_info = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_DS, room_id, 0,
                                      date_parser.parse(timestamp, dayfirst=True))
        critical_moment = alerter.handle_message_tag(message_info)

        return jsonify(critical_moment=critical_moment.value)


class UserConnectMessage(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        room_id = int(json_data['room_id'])
        user_id = json_data['user_id']
        timestamp = json_data['timestamp']

        message_info = mi.MessageInfo(MessageTag.NONE, MessageType.USER_CONNECT, room_id, user_id,
                                      date_parser.parse(timestamp, dayfirst=True))
        critical_moment = alerter.handle_message_tag(message_info)

        return jsonify(critical_moment=critical_moment.value)


class UserDisconnectMessage(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        room_id = int(json_data['room_id'])
        user_id = json_data['user_id']
        timestamp = json_data['timestamp']

        message_info = mi.MessageInfo(MessageTag.NONE, MessageType.USER_DISCONNECT, room_id, user_id,
                                      date_parser.parse(timestamp, dayfirst=True))
        critical_moment = alerter.handle_message_tag(message_info)

        return jsonify(critical_moment=critical_moment.value)


def check_idleness():
    timer = Timer(TIMER_INTERVAL_IN_SEC, check_idleness)
    timer.start()

    list_of_room_ids = alerter.check_idleness()

    for room_id in list_of_room_ids:
        requests.get(url=VCS_REST_URI+'/'+str(room_id)+'/IDLENESS')


api.add_resource(TextMessage, '/text_message')
api.add_resource(DragMessage, '/drag_message')
api.add_resource(CheckDirectSolutionMessage, '/check_ds_message')
api.add_resource(UserConnectMessage, '/user_connect_message')
api.add_resource(UserDisconnectMessage, '/user_disconnect_message')


if __name__ == '__main__':
    check_idleness()
    app.run(host='0.0.0.0', port=36635)
