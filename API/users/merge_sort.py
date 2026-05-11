from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def merge_sort(
    values: Sequence[T],
    key: Callable[[T], object] = lambda value: value,
    reverse: bool = False,
) -> list[T]:
    """
    Ordena uma sequência utilizando Merge Sort.

    A implementação é estável: quando dois elementos possuem a mesma chave,
    o elemento que apareceu primeiro na lista original continua vindo primeiro
    no resultado.

    Args:
        values: sequência de scores de similaridade a ser ordenada.
        key: função que extrai a chave de ordenação de cada valor.
        reverse: quando True, ordena em ordem decrescente.

    Returns:
        Nova lista ordenada.
    """
    values = list(values)

    if len(values) <= 1:
        return values

    middle = len(values) // 2
    left = merge_sort(values[:middle], key=key, reverse=reverse)
    right = merge_sort(values[middle:], key=key, reverse=reverse)

    return _merge(left, right, key, reverse)


def _merge(
    left: list[T],
    right: list[T],
    key: Callable[[T], object],
    reverse: bool,
) -> list[T]:
    """Intercala duas listas que já estão ordenadas."""
    result: list[T] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        left_key = key(left[i])
        right_key = key(right[j])

        if _comes_before_or_ties(left_key, right_key, reverse):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def _comes_before_or_ties(left_key: object, right_key: object, reverse: bool) -> bool:
    """
    Decide se a chave da esquerda deve vir antes da chave da direita.

    O empate retorna True para preservar estabilidade do Merge Sort.
    """
    if reverse:
        return left_key >= right_key

    return left_key <= right_key
