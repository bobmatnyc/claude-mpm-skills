---
title: Type() can hamper productivity
url: https://doc.casthighlight.com/alt_instanceof-avoid-type-in-conditions/
slug: alt_instanceof-avoid-type-in-conditions
content_type: rule
languages: [python]
category: Changeability
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Type() can hamper productivity**

This code insight detects each time type() is used in code

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

*The function isinstance is the best-equipped to handle type checking because it supports inheritance (e.g. an instance of a derived class is an instance of a base class, too). Therefore  isinstance should be used whenever type comparison is required*

## **Business Impacts**

*Type() negatively affects productivity bcause it creates improper comparisons*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://docs.quantifiedcode.com/python-code-patterns/readability/do\_not\_compare\_types\_use\_isinstance.html

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
