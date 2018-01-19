import json

from .base import SerializerBase
from ..common.logger import get_logger

LOG = get_logger('pigalle.serializers.SerializerBase')

class JsonSerializer(SerializerBase):

    CONTENT_TYPE = 'application/json'

    def __init__(self):
        super().__init__('json')

    def serialize(self, o):
        return json.dumps(o)

    def unserialize(self, o):
        return json.loads(o)
