
import inspect

from .registries.services_registry import ServicesRegistry
from .common.base import PigalleMicroserviceClassBase
from .common.logger import get_logger
from .common.extension import Extension

LOG = get_logger('pigalle.microservice')

defaultsOpts = {
    'namespace': 'default',
    'transporter': {
        'module': 'pigalle_microservices.transporters.http.HttpTransporter',
        'options': {}
    },
}

def get_all_methods(o):
    return [method[0] for method in inspect.getmembers(o, predicate=inspect.ismethod)]

class Microservice(PigalleMicroserviceClassBase):

    def __init__(self, options={}):
        LOG.info('Instantiate Microservice %s', options)
        super().__init__()
        self._name = self.__class__.__name__
        self._options = {**defaultsOpts, **options}

    def _get_children_services(self):
        LOG.info('_get_children_services')
        microservice_methods = dir(Microservice)
        child_methods = get_all_methods(self)
        print(child_methods)
        print(microservice_methods)
        retval = [x for x in child_methods if x not in set(microservice_methods)]
        print(retval)
        return retval

    def _createServicesRegistryForTransporter(self):
        print(self._options)
        self._options['transporter']['options']['servicesRegistry'] = ServicesRegistry(self._options.get('namespace'), self._name, self, self._get_children_services());
        return self

    def expose(self, extension_name=None):
        LOG.info('expose')
        self._createServicesRegistryForTransporter()
        extension_name = (extension_name is None) and self._options['transporter']['module'] or extension_name
        klass = Extension.load(extension_name)
        self._transporter = klass(self._options['transporter']['options'])
        return self

    def start(self):
        LOG.info('start')
        if (not self._transporter):
            raise Exception('Missing transporter')
        servicesRegistryInitRetval = self._transporter._servicesRegistry.init()
        return self._transporter.start()

    @classmethod
    def factory(cls, options={}):
        LOG.info('factory')
        return cls(options)



