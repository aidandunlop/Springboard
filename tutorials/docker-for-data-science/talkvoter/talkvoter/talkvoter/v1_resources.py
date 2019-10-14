import requests
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_login import login_required
from flask import Blueprint, abort, current_app
from flask_login import current_user
from sqlalchemy import and_
from sqlalchemy.sql.expression import func
from marshmallow import ValidationError

from .models import db, Talk, Vote
from .serializers import VoteSchema, TalkSchema
from .constants import VoteValue, vote_mapping
import json

PREVIOUS_YEAR = 2017

api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)


def get_talk_or_abort(id):
    talk_obj = db.session.query(Talk).filter(Talk.id == id).first()
    if not talk_obj:
        abort(404, '`talk_id` is not in database')
    return talk_obj


class TalksListResource(Resource):

    @login_required
    def get(self):
        schema = TalkSchema()
        talk_objs = db.session.query(Talk)
        data = schema.dump(talk_objs, many=True).data
        return data, 200


api.add_resource(TalksListResource, '/talks/', endpoint="api.talks")


class TalkDetailResource(Resource):

    @login_required
    def get(self, id):
        schema = TalkSchema()
        talk_obj = get_talk_or_abort(id)
        data = schema.dump(talk_obj).data
        return data, 200


api.add_resource(TalkDetailResource, '/talks/<int:id>/', endpoint="api.talk")


class TalkRandResource(Resource):

    @login_required
    def get(self):
        talks_user_voted_on = [talk.talk_id for talk in current_user.votes]

        schema = TalkSchema()
        talk_obj = (db.session
                      .query(Talk)
                      .filter(and_(Talk.year == PREVIOUS_YEAR, ~Talk.id.in_(talks_user_voted_on)))
                      .order_by(func.random())
                      .first())

        if not talk_obj:
            abort(404, '`talk_id` is not in database')

        data = schema.dump(talk_obj).data
        return data, 200


api.add_resource(TalkRandResource, '/talks/random/', endpoint="api.talkrand")


def validate_vote_type(value):
    if value not in [VoteValue.in_person.value, VoteValue.watch_later.value]:
        raise ValueError("Invalid object: must be watch_later or in_person")
    return value


class VoteResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'vote', type=validate_vote_type,
        required=True, help='Must be in_person | watch_later')

    @login_required
    def post(self, id):
        talk_obj = get_talk_or_abort(id)
        args = self.parser.parse_args()
        vote = args['vote']

        if db.session.query(Vote).filter(Vote.user == current_user, Vote.talk == talk_obj).count():
            abort(409, 'user already voted for this talk')

        schema = VoteSchema()
        msg = ""
        try:
            serial_obj = schema.load(
                {'value': vote_mapping[vote]},
                session=db.session)
        except ValidationError as err:
            err.messages
            valid_data = err.valid_data
            data = str(err)
            print(data, valid_data)
            ret_code = 400
            msg = "Fail"
        else:
            obj = serial_obj.data
            obj.talk = talk_obj
            obj.user = current_user
            db.session.add(obj)
            db.session.commit()
            msg = "Success"
            ret_code = 200
        return {"message": msg}, ret_code


api.add_resource(VoteResource, '/talks/<int:id>/vote/', endpoint="api.vote")


class PredictResource(Resource):

    @login_required
    def post(self):
        return self.get()

    @login_required
    def get(self):
        user = current_user
        votes = [talk_id
                 for talk_id,
                 in (db.session
                       .query(Talk.id)
                       .join(Vote)
                       .filter(Vote.value == vote_mapping[VoteValue.in_person.value],
                               Vote.user == current_user).all())]
        current_app.logger.debug(f'{user.id}: {votes}')
        data = {'user_id': user.id, 'labeled_talk_ids': votes}

        predict_url = current_app.config['PREDICT_ENDPOINT']
        r = requests.post(predict_url, json=data)

        data = json.loads(r.text)
        ret_code = r.status_code
        return data, ret_code


api.add_resource(PredictResource, '/predict/', endpoint="api.predict")
