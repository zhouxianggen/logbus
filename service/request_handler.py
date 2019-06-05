# coding: utf8 
import json
import traceback
import requests
import tornado.web
from pyobject import PyObject, BaseError
from base_request_handler import BaseRequestHandler
from context import g_ctx


class StatusRequestHandler(tornado.web.RequestHandler):
    """
    获取服务状态
    """
    def head(self):
        self.get()

    def get(self):
        self.write('ok')

    
class LogStreamRequestHandler(BaseRequestHandler):
    """
    注册日志源
    获取日志源列表
    """
    async def post(self):
        self.log.info('[POST]')
        await self.do('register_log_stream')


    async def get(self):
        self.log.info('[GET]')
        await self.do('get_log_stream_list')


    def register_log_stream(self, params):
        user_id = self.get_param(params, 'user_id', essential=True)
        app_id = self.get_param(params, 'user_id', essential=True)
        service_id = self.get_param(params, 'user_id', essential=True)
        g_ctx.model.register_log_stream(user_id=user_id, app_id=app_id, 
                service_id=service_id)
        return self.success()


    def get_log_stream_list(self, params):
        user_id = self.get_param(params, 'user_id', essential=True)
        page = self.get_param(params, 'page', vtype=int, default=1)
        size = self.get_param(params, 'size', vtype=int, default=10)
        lst = g_ctx.model.get_log_stream_list(user_id=user_id, page=page, 
                size=size)
        return self.success({'log_stream_list': lst})


class LogStreamInstanceRequestHandler(BaseRequestHandler):
    """
    获取日志源
    删除日志源
    """
    async def delete(self, option):
        self.log.info('[DELETE]: [{}]'.format(option))
        await self.do('delete_log_stream')


    async def get(self, option):
        self.log.info('[GET]: [{}]'.format(option))
        await self.do('get_log_stream')


    def delete_log_stream(self, params):
        user_id = self.get_param(params, 'user_id', essential=True)
        stream_id = self.get_param(params, 'stream_id', essential=True)
        g_ctx.model.delete_log_stream(user_id=user_id, stream_id=stream_id)
        return self.success()


    def get_log_stream(self, params):
        user_id = self.get_param(params, 'user_id', essential=True)
        stream_id = self.get_param(params, 'stream_id', essential=True)
        s = g_ctx.model.get_log_stream(user_id=user_id, stream_id=stream_id)
        return self.success({'log_stream': s})

