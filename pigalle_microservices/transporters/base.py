
from ..common.base import PigalleMicroserviceClassBase
from ..common.logger import get_logger

LOG = get_logger('pigalle.transporters.TransporterBase')

class TransporterBase(PigalleMicroserviceClassBase):

    def __init__(self, protocol_name, options={}):
        super().__init__()
        self.protocol_name = protocol_name
        self._servicesRegistry = options.get('servicesRegistry')
        if self._servicesRegistry is None:
            raise Exception('Missing services registry')

    def start(self):
        raise NotImplemented()
