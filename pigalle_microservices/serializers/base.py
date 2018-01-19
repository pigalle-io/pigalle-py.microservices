
from ..common.base import PigalleMicroserviceClassBase
from ..common.logger import get_logger

LOG = get_logger('pigalle.serializers.SerializerBase')

class SerializerBase(PigalleMicroserviceClassBase):

    def __init__(self, serializer_name):
        super().__init__()
        self.name = serializer_name

    def serialize(self):
        raise NotImplemented()

    def unserialize(self):
        raise NotImplemented()
