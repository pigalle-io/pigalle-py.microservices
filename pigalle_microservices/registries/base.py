
from pigalle_microservices.common.base import PigalleMicroserviceClassBase

class RegistryBase(PigalleMicroserviceClassBase):

    def __init__(self, t):
        super(RegistryBase).__init__()
        self._type = t.lower()

