---
title: Explicit return in __init__ is Unproductive
url: https://doc.casthighlight.com/alt_constructorreturn-avoid-explicit-return-in-__init__/
slug: alt_constructorreturn-avoid-explicit-return-in-__init__
content_type: rule
languages: [python]
category: Efficiency
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Explicit return in \_\_init\_\_ is Unproductive**

This code insight counts one violation each time a return statement is encountered in a \_\_init\_\_ method.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

`__init__` is a [special Python method](https://docs.python.org/2/reference/datamodel.html#special-method-names) that is automatically called when memory is allocated for a new object. The sole purpose of `__init__` is to initialize the values of instance members for the new object. Using `__init__` to return a value implies that a program is using `__init__` to do something other than initialize the object. This logic should be moved to another instance method and called by the program later, after initialization.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Returning%20a%20value%20from%20%60\_\_init\_\_%60/4RjRB5HW

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
