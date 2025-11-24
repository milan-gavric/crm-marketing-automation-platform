from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .authentication import generate_token

User = get_user_model()


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email.lower())
        if password:
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # If no password provided, allow login (simplified auth)
    except User.DoesNotExist:
        # Create user with default password if email-based auth is used
        default_password = password or 'default-password-123'
        user = User.objects.create_user(email=email.lower(), password=default_password)

    token = generate_token(user)

    response = Response({
        'message': 'Login successful',
        'token': token,
        'user': {'id': user.id, 'email': user.email}
    })

    # Set cookies
    response.set_cookie(
        'token',
        token,
        max_age=7 * 24 * 60 * 60,  # 7 days
        httponly=True,
        samesite='Lax',
        path='/'
    )
    response.set_cookie(
        'email',
        user.email,
        max_age=7 * 24 * 60 * 60,
        httponly=False,
        samesite='Lax',
        path='/'
    )

    return response


@api_view(['POST'])
def logout(request):
    response = Response({'message': 'Logout successful'})
    response.delete_cookie('token')
    response.delete_cookie('email')
    return response

