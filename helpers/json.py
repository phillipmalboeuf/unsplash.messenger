
from json import JSONEncoder
from bson.objectid import ObjectId

from datetime import datetime, date, timedelta


class SuperEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, ObjectId):
      return str(obj)

    if isinstance(obj, datetime):
      return obj.isoformat()

    if isinstance(obj, date):
      return obj.isoformat()

    if isinstance(obj, timedelta):
      return str(obj)

    return super().default(self, obj)