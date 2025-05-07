import logging
import os
from datetime import datetime

import cloudinary
import cloudinary.uploader
import requests
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from msal import ConfidentialClientApplication
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import ItemFilter
from .models import Brand, Category, Color, Item, ItemImage, Location, UserProfile
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ColorSerializer,
    ItemImageSerializer,
    ItemSerializer,
    LocationSerializer,
)
from .tasks import find_and_notify_matches_task, upload_images_to_cloudinary


class UserListView(View):
    """
    Endpoint para listar todos os usuários e obter um usuário pelo ID.
    """

    @swagger_auto_schema(
        operation_description="Retorna um usuário pelo ID",
        responses={
            200: openapi.Response(
                "Usuário encontrado",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID do usuário"
                        ),
                        "first_name": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Nome do usuário"
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING, description="E-mail do usuário"
                        ),
                        "foto": openapi.Schema(
                            type=openapi.TYPE_STRING, description="URL da foto do usuário"
                        ),
                    },
                ),
            )
        },
    )
    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            profile = getattr(user, "profile", None)
            profile_picture = profile.profile_picture if profile else None

            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "email": user.email,
                "foto": profile_picture,
            }
            return JsonResponse(user_data, status=200)

        users = User.objects.all()
        users_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "email": user.email,
                "foto": getattr(user.profile, "profile_picture", None),
            }
            for user in users
        ]

        return JsonResponse(users_data, safe=False, status=200)


CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = ["User.Read", "email"]
logger = logging.getLogger(__name__)
User = get_user_model()


class FoundItemPagination(PageNumberPagination):
    """Paginação personalizada para itens achados."""

    page_size = 27


class LostItemPagination(PageNumberPagination):
    """Paginação personalizada para itens perdidos."""

    page_size = 27


class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ItemFilter
    search_fields = ["name", "description", "category__name", "location__name"]

    ordering_fields = ["created_at", "found_lost_date"]

    @swagger_auto_schema(
        operation_description="Retorna a lista de itens cadastrados no sistema.",
        responses={200: openapi.Response("Lista de itens", ItemSerializer(many=True))},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo item.",
        request_body=ItemSerializer,
        responses={201: openapi.Response("Item criado com sucesso", ItemSerializer)},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_queryset(self):

        self.request.query_params.get("status", None)
        if "found" in self.request.path:
            return (
                Item.objects.filter(status="found")
                .select_related("category", "location", "color", "brand")
                .prefetch_related("images")
            )
        elif "lost" in self.request.path:
            return (
                Item.objects.filter(status="lost")
                .select_related("category", "location", "color", "brand")
                .prefetch_related("images")
            )

        return Item.objects.select_related(
            "category", "location", "color", "brand"
        ).prefetch_related("images")

    def get_paginated_response(self, data):
        total_found = Item.objects.filter(status="found").count()
        total_lost = Item.objects.filter(status="lost").count()
        paginated_response = super().get_paginated_response(data)
        paginated_response.data.update(
            {
                "total_found": total_found,
                "total_lost": total_lost,
            }
        )
        return paginated_response

    def schedule_match_task(self, item):
        find_and_notify_matches_task.apply_async((item.id,), countdown=10)

    def perform_create(self, serializer):
        item = serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None
        )
        self.schedule_match_task(item)

    def perform_update(self, serializer):
        item = serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None
        )
        self.schedule_match_task(item)


""" Estrutura de match para implementação futura
Match de itens caso o usuário queira ver os possíveis matches pelo site:

 class MatchItemViewSet(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request, item_id):
          retorna possiveis matches
         try:
             target_item = Item.objects.get(id=item_id, user=request.user)
         except Item.DoesNotExist:
             return Response({"error": "Item não encontrado."}, status=404)

         matches = find_and_notify_matches(target_item)
         data = [
             {
                 "id": match.id,
                 "barcode": match.barcode,
                 "status": match.status,
                 "name": match.name,
                 "description": match.description,
             }
             for match in matches
         ]
         return Response(data, status=200)"""


