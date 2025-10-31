import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User, UserProfile

@pytest.mark.django_db
class TestUserProfileViewMC_DC:
    """
    Suite de testes MC/DC para o método get() da UserProfileView.
    """

    def setup_method(self):
        """
        Configura os usuários necessários para os 6 cenários de teste.
        """
        self.client = APIClient()
        # Usuário 1: Banido (para CT1, CT3)
        self.user_banned = User.objects.create_user(username="usuario_banido", email="banned@unb.br")
        profile_banned = UserProfile.objects.get(user=self.user_banned)
        profile_banned.is_banned = True
        profile_banned.save()

        # Usuário 2: Ativo (para CT2 e CT4-CT6)
        self.user_active = User.objects.create_user(
            username="usuario_ativo",
            email="active@unb.br",
            first_name="NomeAtivo",
            last_name="SobrenomeAtivo"
        )
        
        # Usuário 3: Visitante (para CT1, CT2)
        self.user_visitor = User.objects.create_user(username="visitante", email="visitor@unb.br")

        self.url_banned = reverse('user-profile', args=[self.user_banned.id])
        self.url_active = reverse('user-profile', args=[self.user_active.id])

    # --- Testes para Decisão D1 (Controle de Acesso de Banido) ---

    def test_ct1_visualizar_perfil_banido_como_outro_usuario(self):
        """
        CT1 (MC/DC Linha 4: C1=V, C2=V)
        Testa visualizar um usuário BANIDO (C1=V) como OUTRO usuário (C2=V).
        Resultado D1 = V (JSON Limitado).
        """
        self.client.force_authenticate(user=self.user_visitor)
        response = self.client.get(self.url_banned)
        
        assert response.status_code == 200
        assert response.json()["username"] == "Usuário indisponível"

    def test_ct2_visualizar_perfil_ativo_como_outro_usuario(self):
        """
        CT2 (MC/DC Linha 2: C1=F, C2=V)
        Testa visualizar um usuário ATIVO (C1=F) como OUTRO usuário (C2=V).
        Resultado D1 = F (JSON Completo).
        """
        self.client.force_authenticate(user=self.user_visitor)
        response = self.client.get(self.url_active)
        
        assert response.status_code == 200
        assert response.json()["username"] == "usuario_ativo"

    def test_ct3_visualizar_perfil_banido_como_o_proprio_dono(self):
        """
        CT3 (MC/DC Linha 3: C1=V, C2=F)
        Testa visualizar um usuário BANIDO (C1=V) como ELE MESMO (C2=F).
        Resultado D1 = F (JSON Completo).
        """
        self.client.force_authenticate(user=self.user_banned)
        response = self.client.get(self.url_banned)
        
        assert response.status_code == 200
        assert response.json()["username"] == "usuario_banido"

    # --- Testes para Decisão D2 (Formatação de Nome) ---

    def test_ct4_formatar_nome_primeiro_vazio_sobrenome_preenchido(self):
        """
        CT4 (MC/DC Linha 8: C3=V, C4=V)
        Testa nome: first_name VAZIO (C3=V), last_name PREENCHIDO (C4=V).
        Resultado D2 = V (Usa last_name no first_name, last_name fica vazio).
        """
        self.user_active.first_name = ""
        self.user_active.last_name = "Silva"
        self.user_active.save()
        
        self.client.force_authenticate(user=self.user_active)
        response = self.client.get(self.url_active)
        
        assert response.status_code == 200
        assert response.json()["first_name"] == "Silva"
        assert response.json()["last_name"] == ""

    def test_ct5_formatar_nome_primeiro_preenchido_sobrenome_preenchido(self):
        """
        CT5 (MC/DC Linha 6: C3=F, C4=V)
        Testa nome: first_name PREENCHIDO (C3=F), last_name PREENCHIDO (C4=V).
        Resultado D2 = F (Nomes permanecem inalterados).
        """
        self.user_active.first_name = "Brunno"
        self.user_active.last_name = "Fernandes"
        self.user_active.save()
        
        self.client.force_authenticate(user=self.user_active)
        response = self.client.get(self.url_active)
        
        assert response.status_code == 200
        assert response.json()["first_name"] == "Brunno"
        assert response.json()["last_name"] == "Fernandes"

    def test_ct6_formatar_nome_primeiro_vazio_sobrenome_vazio(self):
        """
        CT6 (MC/DC Linha 7: C3=V, C4=F)
        Testa nome: first_name VAZIO (C3=V), last_name VAZIO (C4=F).
        Resultado D2 = F (Usa username no first_name, last_name fica vazio).
        """
        self.user_active.first_name = ""
        self.user_active.last_name = ""
        self.user_active.save()
        
        self.client.force_authenticate(user=self.user_active)
        response = self.client.get(self.url_active)
        
        assert response.status_code == 200
        assert response.json()["first_name"] == "usuario_ativo"
        assert response.json()["last_name"] == ""