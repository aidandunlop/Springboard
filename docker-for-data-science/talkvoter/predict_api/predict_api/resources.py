from flask_restful import Resource, Api
from flask import Blueprint, request, current_app
from .model import ModelWrapper, vectorize_talk_text, talks_df_from_db


api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)


CURRENT_YEAR = 2018  # TODO make this an environment variable
talks_df = talks_df_from_db()
vectorized_text = vectorize_talk_text(talks_df['description'])
count_labeled = len(talks_df[talks_df.year == CURRENT_YEAR])
vectorized_text_labeled = vectorized_text[:count_labeled]
vectorized_text_predict = vectorized_text[count_labeled:]
mw = ModelWrapper(talks_df=talks_df, model_file='talk_model.pkl',
                  vectorized_text_labeled=vectorized_text_labeled,
                  vectorized_text_predict=vectorized_text_predict)


class PredictResource(Resource):

    def post(self):
        return self.get()

    def get(self):
        content = request.json
        predicted_talks = mw.predict(content['user_id'], content['labeled_talk_ids'])
        ret_code = 200
        # TODO error handling
        return {"predicted_talks": predicted_talks}, ret_code


api.add_resource(PredictResource, '/predict/', endpoint="api.predict")
