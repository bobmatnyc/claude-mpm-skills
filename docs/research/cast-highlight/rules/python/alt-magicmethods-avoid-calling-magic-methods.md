---
title: Magic Methods in Python can be Risky
url: https://doc.casthighlight.com/alt_magicmethods-avoid-calling-magic-methods/
slug: alt_magicmethods-avoid-calling-magic-methods
content_type: rule
languages: [python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Magic Methods in Python can be Risky**

This code insight counts one violation each time a magic method is called, except if it is in the body of a magic method.

**bad**

```
first_names = ["eve", "lisa", "robert", "paul", "alice"]
if first_names.__contains__("robert"):
    print("list of first names contains robert")
```

**`good`**

*example 1*

```
first_names = ["eve", "lisa", "robert", "paul", "alice"]
if "robert" in first_names:
    print("list of first names contains robert")
```

this example illustrate the work around for the bad example above: the \_\_contains\_\_ method is still called, but in background through the use of python high level mechanism, for which magic methods are intended to be used.

*example 2*

class child\_class(**parent\_class**):  
def **\_\_init\_\_**():  
**super().\_\_init\_\_**()

def **\_\_contains\_\_**(arg1, arg2):  
**parent\_class.\_\_contains\_\_**(arg1)  
print(arg2)

in this example, the call to **super().\_\_init\_\_()** and **parent\_class.\_\_init\_\_()** are not violation because its a call of parent’s method in a context of respectively overriding and overloading

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Magic methods (starting and ending with two underscores) should not have to be called directly unless . Magic methods are used to implement specific protocols and are called for you, either due to operator access or due to some special operation.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Avoid%20calling%20magic%20methods/7dz67uIe

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
