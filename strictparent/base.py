import re


class InheritanceError(AssertionError):
    pass


class DecoratorRegistry:
    def __init__(self):
        raise TypeError(
            'Do not instantiate this class, it is just a container for data.')
    finalized = set()
    overrides = set()
    force_override = set()


def final(obj):
    DecoratorRegistry.finalized.add(obj)
    return obj


def overrides(obj):
    DecoratorRegistry.overrides.add(obj)
    return obj


def force_override(obj):
    DecoratorRegistry.force_override.add(obj)
    return obj


class StrictParent:
    def __init_subclass__(cls):
        bases = cls.__mro__[1:]  # `__mro__` also containes the class itself, exclude it
        functions = {unmangle(name): value for (name, value) in cls.__dict__.items()
                     if callable(value) or isinstance(value, (staticmethod, classmethod, property))}
        for name, value in functions.items():
            _check_override_violations(name, value, bases, cls.__name__)
            _check_final_violations(name, value, bases)


def _check_final_violations(name, value, bases):
    if value in DecoratorRegistry.force_override:
        return
    for base in bases:
        base_class_method = get_unmangled_attr(base, name)
        if not base_class_method:
            # i.e. this method does not exist in the base class
            continue
        if base_class_method in DecoratorRegistry.finalized:
            raise InheritanceError(
                f'`{base_class_method.__name__}` is finalized in `{base.__name__}`. '
                'You cannot override it unless you decorate it with `@force_override`.')


def _check_override_violations(name, value, bases, cls_name):
    if value in DecoratorRegistry.overrides or value in DecoratorRegistry.force_override:
        for base in bases:
            if get_unmangled_attr(base, name):
                break
        else:
            raise InheritanceError(f'`{unmangle(name)}` of {cls_name} claims to '
                                   'override a parent class method, but no parent class method with that name were found.')
    else:
        for base in bases:
            if unmangle(name) in _get_all_base_classes_member_names(bases):
                raise InheritanceError(f'`{unmangle(name)}` of {cls_name} is '
                                       'overriding a parent class method, but does not have `@overrides` decorator.')


def _get_all_base_classes_member_names(bases: tuple) -> set:
    sum_of_base_dicts = {}
    for base in bases:
        sum_of_base_dicts.update(base.__dict__)

    return {name for name in sum_of_base_dicts}


MANGLE_RE = re.compile(r'_.+?(__.+)')


def get_unmangled_attr(obj, name):
    for _name, value in obj.__dict__.items():
        if unmangle(_name) == name:
            return value
    return False


def unmangle(name):
    match = MANGLE_RE.match(name)
    if not match:
        return name
    return match.group(1)
