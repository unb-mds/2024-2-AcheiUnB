from datetime import datetime

from users.match_ranking import (
    calculate_similarity_score,
    categorical_similarity,
    date_similarity,
    get_ranked_items,
    normalize_text,
    rank_match_candidates,
    text_similarity,
)


def test_normaliza_texto_removendo_acentos_e_pontuacao():
    """Remove acentos e pontuação, e converte para minúsculas."""
    assert normalize_text("Fône Bluetooth, PRÉTO!") == "fone bluetooth preto"


def test_similaridade_textual_parcial():
    """Retorna um valor entre 0 e 1, onde 1 é texto idêntico e 0 é completamente diferente."""
    score = text_similarity("fone bluetooth preto", "fone preto sem fio")

    assert 0 < score < 1


def test_cor_e_marca_iguais():
    """Retorna 1 para cor e/ou marca iguais."""
    target = {
        "color": "Preto",
        "brand": "JBL",
    }
    candidate = {
        "color": "Preto",
        "brand": "JBL",
    }

    assert categorical_similarity(target, candidate, "color") == 1.0
    assert categorical_similarity(target, candidate, "brand") == 1.0


def test_cor_e_marca_diferentes():
    """Retorna 0 para cor e/ou marca diferentes."""
    target = {
        "color": "Preto",
        "brand": "JBL",
    }
    candidate = {
        "color": "Branco",
        "brand": "Samsung",
    }

    assert categorical_similarity(target, candidate, "color") == 0.0
    assert categorical_similarity(target, candidate, "brand") == 0.0


def test_datas_proximas_tem_score_maior():
    """Compara as datas e retorna maior score para datas mais próximas."""
    target_date = datetime(2026, 4, 10, 10, 30)
    close_date = datetime(2026, 4, 11, 14, 0)
    far_date = datetime(2026, 5, 20, 14, 0)

    close_score = date_similarity(target_date, close_date)
    far_score = date_similarity(target_date, far_date)

    assert close_score > far_score
    assert far_score == 0.0


def test_candidato_mais_parecido_tem_score_maior():
    """Demonstra que o candidato mais parecido deve ter score maior que candidato menos parecido."""
    target = {
        "name": "Fone bluetooth preto",
        "description": "Fone sem fio com estojo oval e borrachas pequenas.",
        "color": "Preto",
        "brand": "JBL",
        "found_lost_date": datetime(2026, 4, 10, 10, 0),
    }

    similar_candidate = {
        "name": "Fone bluetooth preto",
        "description": "Fone sem fio com estojo oval e borrachas pequenas.",
        "color": "Preto",
        "brand": "JBL",
        "found_lost_date": datetime(2026, 4, 11, 10, 0),
    }

    weak_candidate = {
        "name": "Carregador de notebook",
        "description": "Carregador com cabo grosso e conector redondo.",
        "color": "Branco",
        "brand": "Dell",
        "found_lost_date": datetime(2026, 4, 11, 10, 0),
    }

    similar_score = calculate_similarity_score(target, similar_candidate)
    weak_score = calculate_similarity_score(target, weak_candidate)

    assert similar_score > weak_score


def test_ordena_candidatos_por_score_decrescente():
    """Ordena os candidatos por score decrescente."""
    target = {
        "name": "Fone bluetooth preto",
        "description": "Fone sem fio com estojo oval e borrachas pequenas.",
        "color": "Preto",
        "brand": "JBL",
        "found_lost_date": datetime(2026, 4, 10, 10, 0),
    }

    candidates = [
        {
            "id": 1,
            "name": "Carregador de notebook",
            "description": "Carregador com cabo grosso e conector redondo.",
            "color": "Branco",
            "brand": "Dell",
            "found_lost_date": datetime(2026, 4, 10, 10, 0),
        },
        {
            "id": 2,
            "name": "Fone bluetooth preto",
            "description": "Fone sem fio com estojo oval e borrachas pequenas.",
            "color": "Preto",
            "brand": "JBL",
            "found_lost_date": datetime(2026, 4, 11, 10, 0),
        },
        {
            "id": 3,
            "name": "Fone preto",
            "description": "Fone com estojo oval preto e borrachas pequenas.",
            "color": "Preto",
            "brand": "Sony",
            "found_lost_date": datetime(2026, 4, 12, 10, 0),
        },
    ]

    result = rank_match_candidates(target, candidates, min_score=0)

    assert [ranked_match.item["id"] for ranked_match in result] == [2, 3, 1]
    assert result[0].score >= result[1].score >= result[2].score


def test_filtra_candidatos_abaixo_do_score_minimo():
    """Filtra candidatos com score abaixo do mínimo (36) e ordena os restantes por score decrescente."""
    target = {
        "name": "Fone bluetooth preto",
        "description": "Fone sem fio com estojo oval e borrachas pequenas.",
        "color": "Preto",
        "brand": "JBL",
        "found_lost_date": datetime(2026, 4, 10, 10, 0),
    }

    candidates = [
        {
            "id": 1,
            "name": "Fone bluetooth preto",
            "description": "Fone sem fio com estojo oval e borrachas pequenas.",
            "color": "Preto",
            "brand": "JBL",
            "found_lost_date": datetime(2026, 4, 11, 10, 0),
        },
        {
            "id": 2,
            "name": "Garrafa azul",
            "description": "Garrafa térmica com tampa rosqueável e alça lateral.",
            "color": "Azul",
            "brand": "Stanley",
            "found_lost_date": datetime(2026, 4, 25, 10, 0),
        },
    ]

    result = rank_match_candidates(target, candidates)

    assert [ranked_match.item["id"] for ranked_match in result] == [1]
    assert all(ranked_match.score >= 36 for ranked_match in result)


def test_retorna_apenas_items_ordenados():
    """Retorna apenas os matches ordenados (mais provável para o menos provável) a serem enviados para o usuário."""
    target = {
        "name": "Fone bluetooth preto",
        "description": "Fone sem fio com estojo oval e borrachas pequenas.",
        "color": "Preto",
        "brand": "JBL",
        "found_lost_date": datetime(2026, 4, 10, 10, 0),
    }

    candidates = [
        {
            "id": 1,
            "name": "Mouse vermelho",
            "description": "Mouse com botão lateral e roda de rolagem.",
            "color": "Vermelho",
            "brand": "Logitech",
            "found_lost_date": datetime(2026, 4, 12, 10, 0),
        },
        {
            "id": 2,
            "name": "Fone bluetooth preto",
            "description": "Fone sem fio com estojo oval e borrachas pequenas.",
            "color": "Preto",
            "brand": "JBL",
            "found_lost_date": datetime(2026, 4, 11, 10, 0),
        },
    ]

    result = get_ranked_items(target, candidates)

    assert [item["id"] for item in result] == [2]
