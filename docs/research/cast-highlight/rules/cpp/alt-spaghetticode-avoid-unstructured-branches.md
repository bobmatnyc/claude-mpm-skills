---
title: Inconditional branches are unproductive in C++
url: https://doc.casthighlight.com/alt_spaghetticode-avoid-unstructured-branches/
slug: alt_spaghetticode-avoid-unstructured-branches
content_type: rule
languages: [cpp, sql]
category: Robustness
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Inconditional branches are unproductive in C++**

This code insight

Count one violation each time one of the following keywords is encountered : continue, **goto**, **break**.

Exception : **break** at end of “**case**” statements.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Inconditional branches can lead to loss of productivity and necessary optimizations in the code.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
