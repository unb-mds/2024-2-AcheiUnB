from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Brand, Color, Item
from .serializers import BrandSerializer, ColorSerializer, ItemSerializer
from msal import ConfidentialClientApplication
from django.shortcuts import redirect
from django.http import JsonResponse
import os
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .serializers import ItemImageSerializer
from .models import Item, ItemImage
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth import login
import logging
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.views import View
from .models import UserProfile
import cloudinary.uploader


# Configurações do MSAL
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI")
SCOPES = ["User.Read"]
logger = logging.getLogger(__name__)
User = get_user_model()


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "color", "is_valuable", "status"]
    search_fields = ["name", "location", "description"]
    ordering_fields = ["created_at", "found_lost_date"]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None
        )


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ItemImageViewSet(ModelViewSet):
    serializer_class = ItemImageSerializer

    def get_queryset(self):
        item_id = self.kwargs.get("item_id")
        return ItemImage.objects.filter(item_id=item_id)

    def create(self, request, *args, **kwargs):
        item_id = self.kwargs.get("item_id")
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Valida o limite de imagens
        if item.images.count() >= 3:
            return Response(
                {"error": "Você pode adicionar no máximo 3 imagens por item."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fazer upload da imagem para o Cloudinary.
        image_file = request.FILES.get("image")

        if not image_file:
            return Response(
                {"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = self.get_serializer(data={"image_url": image_url})
        serializer.is_valid(raise_exception=True)
        serializer.save(item=item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retorna os dados do usuário autenticado",
        responses={
            200: openapi.Response(
                description="Usuário autenticado",
                examples={
                    "application/json": {
                        "id": 2,
                        "username": "testuser",
                        "email": "231026714@aluno.unb.br",
                        "first_name": "Euller",
                        "last_name": "Silva",
                        "matricula": "231026714",
                        "foto": "https://foto.unb.br/user-picture.jpg",
                    }
                },
            )
        },
    )
    def get(self, request):
        user = request.user
        social_account = SocialAccount.objects.filter(
            user=user, provider="microsoft"
        ).first()

        # Extrai a matrícula e a foto do usuário(se disponivel)
        if user.email and "@aluno.unb.br" in user.email:
            matricula = user.email.split("@")[0]
        else:
            matricula = None

        foto = social_account.extra_data.get("photo", None) if social_account else None

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "matricula": matricula,
            "foto": foto,
        }
        return Response(user_data)


def fetch_user_data(access_token):
    """
    Busca os dados do usuário autenticado na Microsoft Graph API.
    """
    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Erro ao buscar dados do usuário: {response.status_code} - {response.text}"
        )


User = get_user_model()


def save_or_update_user(user_data, access_token=None):
    """
    Salva ou atualiza os dados do usuário no banco de dados.
    """
    try:
        user, created = User.objects.update_or_create(
            email=user_data.get("userPrincipalName"),
            defaults={
                "username": user_data.get("userPrincipalName").split("@")[0],
                "first_name": user_data.get("givenName", ""),
                "last_name": user_data.get("surname", ""),
                "password": "defaultpassword",
                "last_login": datetime.now(),
                "is_superuser": False,
                "is_staff": False,
                "is_active": True,
                "date_joined": datetime.now(),
            },
        )
        photo_url = get_and_save_user_photo(access_token, user.id)
        profile, _ = UserProfile.objects.update_or_create(
            user=user, defaults={"profile_picture": photo_url}
        )
        return user, created
    except Exception as e:
        raise Exception(f"Erro ao salvar ou atualizar o usuário: {e}")


def microsoft_login(request):
    """
    Inicia o fluxo de login com a Microsoft e redireciona o usuário automaticamente.
    """
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY
    )
    # Gera a URL de autorização
    auth_url = app.get_authorization_request_url(
        scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    return redirect(auth_url)


def microsoft_callback(request):
    """
    Processa o callback da Microsoft após o login.
    """
    authorization_code = request.GET.get("code")
    if not authorization_code:
        logger.error("Código de autorização não fornecido.")
        return JsonResponse(
            {"error": "Código de autorização não fornecido."}, status=400
        )

    app = ConfidentialClientApplication(
        client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY
    )

    try:
        # Troca o código de autorização pelo token de acesso
        token_response = app.acquire_token_by_authorization_code(
            code=authorization_code, scopes=SCOPES, redirect_uri=REDIRECT_URI
        )
        if "access_token" in token_response:
            access_token = token_response["access_token"]

            # Buscar dados do usuário
            user_data = fetch_user_data(access_token)

            # Salvar ou atualizar o usuário no banco de dados
            user, created = save_or_update_user(
                user_data=user_data, access_token=access_token
            )

            # Autenticar o usuário
            login(request, user)

            # Redirecionar para a página desejada
            return redirect("http://localhost:8000/#/found")
        else:
            logger.error("Falha ao adquirir token de acesso.")
            return JsonResponse(
                {"error": "Falha ao adquirir token de acesso."}, status=400
            )
    except Exception as e:
        logger.error(f"Erro no callback: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def get_user_data(access_token):
    """Busca os dados do usuário autenticado na Microsoft Graph API."""
    url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Erro ao buscar dados do usuário: {response.status_code} - {response.text}"
        )


class TestUserView(APIView):
    """
    View para testar criação e recuperação de usuários.
    """

    def post(self, request):
        """
        Testa a criação de um usuário completo no banco de dados.
        """
        data = request.data  # Dados enviados no corpo da requisição

        try:
            user, created = User.objects.update_or_create(
                email=data.get("email"),
                defaults={
                    "username": data.get("username"),
                    "first_name": data.get("first_name"),
                    "last_name": data.get("last_name"),
                    "password": data.get(
                        "password", ""
                    ),  # Salve apenas hashes reais em produção
                    "last_login": data.get("last_login", datetime.now()),
                    "is_superuser": data.get("is_superuser", False),
                    "is_staff": data.get("is_staff", False),
                    "is_active": data.get("is_active", True),
                    "date_joined": data.get("date_joined", datetime.now()),
                },
            )
            return Response(
                {
                    "message": "Usuário criado/atualizado",
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """
        Testa a recuperação de todos os usuários do banco de dados.
        """
        users = User.objects.all().values(
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
        )
        return Response(list(users), status=status.HTTP_200_OK)


def get_user_photo(access_token):
    """
    Busca o blob da foto do usuário autenticado na Microsoft Graph API.

    :param access_token: O token de acesso do usuário.
    :return: O conteúdo da foto do usuário (blob).
    """
    url = "https://graph.microsoft.com/v1.0/me/photo/$value"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(
        url, headers=headers, stream=True
    )  # stream=True para trabalhar com blobs
    if response.status_code == 200:
        return response.content  # Retorna o blob da foto
    else:
        raise Exception(
            f"Erro ao buscar a foto do usuário: {response.status_code} - {response.text}"
        )


def get_and_save_user_photo(access_token, user_id):
    """
    Busca o blob da foto do usuário na API Microsoft Graph e salva localmente.

    :param access_token: Token de acesso do usuário.
    :param user_id: ID único do usuário (usado para nomear o arquivo).
    :return: URL do arquivo salvo ou None se a foto não estiver disponível.
    """
    if not access_token:
        raise ValueError(
            "O parâmetro access_token não foi fornecido para obter a foto."
        )

    # Diretório onde as fotos serão salvas
    MEDIA_DIR = "/home/pedroubu/Imagens/AcheiUnBFt/"
    os.makedirs(MEDIA_DIR, exist_ok=True)  # Garante que o diretório existe

    url = "https://graph.microsoft.com/v1.0/me/photo/$value"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        # Nome do arquivo (usando o user_id)
        file_path = os.path.join(MEDIA_DIR, f"{user_id}.jpg")

        # Salva o blob como um arquivo local
        with open(file_path, "wb") as photo_file:
            for chunk in response.iter_content(chunk_size=8192):
                photo_file.write(chunk)

        # Gera a URL (ajuste conforme necessário)
        file_url = f"/home/pedroubu/Imagens/AcheiUnBFt/{user_id}.jpg"
        return file_url
    elif response.status_code == 404:  # Foto não encontrada
        logger.warning(f"Foto de perfil não encontrada para o usuário {user_id}.")
        return None
    else:
        raise Exception(
            f"Erro ao buscar a foto do usuário: {response.status_code} - {response.text}"
        )


class DeleteUserView(View):
    """
    Endpoint para deletar usuários pelo ID.
    """

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()  # Deleta o usuário do banco de dados
            return JsonResponse(
                {"message": f"Usuário com ID {user_id} foi deletado com sucesso."},
                status=200,
            )
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuário não encontrado."}, status=404)
