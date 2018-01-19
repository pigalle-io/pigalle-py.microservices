from .base import RegistryBase
from ..common.logger import get_logger

LOG = get_logger('ServicesRegistry')


class ServicesRegistry(RegistryBase):
    def __init__(self, namespace, name, context, fns=[]):
        super().__init__('service-registry')
        LOG.debug('Instantiating ServicesRegistry', {namespace: namespace, name: name, context: context})
        self.namespace = namespace
        self.name = name
        self._context = context
        self._fns = fns
        self._services = dict()

    def services(self):
        return self._services

    def init(self):
        """

        :return:
        :todo: async
        """
        LOG.debug('Initializing ServicesRegistry')
        setUpRetval = self.setUp()
        self.registerAll()
        return self

    def register(self, method, service):
        LOG.debug('Registering method', {method: method, service: service})
        self._services[method] = service
        return self

    def registerAll(self):
        LOG.debug('Register all methods of service: ${this._namespace}.${this._name}')
        for method in self._fns:
            print(method)
            self.register(method, getattr(self._context, method))
        return self

    def get(self, method):
        LOG.debug('Get service ${this._namespace}.${this._name}.${method}')
        return self._services.get(method)

    def call(self, method, args=None, serializer=None):
        """
        :param method:
        :param args:
        :return:
        :todo: async
        """
        LOG.debug('Call service ${this._namespace}.${this._name}.${method}')
        try:
            fn = self.get(method)
            retval = getattr(self._context, method)(args)
            LOG.debug('retval: %s', retval)
            return serializer.serialize(retval)
        except Exception as e:
            LOG.error('Uncaught error when calling service ${this._namespace}.${this._name}.${method}', e)
            raise e

    def getSetUpFn(self):
        LOG.debug('Lookup ${this._namespace}.${this._name} for setUp function')
        if hasattr(self._context, 'setUp'):
            return self._context.setUp
        else:
            LOG.info('setUp() function is not defined for ${this._namespace}.${this._name}')

    def setUp(self):
        LOG.debug('Call setUp function for ${this._namespace}.${this._name}')
        if (self.getSetUpFn()):
            LOG.debug('Context', self._context)
            retval = self.getSetUpFn().apply(self._context)
        return self
