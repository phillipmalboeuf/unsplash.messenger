

from tornado.websocket import WebSocketHandler
from tornado.web import Application
from tornado.ioloop import IOLoop

from models.message import Message
from models.conversation import Conversation

from helpers.json import SuperEncoder

import time
import json
json._default_encoder = SuperEncoder()


class Mess(WebSocketHandler):
  def open(self):
    # self.write_message({'messages': Message.list()})
    cursor = Message.tail()
    while cursor.alive:
      try:
        message = cursor.next()
        print(message)
        self.write_message({'message': message})
      except StopIteration:
        time.sleep(0.1)

  def on_message(self, message):
    Message.create({'body': message})

  def on_close(self):
    return True

  def check_origin(self, origin):
    return True


if __name__ == '__main__':
  server = Application([('/', Mess)], debug=True)
  server.listen(8666)
  IOLoop.current().start()


