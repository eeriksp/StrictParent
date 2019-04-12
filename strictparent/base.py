# Three underscores to avoid potential conflicts with Python's own features
FINALIZED = '___finalized___'
OVERRIDES = '___overrides___'
FORCE_OVERRIDE = '___force_override___'


class EmptyClass:
    # TODO Perhaps it should be an empty ABC class,
    # because ABCMeta adds its own features.
    pass


class InheritanceError(AssertionError):
    pass


class Data:
    def __init__(self):
        raise TypeError(
            'Do not instantiate this class, it is just a container for data.')
    finalized = set()
    overrides = set()
    force_override = set()





def final(obj):
    Data.finalized.add(obj)
    return obj


def overrides(obj):
    Data.overrides.add(obj)
    return obj


def force_override(obj):
    Data.force_override.add(obj)
    return obj


class StrictParent:
    def __init_subclass__(cls):
        cls_name = cls.__name__
        bases = cls.__bases__
        namespace = cls.__dict__

        # Check if `@overrides` are valid
        sum_of_base_dicts = {}
        for base in bases:
            sum_of_base_dicts.update(base.__dict__)

        all_base_class_member_names = {name for name in sum_of_base_dicts}

        functions = {name: value for (name, value) in namespace.items()
                     if callable(value) or isinstance(value, (staticmethod, classmethod, property))}
        for name, value in functions.items():
            if value in Data.overrides or value in Data.force_override:
                for base in bases:
                    if getattr(base, name, False):
                        break
                else:
                    raise InheritanceError(f'`{name}` of {cls_name} claims to '
                                           'override a parent class method, but no parent class method with that name were found.')
            else:
                # TODO We now exclude all built-in method including `__str__`.
                # Should be so that if they are overridden in parent class (not equal to object.this_method),
                # then they should be taken into account.
                if name in all_base_class_member_names and name not in EmptyClass.__dict__:
                    raise InheritanceError(f'`{name}` of {cls_name} is '
                                           'overriding a parent class method, but does not have `@overrides` decorator.')

        # Check `@final` violations
        for name, value in functions.items():
            if value not in Data.force_override:
                for base in bases:
                    base_class_method = getattr(base, name, False)
                    if not base_class_method:
                        # i.e. this method does not exist in the base class
                        continue
                    if base_class_method in Data.finalized:
                        raise InheritanceError(
                            f'`{base_class_method.__name__}` is finalized in `{base.__name__}`. '
                            'You cannot override it unless you decorate it with `@force_override`.')
