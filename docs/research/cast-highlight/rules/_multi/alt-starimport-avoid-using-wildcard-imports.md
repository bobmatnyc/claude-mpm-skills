---
title: Wildcard(*) imports can increase production risks.
url: https://doc.casthighlight.com/alt_starimport-avoid-using-wildcard-imports/
slug: alt_starimport-avoid-using-wildcard-imports
content_type: rule
category: Transferability
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Wildcard(\*) imports can increase production risks.

This code insight counts one violation each time a wildcard import is used.

Violations pattern is:

**import \***

**from xxx import \***

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

In general, import statements should be as specific as possible and you should only import what you need. When “`from module import *"` is used, you are implicitly loading all locals of the *imported* module into and over the *importing* module. This has two disadvantages:

- first, you might unintentionally overload already imported objects.

- Second, it becomes difficult to detect undefined names in the program that imported the module.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Avoid%20using%20wildcard%20%28%2A%29%20imports/3Q3eTYIU

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
