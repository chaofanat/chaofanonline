#ninjia api
from typing import Any
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.security.session import SessionAuth
from ninja.security import django_auth
from ninja.security import HttpBearer
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth,JWTBaseAuthentication
from ninja_extra import NinjaExtraAPI



class DjangoSessionAuth(SessionAuth):
    def authenticate(self, request, token=None):

        return super().authenticate(request,key=token)


    





api = NinjaExtraAPI(auth=DjangoSessionAuth(),version='0.0.0')





####################################   测试api    ###################################################################
@api.post("/bearer")
def bearer(request):
    return {'message': 'hello'}





@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

api.add_router("/flashcard", "flashcard.api.router")