class MyItemsLostView(APIView):
    """
    listar os itens do usuário dividos em 'lost' e 'found'.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retorna a lista de itens perdidos pelo usuário autenticado.",
        responses={
            200: openapi.Response("Lista de itens perdidos", ItemSerializer(many=True))
        },
    )
    def get(self, request):
        user = request.user

        lost_items = Item.objects.filter(user=user, status="lost")

        serializer = ItemSerializer(lost_items, many=True)

        return Response(serializer.data)


class MyItemsFoundView(APIView):
    """
    listar os itens do usuário 'found'
    """

    @swagger_auto_schema(
        operation_description="Retorna a lista de itens achados pelo usuário autenticado.",
        responses={200: openapi.Response("Lista de itens achados", ItemSerializer(many=True))},
    )
    def get(self, request):
        user = request.user
        found_items = Item.objects.filter(user=user, status="found")
        serializer = ItemSerializer(found_items, many=True)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    pagination_class = None


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


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
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        MAX_IMAGES = 2

        if item.images.count() >= MAX_IMAGES:
            return Response(
                {"error": f"Você pode adicionar no máximo {MAX_IMAGES} imagens por item."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        image_file = request.FILES.get("image")

        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(data={"image_url": image_url})
        serializer.is_valid(raise_exception=True)
        serializer.save(item=item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Token válido"})


class UserDetailView(APIView):
    """
    Retorna os detalhes do usuário autenticado.
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retorna os detalhes do usuário autenticado.",
        responses={
            200: openapi.Response(
                "Detalhes do usuário",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_INTEGER, description="ID do usuário"
                        ),
                        "username": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Nome de usuário"
                        ),
                        "email": openapi.Schema(
                            type=openapi.TYPE_STRING, description="E-mail do usuário"
                        ),
                        "first_name": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Primeiro nome"
                        ),
                        "last_name": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Último nome"
                        ),
                        "matricula": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Matrícula (se aluno UnB)"
                        ),
                        "foto": openapi.Schema(
                            type=openapi.TYPE_STRING, description="URL da foto do usuário"
                        ),
                    },
                ),
            )
        },
    )
    def get(self, request):
        user = request.user
        request.headers.get("Authorization", "").replace("Bearer ", "")
        logger.info(f"Usuário autenticado: {user.username} (ID: {user.id})")

        try:
            profile = UserProfile.objects.get(user=user)
            foto_url = profile.profile_picture
        except UserProfile.DoesNotExist:
            foto_url = None

        matricula = user.email.split("@")[0] if "@aluno.unb.br" in user.email else None

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "matricula": matricula,
            "foto": foto_url,
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
        try:
            photo_blob = get_user_photo(access_token) if access_token else None
        except Exception as e:
            photo_blob = None
            logger.error(f"Erro ao buscar a foto do usuário: {e}")

        if photo_blob:
            upload_images_to_cloudinary.delay(user.id, [photo_blob], object_type="user")

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
    auth_url = app.get_authorization_request_url(scopes=SCOPES, redirect_uri=REDIRECT_URI)
    return redirect(auth_url)


def microsoft_callback(request):
    """
    Processa o callback da Microsoft após o login.
    """
    authorization_code = request.GET.get("code")
    if not authorization_code:
        logger.error("Código de autorização não fornecido.")
        return JsonResponse({"error": "Código de autorização não fornecido."}, status=400)

    app = ConfidentialClientApplication(
        client_id=CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY
    )

    try:
        token_response = app.acquire_token_by_authorization_code(
            code=authorization_code, scopes=SCOPES, redirect_uri=REDIRECT_URI
        )
        if "access_token" in token_response:
            access_token = token_response["access_token"]

            user_data = fetch_user_data(access_token)

            user, created = save_or_update_user(user_data=user_data, access_token=access_token)

            login(request, user)

            refresh = RefreshToken.for_user(user)
            jwt_access = str(refresh.access_token)
            str(refresh)

            response = HttpResponseRedirect("https://acheiunb.com.br/#/found")
            response.set_cookie(
                key="access_token",
                value=jwt_access,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=3600,
            )
            return response
        else:
            logger.error("Falha ao adquirir token de acesso.")
            return JsonResponse({"error": "Falha ao adquirir token de acesso."}, status=400)
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
        data = request.data

        try:
            user, created = User.objects.update_or_create(
                email=data.get("email"),
                defaults={
                    "username": data.get("username"),
                    "first_name": data.get("first_name"),
                    "last_name": data.get("last_name"),
                    "password": data.get("password", ""),
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
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        return response.content
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
            user.delete()
            return JsonResponse(
                {"message": f"Usuário com ID {user_id} foi deletado com sucesso."},
                status=200,
            )
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuário não encontrado."}, status=404)
