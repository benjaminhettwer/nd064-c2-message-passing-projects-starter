

def register_routes(api, app, root="api"):
    from app.persons.controllers import api as persons_api

    api.add_namespace(persons_api, path=f"/{root}")
