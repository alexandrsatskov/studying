"""Дебажу принтами и пытаюсь понять как же отрабатывает yield,
который одновременно и принимает данные, и выбрасывает их наружу
"""


class MyEx(Exception):
    pass


def coroutine_init(func):
    def inner(*args, **kwargs):
        generator = func(*args, **kwargs)
        generator.send(None)
        return generator
    return inner


@coroutine_init
def average():
    count = sum_ = 0
    avg_ = None

    while True:
        try:
            print('Try before yield')
            x = yield avg_
            print('Try after yield')
        except StopIteration:
            print('StopIteration')
            break
        except MyEx:
            print('MyEx')
            break
        else:
            print('Else')
            count += 1
            sum_ += x
            avg_ = round(sum_ / count, 2)


g = average()
# Без синтаксического сахара, еле разобрался
# Вот так уже не работает: coroutine(average())()
# и так тоже coroutine(average),
# и так... coroutine(average())
# g = coroutine(average)()
