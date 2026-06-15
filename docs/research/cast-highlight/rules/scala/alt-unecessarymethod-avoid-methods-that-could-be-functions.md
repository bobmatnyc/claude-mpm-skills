---
title: Methods as functions tend to be unproductive
url: https://doc.casthighlight.com/alt_unecessarymethod-avoid-methods-that-could-be-functions/
slug: alt_unecessarymethod-avoid-methods-that-could-be-functions
content_type: rule
languages: [scala, python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Methods as functions tend to be unproductive**

This code insight counts one violation each time a method :

- has **no @staticmethod** decorator and **no “self”** as first argument
- has **@classmethod** decorator and **no “cls”** as first argument

class Rectangle:

```
    # should be preceded by @staticmethod here
    def area(width, height):
        return width * height
```

```
class Rectangle:
    # should be preceded by @classmethod here
    # missing required first argument "cls"
    def print_class_name():
        print("class name: Rectangle")
```

**good**

```
class Rectangle:
    # clarifies that this is a static method and belongs here
    @staticmethod
    def area(width, height):
        return width * height
```

```
class Rectangle:
    @classmethod
    def print_class_name(cls):
        # "class name: Rectangle"
        print("class name: {0}".format(cls))
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

When a method is not preceded by the `@staticmethod` or `@classmethod` decorators and does not contain any references to the class or instance (via keywords like `cls` or `self`), Python raises the “`Method could be a function"` error. This is not a critical error, but you should check the code in question in order to determine if this section of code really needs to be defined as a method of this class.

Unlike some programming languages, Python does not pass references to instance or class objects automatically behind the scenes. So the program must explicitly pass them as arguments whenever it wants to access any members of the instance or class within a method

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://docs.quantifiedcode.com/python-code-patterns/correctness/method\_could\_be\_a\_function.html

https://www.quantifiedcode.com/knowledge-base/correctness/Provide%20argument%20or%20%60%40staticmethod%60%20to%20method/3bECxdfc

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
