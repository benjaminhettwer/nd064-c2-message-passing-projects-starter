import grpc
import person_pb2
import person_pb2_grpc
import logging
from concurrent import futures

import sys
import os.path
# Import from sibling directory ..\app
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from app.persons.services import PersonService
from app.persons.models import Person
from wsgi import app

logger = logging.getLogger("persons-api")


class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Create(self, request, context):

        request_value = {
            "id": int(request.id),
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }
        logger.info('Requested persons create: ' + str(request_value))
        with app.app_context():
            new_person: Person = PersonService.create(request_value)
            return person_pb2.PersonMessage(new_person)
        
    def Retrieve(self, request, context):
        logger.info('Requested persons retrive: ' + str(request.id))
        with app.app_context():
            person = PersonService.retrieve(request.id)
            if not person:
                error_message = 'User ID not found!'
                context.set_details(error_message)
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return person_pb2.PersonMessage()
            
            return person_pb2.PersonMessage(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
        
    def Retrieve_all(self, request, context):
        logger.info('Requested person retrieve all')
        with app.app_context():
            persons = PersonService.retrieve_all()
            result = person_pb2.PersonMessageList()
            for p in persons:
                p_res = person_pb2.PersonMessage(
                id=p.id,
                first_name=p.first_name,
                last_name=p.last_name,
                company_name=p.company_name
                )
                result.persons.extend([p_res])
            
            return result
    

def start_grpc_server():
    gprc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), gprc_server)
    
    gprc_server.add_insecure_port("[::]:5005")
    print('Starting GRPC server on port 5005')
    gprc_server.start()
    gprc_server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_grpc_server()

        