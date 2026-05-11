import re
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from .merge_sort import merge_sort


@dataclass(frozen=True)
class RankedMatch:
    """Representa um candidato de match junto com sua pontuação."""
    item: Any
    score: float


def normalize_text(text: str | None) -> str:
    """Normaliza texto para comparação, removendo acentos e pontuação."""
    if not text:
        return ""

    normalized = text.lower()
    normalized = unicodedata.normalize("NFD", normalized)
    normalized = "".join(
        character for character in normalized if unicodedata.category(character) != "Mn"
    )
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def tokenize(text: str | None) -> set[str]:
    """Transforma um texto em um conjunto de palavras normalizadas."""
    normalized = normalize_text(text)

    if not normalized:
        return set()

    return set(normalized.split())


def text_similarity(first_text: str | None, second_text: str | None) -> float:
    """
    Calcula similaridade textual usando índice de Jaccard.

    O resultado varia entre 0 e 1:
    - 0: nenhuma palavra em comum;
    - 1: os conjuntos de palavras são iguais.
    """
    first_tokens = tokenize(first_text)
    second_tokens = tokenize(second_text)

    if not first_tokens or not second_tokens:
        return 0.0

    intersection = first_tokens.intersection(second_tokens)
    union = first_tokens.union(second_tokens)

    return len(intersection) / len(union)


def date_similarity(first_date: Any, second_date: Any, max_days: int = 30) -> float:
    """
    Calcula proximidade entre as datas.

    Quanto menor a diferença entre as datas, maior a pontuação,
    sendo que diferenças iguais ou maiores que max_days recebem 0.
    """
    parsed_first_date = _parse_date(first_date)
    parsed_second_date = _parse_date(second_date)

    if not parsed_first_date or not parsed_second_date:
        return 0.0

    days_difference = abs((parsed_first_date - parsed_second_date).days)

    if days_difference >= max_days:
        return 0.0

    return 1 - (days_difference / max_days)


def calculate_similarity_score(target_item: Any, candidate_item: Any) -> float:
    """
    Calcula score de similaridade entre item alvo e candidato.

    A pontuação final vai de 0 a 100. Os pesos escolhidos priorizam o nome do
    item, a descrição, a cor e a marca, e por fim, a proximidade entre datas.
    """
    name_score = text_similarity(
        _get_attribute(target_item, "name"),
        _get_attribute(candidate_item, "name"),
    )
    description_score = text_similarity(
        _get_attribute(target_item, "description"),
        _get_attribute(candidate_item, "description"),
    )
    color_score = categorical_similarity(
        target_item,
        candidate_item,
        "color"
    )
    brand_score = categorical_similarity(
        target_item,
        candidate_item,
        "brand"
    )
    date_score = date_similarity(
        _get_attribute(target_item, "found_lost_date"),
        _get_attribute(candidate_item, "found_lost_date"),
    )

    final_score = (
        (name_score * 0.40)
        + (description_score * 0.25)
        + (color_score * 0.15)
        + (brand_score * 0.15)
        + (date_score * 0.05)
    )

    return round(final_score * 100, 2)


def _get_attribute(item: Any, attribute_name: str) -> Any:
    """Lê atributo de objetos ou dicionários."""
    if isinstance(item, dict):
        return item.get(attribute_name)

    return getattr(item, attribute_name, None)


def _get_named_attribute(item: Any, attribute_name: str) -> str:
    """Lê atributos com opções de escolha como cor e marca."""
    value = _get_attribute(item, attribute_name)

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if hasattr(value, "name"):
        return str(value.name)

    return str(value)


def categorical_similarity(
    target_item: Any, candidate_item: Any, attribute_name: str
) -> float:
    """Compara atributos categóricos como cor e marca, retornando 1 para correspondência exata e 0 caso contrário."""
    target_value = _get_named_attribute(target_item, attribute_name)
    candidate_value = _get_named_attribute(candidate_item, attribute_name)

    if not target_value or not candidate_value:
        return 0.0

    return 1.0 if normalize_text(target_value) == normalize_text(candidate_value) else 0.0


def _parse_date(value: Any) -> date | None:
    """Extrai a data de um datetime e retorna None para valores ausentes."""
    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date()

    return None


def rank_match_candidates(
    target_item: Any,
    candidates: list[Any],
    min_score: float = 36,
) -> list[RankedMatch]:
    """
    Calcula o score de cada candidato e ordena usando Merge Sort.

    Args:
        target_item: item perdido/encontrado usado como referência.
        candidates: lista de possíveis matches já filtrados por status, categoria e local.
        min_score: pontuação mínima para manter um candidato como um match.

    Returns:
        Lista de RankedMatch em ordem decrescente de score.
    """
    ranked_matches = []

    for candidate in candidates:
        score = calculate_similarity_score(target_item, candidate)

        if score >= min_score:
            ranked_matches.append(RankedMatch(item=candidate, score=score))

    return merge_sort(ranked_matches, key=lambda match: match.score, reverse=True)


def get_ranked_items(
    target_item: Any,
    candidates: list[Any],
    min_score: float = 36,
) -> list[Any]:
    """Retorna apenas os matches, já ordenados por similaridade."""
    ranked_matches = rank_match_candidates(target_item, candidates, min_score=min_score)

    return [ranked_match.item for ranked_match in ranked_matches]
