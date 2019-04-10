#!/usr/bin/env python

import unittest
from base import InheritanceError, StrictParent, final, overrides, force_override


class Parent(StrictParent):

    def overrideable_method(self):
        return 'I do not mind being overridden'

    @final
    def final_method(self):
        return 'Knowledge & vision arose in me: this is the last birth. There is now no further becoming.'


class StrictParentTest(unittest.TestCase):

    def test_obedient_child(self):
        try:
            class ObedientChild(Parent):

                @overrides
                def overrideable_method(self):
                    return 'Hey'

                @force_override
                def final_method(self):
                    return 'I am aware I have broken the convention'
        except Exception as e:
            self.fail(e)

    def test_invalid_override(self):
        with self.assertRaisesRegex(InheritanceError,
                                    'Method my_heretic_method of RebelChild claims to override a parent class method, '
                                    'but no parent class method with that name were found.'):
            class RebelChild(Parent):

                @overrides  # Will raise exception, because `Parent` class has no such method
                def my_heretic_method(self):
                    return 'I claim to be be authentic, but I am just a faker'

    def test_missing_override(self):
        with self.assertRaisesRegex(InheritanceError,
                                    'Method overrideable_method of RebelChild is '
                                    'overriding a parent class method, but does not have `@overrides` decorator.'):
            class RebelChild(Parent):

                def overrideable_method(self):
                    return 'I claim to be be authentic, but I am just a faker'

    def test_final_violation(self):
        with self.assertRaisesRegex(InheritanceError,
                                    r'Method `<function Parent.final_method at 0x\w+>` is finalized in `Parent`. '
                                    r'You cannot override it unless you decorate it with `@force_override`.'):
            class RebelChild(Parent):

                @overrides
                # Will raise exception, because `final_method` has been finalized in `Parent` class
                def final_method(self):
                    return 'I am against the machine!'


if __name__ == '__main__':
    unittest.main()
