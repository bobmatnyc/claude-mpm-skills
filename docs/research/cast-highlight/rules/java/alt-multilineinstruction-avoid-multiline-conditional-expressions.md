---
title: Multiline Conditional Expressions should be avoided
url: https://doc.casthighlight.com/alt_multilineinstruction-avoid-multiline-conditional-expressions/
slug: alt_multilineinstruction-avoid-multiline-conditional-expressions
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Multiline Conditional Expressions should be avoided**

This code insight counts one violation each time a multiline conditional expression is encountered.

bad

x = 1 if cond  
else 2

good

x = 1 if cond else 2

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Conditional expressions are mechanisms that provide a shorter syntax for if statements. For example: x = 1 if cond else 2.

May be harder to read than an if statement. The condition may be difficult to locate if the expression is long.

Okay to use for one-liners. In other cases prefer to use a complete if statement.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://support.objectivity.com/sites/default/files/docs/objy/R11\_0\_0/html/java/guide/jgdObjectQualification.html

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
