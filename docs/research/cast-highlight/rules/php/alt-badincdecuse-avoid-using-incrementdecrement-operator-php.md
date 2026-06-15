---
title: Increment/Decrement Operators can increase costs
url: https://doc.casthighlight.com/alt_badincdecuse-avoid-using-incrementdecrement-operator-php/
slug: alt_badincdecuse-avoid-using-incrementdecrement-operator-php
content_type: rule
languages: [php]
category: Efficiency
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Increment/Decrement Operators can increase costs

This code insight searches all the artifacts having increment/decrement operators.

Increment and decrement operators

1) cannot be used in an arithmetic operation.

Ex of violation :  
**$id = –$i – $x;**

2) must be bracketed when used in string concatenation.

Ex of violation :  
**$id = $id.’\_’.$i++;**  
should be $id = $id.’\_’.($i++);

3) should be used where possible.

Ex of violation :  
**$var = (1 – $var);**  
should be $var–;

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

For performance reasons, it is preferable to avoid incrementer/decrement operators.  
This could be time and memory consuming.  Try to reduce the number of artifacts having Increment/decrement operators.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
