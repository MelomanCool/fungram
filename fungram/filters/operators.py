def f_and(a, b, *preds):
    def inner(*args, **kwargs):
        return all(pred(*args, **kwargs) for pred in (a, b, *preds))

    return inner


def f_or(a, b, *preds):
    def inner(*args, **kwargs):
        return any(pred(*args, **kwargs) for pred in (a, b, *preds))

    return inner


def f_not(pred):
    def inner(*args, **kwargs):
        return not pred(*args, **kwargs)

    return inner
