---
title: Missing spaces can increase costs
url: https://doc.casthighlight.com/alt_badspacing-avoid-missing-spaces/
slug: alt_badspacing-avoid-missing-spaces
content_type: rule
languages: [python]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Missing spaces can increase costs

This code insight counts one violation each time :

- following operators are not surrounder with at least one space: **=, += ,****-=, == , < , > , != , <> , <= , >= , in , not in , is ,****is not, and , or ,****not**.
- following elements are not followed by at least one space : **comma, semicolon, colon** (except slice operator)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

- Always surround these binary operators with a single space on either side: assignment ( = ), augmented assignment ( += , -= etc.), comparisons ( == , < , > , != , <> , <= , >= , in , not in , is , is not ), Booleans ( and , or , not ).

**Additional for Highlight :**

- Always put a whitespace immediately after :
  - comma
  - semicolon
  - colon (except when using as slice operator)

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
