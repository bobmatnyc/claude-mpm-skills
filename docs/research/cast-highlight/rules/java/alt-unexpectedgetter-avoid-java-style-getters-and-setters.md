---
title: Java-Style getters and setters can increase production risks
url: https://doc.casthighlight.com/alt_unexpectedgetter-avoid-java-style-getters-and-setters/
slug: alt_unexpectedgetter-avoid-java-style-getters-and-setters
content_type: rule
languages: [java, scala, python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Java-Style getters and setters can increase production risks

This code insight counts one violation each time a class define getter or setter (one of then or both) for a given member.

If the implementation of the class contain the following pattern:

**self.<member>**

then a violation will be counted if the class defines a getter/setter mehod compliant with the following naming (case insensitive) unless the declaration of this method is preceded with the decorator @property or @xxx.setter:

**(get|set)\_\*<member>**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Python is not Java. If you need to set or get the members of a class or object, just expose the member publicly and access it directly. If you need to perform some computations before getting or setting the member, then use Python’s built-in `property` decorator.

Usage of built-in `property` decorator allow to associate a member access syntax (<object>.<attribute>), to a treatment implemented by a function. this is usefull because:

- there is no “private attribute” concept in python’s classes. But property decorator force getters and setter decorators force to call a getter for each access to a member.
- for existing client code accessing directly to members , it is possible to add data treatment throught getter and setter without needing to modify the client code.

  ```
  class P:
      def __init__(self,x):
          self.x = x
  ```

  ```
      @x.setter
      def x(self, x):
          if x < 0:
              self.__x = 0
          elif x > 1000:
              self.__x = 1000
          else:
              self.__x = x
  ```

  ```
      @property
      def x(self):
          return self.__x
  ```

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://docs.quantifiedcode.com/python-code-patterns/correctness/implementing\_java-style\_getters\_and\_setters.html

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
