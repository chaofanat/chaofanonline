#ninjia api
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

api.add_router("/flashcard", "flashcard.api.router")