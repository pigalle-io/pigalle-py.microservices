from flask import Flask, request, abort, Response
import traceback

from .base import TransporterBase

from ..common.extension import Extension

def exception_to_string(excp):
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
    pretty = traceback.format_list(stack)
    return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)


class HttpTransporter(TransporterBase):

    _defaultOptions = {
        'address': '127.0.0.1',
        'port': 1789,
        'serializer': {
            'module': 'pigalle_microservices.serializers.json.JsonSerializer'
        }
    }

    def __init__(self, options = {}):
        super().__init__('http', options)
        self._connection = Flask(__name__)
        self._options = {**self._defaultOptions, **options};
        self.address = (self._options.get('address') is None) and '127.0.0.1' or self._options.get('address')
        self.port = (self._options.get('port') is None) and 1789 or self._options.get('port')
        klass = Extension.load(self._options['serializer']['module'])
        self.serializer = klass()

    def _wrapService(self, service_name):
        try:
            args = request.data
            retval = self._servicesRegistry.call(service_name, args, self.serializer)
            return Response(retval, content_type=self.serializer.CONTENT_TYPE)
        except Exception as e:
            retval = self.serializer.serialize({'stacktrace': exception_to_string(e)})
            return Response(retval, status=500, content_type=self.serializer.CONTENT_TYPE)

    def _wrapRegisteredServices(self):
        for service_name in self._servicesRegistry.services().keys():
            url = '/%s/%s/%s' % (self._servicesRegistry.namespace, self._servicesRegistry.name, service_name)
            self._connection.add_url_rule(url, service_name, lambda: self._wrapService(service_name))
        return self

    def start(self):
        self._wrapRegisteredServices()
        self._connection.run(self.address, self.port, debug=True)
        return self


