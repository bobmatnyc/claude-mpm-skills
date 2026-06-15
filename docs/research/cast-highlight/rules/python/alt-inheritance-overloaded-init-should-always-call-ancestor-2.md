---
title: Always call ancestor to avoid risks in Python code
url: https://doc.casthighlight.com/alt_inheritance-overloaded-__init__-should-always-call-ancestor-2/
slug: alt_inheritance-overloaded-__init__-should-always-call-ancestor-2
content_type: rule
languages: [python]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Always call ancestor to avoid risks in Python code**

This code insight counts one violation each time an \_\_init\_\_ method is not calling its ancestor.

In a class declared like:

class childClass (parentClass):  
…def \_\_init\_\_(self):  
……

The body of the \_\_init\_\_ function should contain the one of the following statements :

**super( … ).\_\_init\_\_(…)**ORone pattern  **parentClass.\_\_init\_\_(…)** for each parent class. (there can be several parent class in case of multiple inheritance).

There is no violation if **parentClass** is the “object” class.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

If a base class has an \_\_init\_\_ method defined, its child classes should always call that method in their own \_\_init\_\_ implementations. Forgetting to call the base class’ \_\_init\_\_ method could leave instance members of it uninitialized. This can introduce bugs in a program if the derived class attempts to use any of the uninitialized instance members.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Call%20%60\_\_init\_\_%60%20method%20from%20base%20class/4MeaWnJD

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
