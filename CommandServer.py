#!/usr/bin/python
## CommandServer.py

# TODO: add args to enable disable this
import logging
# logging.basicConfig(filename="/home/pi/projects/CommandServer/debug.log", level=logging.DEBUG)

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import unicodedata
from Commands import Commands

# -----------------------------------------------+
# webHandles implementation
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '0.0.1',
                     'last_build': date.today().isoformat() }
        self.write(response)
 
class commandHandler(tornado.web.RequestHandler):
    def get(self, command):

    	command = unicodedata.normalize('NFKD', command).encode('ascii','ignore')
        result = commands.process(command)
        response = { 'command': command,
                     'handled': result.handled,
                     'extras': result.extras,
                     'requestTime': date.today().isoformat() }
        self.write(response)

 # -----------------------------------------------+

# commands profile loaded from file
commands = Commands()

# Tornado callbacks matched by url
webHandles = tornado.web.Application([
    (r"/cmd/(.*)", commandHandler),
    (r"/version", VersionHandler)
])

 # Initiate web server
if __name__ == "__main__":
    logging.debug('starting CommandServer')
    webHandles.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

