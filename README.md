# StrictParent

Python is built to be as dynamic and permissive as possible. However, especially in case of bigger applications it is beneficial to establish some stricter principles. StrictParent helps you to make your Python classes more strict while still leaving the opportunity to break the rules if necessary.

## Features

 * `StrictParent` -- parent class for all your custom classes using these functionalities
 * `@final` -- decorator for methods, raises exception id subclasses try to override this method
 * `@overrides` -- decorator for methods, states that this subclass method is overriding a method in subclass. If parent class does not have such a method, raises exception. If parent class makes this method finalized (by adding `@final` decorator), subclass can still override it by passing `force=True` to the `@overrides` decorator. The developer is thus protected against accidentally overriding a finalized method, but can still do it, if they know what they are doing.

Since you might need to use these functionalities together with ABC classes, `StrictParent`'s metaclass inherits from ABCMeta to prevent metaclass conflict. This means that once you inherit from `StrictParent`, you can use all the features of ABC as well.
```py
from strictparent import StrictParent, final, overrides
from abc import abstractmethod


class Parent(StrictParent):

    def overrideable_method(self):
        return 'I do not mind being overridden'

    @final
    def final_method(self):
        return 'Knowledge & vision arose in me: this is the last birth. There is now no further becoming.'

    @abstractmethod  # You can use all the ABC features here
    def abstract_method(self):
        pass


class ObedientChild(Parent):

    @overrides  # It is now easy to see, that the metod has a meaning in the Parent class
    def overrideable_method(self):
        return 'Hey'

    @overrides(force=True)  # Finalized methods can be overridden if explicidly stated
    def final_method(self):
        return 'I am aware I have broken the convention'

    @overrides
    def abstract_method(self):
        return 'Not abstract any more'


class RebelChild(Parent):

    @overrides  # Will raise exception, because Parent class has no such method
    def my_heretic_method(self):
        return 'I claim to be be authentic, but I am just a faker'

    def final_method(self):  # Will raise exception, because `final_method` has been finalized in `Parent` class
        return 'Knowledge & vision arose in me: this is the last birth. There is now no further becoming.'

```
