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



#jwt 认证器
from django.contrib.auth import get_user_model
class JWTTokenUser(HttpBearer,JWTBaseAuthentication):
    def __init__(self) -> None:
        super().__init__()
        self.user_model = get_user_model()
    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        return super().jwt_authenticate(request, token)
        
    





api = NinjaExtraAPI(auth=JWTTokenUser(),csrf=False,version='1.0.0')
api.register_controllers(NinjaJWTDefaultController)




####################################   测试api    ###################################################################
@api.post("/bearer")
def bearer(request):
    return {'message': 'hello'}





@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

api.add_router("/flashcard", "flashcard.api_v1.router")





