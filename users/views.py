from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()

# Vista per la registrazione aperta a tutti
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

# Vista per ottenere i dati dell'utente loggato
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        # Aggiungiamo un trucchetto per non far rompere il frontend del tuo amico:
        # il suo JS cerca 'is_moderator', quindi glielo passiamo finto
        data = serializer.data
        data['is_moderator'] = data['is_store_manager'] 
        return Response(data)