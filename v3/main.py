#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import time
#from tornado import gen
import Queue
from  threading import Thread
from tornado.options import define, options

from queue_thread import ThreadPool

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
	yield ThreadPool.add_task(self.time_delay(10))
        self.write("first--")
	self.finish()

    def time_delay(self, count):
  	time.sleep(count)
	return  "first"

class SecondHandler(tornado.web.RequestHandler):
    
    @tornado.web.asynchronous
    def get(self):
	self.data=""
	print "second-start",int(time.time())
	ThreadPool.add_task(self.add_to_callback)
	print "second-end",int(time.time())

    def time_delay(self,count):
	time.sleep(count)
	return  "second"

    def add_to_callback(self):
	self.time_delay(10)
	self.data="second"
        tornado.ioloop.IOLoop.instance().add_callback(self.send_response)

    def send_response(self):
        self.write(self.data)
	print "response_time", int(time.time())
        self.finish()


class ThirdHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
	self.data="" 
	print "third-start",int(time.time())
    	mystr = ThreadPool.add_task(self.add_to_callback)
	print "third-end",int(time.time())

    def api_1(self):
    	time.sleep(10)
    	return "Hello Word"

    def add_to_callback(self):
	self.api_1()
	self.data="third="
	tornado.ioloop.IOLoop.instance().add_callback(self.send_response)

    def send_response(self):
	self.write(self.data)
	print "response_time", int(time.time())
	self.finish()


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/first", MainHandler),
	(r"/second", SecondHandler),
	(r"/third", ThirdHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":

    ThreadPool.initialize()
    main()
