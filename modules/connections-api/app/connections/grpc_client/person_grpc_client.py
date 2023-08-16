import os
import grpc
from . import person_pb2_grpc
from . import person_pb2 
from typing import Dict, List
from app.connections.schemas import PersonSchema

PERSONS_SERVICE_HOST = os.environ["PERSONS_SERVICE_HOST"]
PERSONS_SERVICE_PORT = os.environ["PERSONS_SERVICE_PORT"]

class PersonService:
 
    @staticmethod
    def retrieve_all() -> List[PersonSchema]:
        channel = grpc.insecure_channel(f"{PERSONS_SERVICE_HOST}:{PERSONS_SERVICE_PORT}")
        stub = person_pb2_grpc.PersonServiceStub(channel)
        emtpy_list = person_pb2.Empty()
        response = stub.Retrieve_all(emtpy_list)
        #print(response.persons)
        person_list: List[PersonSchema] = []
        for p in response.persons:
            cur_per = PersonSchema()
            cur_per.id = p.id
            cur_per.first_name = p.first_name
            cur_per.last_name = p.last_name
            cur_per.company_name = p.company_name
            person_list.append(cur_per)
        
        print(person_list)
        return person_list