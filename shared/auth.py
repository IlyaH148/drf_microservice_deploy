from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuth(JWTAuthentication):
    """
    Единая JWT аутентификация для всех микросервисов
    """

    def authenticate(self, request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, token = result

        request.user_id = user.id

        return (user, token)