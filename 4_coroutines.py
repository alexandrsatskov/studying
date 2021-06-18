def coroutine_init(func):
    def inner(*args, **kwargs):
        generator = func(*args, **kwargs)
        generator.send(None)
        return generator
    return inner


def sub_generator():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print(f'Entered message: {message}')
    return 'sub_generator() return statement'


@coroutine_init
def delegate_generator(generator):
    # while True:
    #     try:
    #         data = yield
    #         generator.send(data)
    #     except StopIteration as e:
    #         generator.throw(e)
    #         break
    #     else:
    #         print(f'Entered message: {message}')
    # yield from заменяет нам все вышеперечисленное
    result = yield from generator
    print(result)
