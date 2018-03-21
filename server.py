

from tornado.websocket import WebSocketHandler
from tornado.web import Application
from tornado.ioloop import IOLoop

from threading import Thread

from models.message import Message
from models.conversation import Conversation

from helpers.json import SuperEncoder

from bson.objectid import ObjectId
import asyncio
import time
import json
json._default_encoder = SuperEncoder()


class Mess(WebSocketHandler):
  def open(self):
    self.write_message({'messages': Message.list(limit=88)})
    self.stream = Thread(target=self.watch)
    self.stream.start()

  def on_message(self, message):
    Message.create({'body': message})

  def on_close(self):
    self.stream.join(0)


  def watch(self):
    asyncio.set_event_loop(asyncio.new_event_loop())
    with Message.watch() as stream:
      for change in stream:
        self.write_message({'message': change['fullDocument']})


  def check_origin(self, origin):
    return True


if __name__ == '__main__':
  server = Application([('/', Mess)], debug=True)
  server.listen(8666)
  IOLoop.current().start()


