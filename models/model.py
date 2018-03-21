
from models import db
from datetime import datetime, timedelta
from pymongo.cursor import CursorType


class Model():
  collection_name = 'models'
  collection_sort = []

  @classmethod
  def preprocess(cls, document):
    return document


  @classmethod
  def postprocess(cls, document):
    return document


  @classmethod
  def list(cls, document_filter={}, limit=0, skip=0, sort=None):
    if sort is None:
      sort = cls.collection_sort

    return [cls.postprocess(document) for document in db[cls.collection_name].find(document_filter, limit=limit, skip=skip, sort=sort)]


  @classmethod
  def watch(cls, document_filter={}):
    return db[cls.collection_name].watch([{'$match': {'operationType': 'insert'}}])


  @classmethod
  def get(cls, _id):
    return cls.get_where({'_id': ObjectId(_id)})



  @classmethod
  def get_where(cls, document_filter):

    document = db[cls.collection_name].find_one(document_filter)
    if document is None:
      abort(404)

    return cls.postprocess(document)


  @classmethod
  def create(cls, document):
    
    document['created_at'] = datetime.now()
    result = db[cls.collection_name].insert_one(cls.preprocess(document))

    return {'_id': result.inserted_id}


  @classmethod
  def update(cls, _id, document, other_operators={}):

    return cls.update_where({'_id': ObjectId(_id)}, document, other_operators=other_operators)
    



  @classmethod
  def update_where(cls, document_filter, document, multiple=False, other_operators={}):

    document = cls.preprocess(document)
    document['updated_at'] = datetime.now()

    document_set = other_operators
    document_set['$set'] = document


    if not multiple:
      document = db[cls.collection_name].find_one_and_update(document_filter, update=document_set, new=True)
      if document is None:
        abort(404)

      return cls.postprocess(document)

    else:
      return [cls.postprocess(document) for document in db[cls.collection_name].update(document_filter, document_set, multi=True)]



  @classmethod
  def delete(cls, _id):

    db[cls.collection_name].delete_one({'_id': ObjectId(_id)})

    return {'_id': _id}


  @classmethod
  def watch(cls):

    return db[cls.collection_name].watch()


