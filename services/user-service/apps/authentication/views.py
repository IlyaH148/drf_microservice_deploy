from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from apps.users.models import User


User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email_input = request.data.get('username') 
    password = request.data.get('password')

    if not email_input or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


    try:
        user = User.objects.get(email=email_input)
    except User.DoesNotExist:
        # Если такого email вообще нет в базе
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


    authenticated_user = authenticate(username=user.username, password=password)

    if authenticated_user and authenticated_user.is_active:
        refresh = RefreshToken.for_user(authenticated_user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': authenticated_user.id,
                'email': authenticated_user.email,      # qwee@mail.ru
                'username': authenticated_user.username,# qwe
                'first_name': authenticated_user.first_name,
                'last_name': authenticated_user.last_name,
            }
        }, status=status.HTTP_200_OK)


    return Response(
        {'error': 'Invalid credentials'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error':'Refresh token is required'},
                            status = status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken(refresh_token)
        return Response({
                'access':str(refresh.access_token),
                })

    except Exception as e:
        return Response({
        'error':'Invalid refresh token'},
        status = status.HTTP_401_UNAUTHORIZED)
    
    


