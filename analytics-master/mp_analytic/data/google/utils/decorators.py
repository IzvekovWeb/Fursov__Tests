import copy


def check_instance(func):
    def inner(*args, **kwargs):
        annotations = copy.deepcopy(func.__annotations__)
        args_ = copy.deepcopy(args)
        kwargs_ = copy.deepcopy(kwargs)

        if 'return' in annotations:
            annotations.pop('return')

        parametrs = list(annotations.keys())

        if len(args_) > 0:
            if hasattr(args_[0], '__dict__'):
                args_ = args_[1:]

            for i, item in enumerate(args_):
                annotation = annotations.pop(parametrs[i])
                if not isinstance(item, annotation):
                    print(f"----TypeError---{item}")
                    print(func)
                    print(annotation)
                    raise TypeError

        if len(kwargs_) > 0:
            for item in annotations:
                if item not in kwargs_.keys():
                    continue
                if not isinstance(kwargs_[item], annotations[item]):
                    print(f"-----TypeError---{kwargs_[item]}")
                    raise TypeError

        return func(*args, **kwargs)
    return inner
