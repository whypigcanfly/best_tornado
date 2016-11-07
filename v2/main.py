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
#import tornado.web.asynchronous
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(2)

    @tornado.gen.coroutine
    def get(self):
	self.time_delay(10)
        self.write("first--")
	self.finish()

    @run_on_executor
    def time_delay(self, count):
  	time.sleep(count)
	return  "first"

class SecondHandler(tornado.web.RequestHandler):
    
    executor = ThreadPoolExecutor(2)

    @tornado.gen.coroutine
    def get(self):
	self.time_delay(10)
	self.write("second--")
	self.finish()

    @run_on_executor
    def time_delay(count):
	time.sleep(count)
	return  "second"

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/first", MainHandler),
	(r"/second", SecondHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
