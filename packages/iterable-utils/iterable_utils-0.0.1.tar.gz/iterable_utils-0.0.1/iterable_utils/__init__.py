from itertools import islice


def chunk(iterable, size):
    iterable = iter(iterable)
    return iter(lambda: list(islice(iterable, size)), [])


def split(iterable, index):
    if index >= len(iterable):
        return iterable, index
    return iterable[:index], iterable[index:]
