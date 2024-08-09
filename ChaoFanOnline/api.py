#ninjia api
from ninja import NinjaAPI
from ninja.security import django_auth
api = NinjaAPI(auth=django_auth)


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

api.add_router("/flashcard", "flashcard.api.router")





