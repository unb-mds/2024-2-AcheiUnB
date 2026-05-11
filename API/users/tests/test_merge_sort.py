from users.merge_sort import merge_sort


def test_ordena_scores_em_ordem_decrescente():
    """Ordena os scores em ordem decrescente."""
    candidates = [
        {"id": 1, "score": 72},
        {"id": 2, "score": 95},
        {"id": 3, "score": 40},
        {"id": 4, "score": 88},
    ]

    result = merge_sort(candidates, key=lambda candidate: candidate["score"], reverse=True)

    assert [candidate["id"] for candidate in result] == [2, 4, 1, 3]


def test_mantem_estabilidade_para_scores_empatados():
    """Mantém a estabilidade para scores empatados."""
    candidates = [
        {"id": 1, "score": 80},
        {"id": 2, "score": 90},
        {"id": 3, "score": 80},
        {"id": 4, "score": 70},
    ]

    result = merge_sort(candidates, key=lambda candidate: candidate["score"], reverse=True)

    assert [candidate["id"] for candidate in result] == [2, 1, 3, 4]


def test_lista_vazia():
    """Funciona corretamente quando a lista é vazia."""
    assert merge_sort([], reverse=True) == []


def test_lista_com_unico_elemento():
    """Funciona corretamente quando há um único score."""
    candidates = [{"id": 1, "score": 100}]

    result = merge_sort(candidates, key=lambda candidate: candidate["score"], reverse=True)

    assert result == candidates
