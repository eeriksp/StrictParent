#!/usr/bin/env python

import unittest
from base import InheritanceError, StrictParent, final, overrides, force_override


class Parent(StrictParent):
    field = 42

    class InlineClass:
        foo = 5

    @final
    class FinalInlineClass:
        bar = 7

    def overrideable_method(self):
        return 'I do not mind being overridden'

    def another_overrideable_method(self, foo: int = 8):
        return 'Hey'

    @final
    def final_method(self):
        return 'Knowledge & vision arose in me: this is the last birth. There is now no further becoming.'


class StrictParentTest(unittest.TestCase):

    def test_obedient_child(self):
        try:
            class ObedientChild(Parent):
                field = 55

                @overrides
                class InlineClass:
                    foo = 5

                @overrides
                def overrideable_method(self):
                    return 'Hey'

                @force_override
                def final_method(self):
                    return 'I am aware I have broken the convention'

                def my_own_method(self):
                    pass

        except Exception as e:
            self.fail(e)

    def test_invalid_override(self):
        with self.assertRaisesRegex(InheritanceError,
                                    '`my_heretic_method` of RebelChild claims to override a parent class method, '
                                    'but no parent class method with that name were found.'):
            class RebelChild(Parent):

                @overrides  # Will raise exception, because `Parent` class has no such method
                def my_heretic_method(self):
                    return 'I claim to be be authentic, but I am just a faker'

    def test_missing_override(self):
        with self.assertRaisesRegex(InheritanceError,
                                    '`overrideable_method` of RebelChild is '
                                    'overriding a parent class method, but does not have `@overrides` decorator.'):
            class RebelChild(Parent):

                def overrideable_method(self):
                    return 'I claim to be be authentic, but I am just a faker'

        with self.assertRaisesRegex(InheritanceError,
                                    '`InlineClass` of RebelChild is '
                                    'overriding a parent class method, but does not have `@overrides` decorator.'):
            class RebelChild(Parent):

                class InlineClass:
                    pass

    def test_final_violation(self):
        with self.assertRaisesRegex(InheritanceError,
                                    r'`final_method` is finalized in `Parent`. '
                                    r'You cannot override it unless you decorate it with `@force_override`.'):
            class RebelChild(Parent):

                @overrides
                # Will raise exception, because `final_method` has been finalized in `Parent` class
                def final_method(self):
                    return 'I am against the machine!'

        with self.assertRaisesRegex(InheritanceError,
                                    r'`FinalInlineClass` is finalized in `Parent`. '
                                    r'You cannot override it unless you decorate it with `@force_override`.'):
            class RebelChild(Parent):

                @overrides
                class FinalInlineClass:
                    pass

    def test_together_with_staticmethod_and_classmethod(self):
        try:
            class Child(Parent):
                @final
                @overrides
                @staticmethod
                def overrideable_method(self):
                    pass

                @final
                @overrides
                @classmethod
                def another_overrideable_method(self):
                    pass
        except Exception as e:
            self.fail(e)
        with self.assertRaisesRegex(InheritanceError,
                                    '`overrideable_method` of Child is '
                                    'overriding a parent class method, but does not have `@overrides` decorator.'):
            class Child(Parent):
                @staticmethod
                def overrideable_method(self):
                    pass

    def test_together_with_property(self):
        try:
            class Child(Parent):
                @overrides
                @property
                def overrideable_method(self):
                    return 'Foo'
            # We add a wrapper around the property, make sure this does not break the property interface
            self.assertEqual(Child.overrideable_method, 'Foo')
        except Exception as e:
            self.fail(e)
        with self.assertRaisesRegex(InheritanceError,
                                    '`overrideable_method` of Child is '
                                    'overriding a parent class method, but does not have `@overrides` decorator.'):
            class Child(Parent):
                @property
                def overrideable_method(self):
                    pass
    # TODO add tests for objects with slots, they should function just as properties


if __name__ == '__main__':
    unittest.main()
