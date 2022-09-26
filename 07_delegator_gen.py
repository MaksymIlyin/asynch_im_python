
def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class BlaBlaException(Exception):
    pass

def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            # print("ERROR!!!")
            break
        else:
            print(".........", message)

    return "Returned from subgen()"

@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except BlaBlaException as e:
    #         g.throw(e)
    #     else:
    #         pass
    result = yield from g
    print(result)
