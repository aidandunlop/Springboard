from marshmallow_sqlalchemy import ModelSchema
import toastedmarshmallow
from .models import Vote


class VoteSchema(ModelSchema):
    class Meta:
        jit = toastedmarshmallow.Jit
        model = Vote
        fields = ['value']


class TalkSchema(ModelSchema):
    class Meta:
        jit = toastedmarshmallow.Jit
        model = Vote
        fields = ['id', 'title', 'description', 'presenters', 'year']
