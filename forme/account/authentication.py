from account.models import Token
from rest_framework.authentication import BaseAuthentication


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = None
        token = request.headers.get("Authorization")
        print(str(token).split())
        if token:
            try:
                token = str(token).split()[1]
                print(token)
                user = Token.objects.get(token=token).user
            except:
                print("Invalid token")
        else:
            user = None

        return user, None
