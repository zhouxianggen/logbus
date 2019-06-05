# coding: utf8 
import json
import traceback
import tornado.web
from pyobject import PyObject, BaseError
from context import g_ctx


class BaseRequestHandler(tornado.web.RequestHandler, PyObject):
    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        PyObject.__init__(self)
    

    def fail(self, error_code='ERR_ACTION_FAILED', error_desc='', data=None):
        self.log.error('{}:{}'.format(error_code, error_desc))
        return {'status': 'FAIL', 'error_code': error_code, 
                'error_desc': error_desc, 'data': data}


    def success(self, data={}):
        return {'status': 'SUCCESS', 'error_code': '', 'error_desc': '', 
                'data': data}


    def get_params(self):
        params = {}
        if (self.request.method.upper() == 'POST' and self.request.body 
                and self.request.body[0] == 123):
            try:
                params.update(json.loads(self.request.body))
            except Exception as e:
                self.log.error('parse body failed [{}]'.format(
                        self.request.body))
        params.update({k:v[0].decode('utf8') for k,v in 
            self.request.arguments.items() if v})
        return params


    def get_param(self, params, key, default=None, essential=False, vtype=None):
        value = params.get(key, None)
        if value == 'undefined':
            value = None
        if vtype is not None and value is not None:
            try:
                value = vtype(value)
            except Exception as e:
                raise BaseError('ERR_PARAM_TYPE_ERROR', key)
        if value is None and default is not None:
            value = default
        if value is None and essential:
            raise BaseError('ERR_MISSING_PARAM', key)
        return value


    async def do(self, operator=''):
        params = self.get_params()
        try:
            func = getattr(self, operator)
            result = await g_ctx.loop.run_in_executor(g_ctx.pool, 
                    func, params)
            self.finish(result)
        except BaseError as e:
            self.finish(self.fail(e.error_code, e.error_desc))
        except Exception as e:
            self.log.exception(e)
            self.finish(self.fail('ERR_SERVICE_EXCEPTION', 
                    traceback.format_exc()))

