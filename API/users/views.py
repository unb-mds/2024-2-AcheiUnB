from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Item
from .serializers import ItemSerializer
from msal import ConfidentialClientApplication
from django.shortcuts import redirect
from django.http import JsonResponse
import os

# Configurações do MSAL
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
AUTHORITY = os.getenv("MICROSOFT_AUTHORITY")
REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI")


class ItemListCreateView(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filtrar itens por categoria se passado na query string
        category = self.request.query_params.get("category")
        is_valuable = self.request.query_params.get("is_valuable")

        queryset = super().get_queryset()
        if category:
            queryset = queryset.filter(category=category)
        if is_valuable is not None:
            queryset = queryset.filter(is_valuable=is_valuable.lower() == "true")

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None
        )
    
    def ItemListCreateView(ListCreateAPIView):
        queryset = Item.objects.all()
        serializer_class= ItemSerializer
        permission_classes = [IsAuthenticatedOrReadOnly]

def microsoft_login(request):
    """Inicia o fluxo de login com Microsoft."""
    app = ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    # URL para redirecionar o usuário para o login da Microsoft
    auth_url = app.get_authorization_request_url(
        scopes=["User.Read"],  # Scopes solicitados
        redirect_uri=REDIRECT_URI,
    )
    return redirect(auth_url)

def microsoft_callback(request):
    """Processa o callback da Microsoft após o login."""
    # Obtém o código de autorização da URL
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Código de autorização não fornecido."}, status=400)

    # Troca o código pelo token
    app = ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=["User.Read"],  # Scopes solicitados
        redirect_uri=REDIRECT_URI,
    )

    if "access_token" in result:
        # Você pode usar o token para autenticar o usuário
        user_info = result.get("id_token_claims")
        return JsonResponse({"message": "Login bem-sucedido!", "user": user_info})
    else:
        return JsonResponse({"error": "Erro ao obter o token.", "details": result}, status=400)