---
title: While Loops are more productive than For Loops
url: https://doc.casthighlight.com/alt_badloop-avoid-for-loops-which-can-be-simplified-to-a-while-loop-php/
slug: alt_badloop-avoid-for-loops-which-can-be-simplified-to-a-while-loop-php
content_type: rule
languages: [php, sql]
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **While Loops are more productive than For Loops**

This code insight searches all the artifacts having for loops which can be simplified to a while loop.

For loops that do not have Init nor Update part :

**for ( ;cond; )**

Remedy –

Try to reduce the number of the artifacts having for loops which can be  
simplified to a while loop.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

For performance reasons, while loops are prefered to for loops.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
