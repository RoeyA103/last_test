from pymongo import MongoClient

class MongoService():
    def __init__(self,my_logger,their_logger,mongo_host,db):
        self.logger = my_logger
        self.their_logger = their_logger
        self.mongo_host = mongo_host
        self.db = db

        self.logger.info("MongoService created")
        self.their_logger(level="info", message=f"MongoService created", extra_info=None)

    def _get_collection(self,collection):
        try:
            client = MongoClient(self.mongo_host)

            db = client[self.db]

            collection = db[collection]

            return collection
        
        except Exception as e:
            self.logger.error(f"MongoService - error in connecting to mongo: {e}")
            self.their_logger(level="error", message=f"MongoService - error in connecting to mongo: {e}", extra_info=None)
        

    def save_doc(self,doc:dict,collection):
        try:
            collection = self._get_collection(collection=collection)

            collection.insert_one(document=doc)

            self.logger.info(f"MongoService - doc inserted sucssefuly:\n{doc}")
            self.their_logger(level="info", message=f"MongoService - doc inserted sucssefuly:{doc}", extra_info=doc)

        except Exception as e:
            self.logger.error(f"MongoService - error in inseting doc: {e}")
            self.their_logger(level="error", message=f"MongoService - error in inseting doc: {e}", extra_info=doc)

    def get_doc(self,entity_id:str,collection):
        try:
            collection = self._get_collection(collection=collection)

            res = collection.find_one({"entity_id":entity_id})
            if res:
                self.logger.info(f"MongoService - doc pulled sucssefuly:\n{entity_id}")
                self.their_logger(level="info", message=f"MongoService - doc pulled sucssefuly:{entity_id}", extra_info={"entity_id":entity_id})

            return res
        
        except Exception as e:
            self.logger.error(f"MongoService - error in geting doc: {e}")
            self.their_logger(level="error", message=f"MongoService - error in getting doc: {e}", extra_info={"entity_id":entity_id})

    def replace_doc(self,doc:dict,entity_id,collection):
        try:
            collection = self._get_collection(collection=collection)

            query_filter = { "entity_id" : entity_id }
            update_operation = doc
            result = collection.replace_one(query_filter, update_operation)

            if result.modified_count == 0:
                self.logger.info(f"MongoService - doc updeted : {entity_id}")
                self.their_logger(level="info", message=f"MongoService - doc updeted : {entity_id}", extra_info={"entity_id":entity_id})

        
        except Exception as e:
            self.logger.error(f"MongoService - error in updating doc: {e}")
            self.their_logger(level="error", message=f"MongoService - error in updating doc: {e}", extra_info={"entity_id":entity_id})


    def update_doc(self,updated_filed:dict,entity_id,collection):
        try:
            collection = self._get_collection(collection=collection)

            query_filter = { "entity_id" : entity_id }
            update_operation = updated_filed
            result = collection.update_one(query_filter, update_operation)

            if result.modified_count == 0:
                self.logger.info(f"MongoService - doc updeted : {entity_id}")
                self.their_logger(level="info", message=f"MongoService - doc updeted : {entity_id}", extra_info={"entity_id":entity_id})

        
        except Exception as e:
            self.logger.error(f"MongoService - error in updating doc: {e}")
            self.their_logger(level="error", message=f"MongoService - error in updating doc: {e}", extra_info={"entity_id":entity_id})

