'''
@desc:
@author: Martin Huang
@time: created on 2020/5/9 15:46
@修改记录:
'''
from xiaoIceServer.ice_server import *
import logging
from tornado import options

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    options.define("p", default=6789, help="running port", type=int)
    options.define("h", default='127.0.0.1', help="listen address", type=str)
    options.define("a", default='', help="Allowed IPs to access this server,split by comma", type=str)
    options.define("auth", default=False, help="Enable auth? default is set to false", type=bool)
    options.parse_command_line()
    p = options.options.p
    h = options.options.h
    allow = options.options.a
    AUTH = options.options.auth
    if allow:
        ALLOWED_IPS = allow.split(',')
    RunServer.run_server(port=p, host=h)