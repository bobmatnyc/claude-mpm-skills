---
title: Using “is” for anything but singleton can increase costs
url: https://doc.casthighlight.com/alt_instanceof-avoid-using-is-for-anything-else-than-singleton/
slug: alt_instanceof-avoid-using-is-for-anything-else-than-singleton
content_type: rule
languages: [python]
category: Robustness
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Using “is” for anything but singleton can increase costs

Count one violation each time one of the operand of **is** (or **is not**) is not **None**, **True** or **False**.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Testing the identity of two objects can be achieved in python with a special operator called  **`is`**. Most prominently it is used to check whether an variable points to  **`None`**. But the operator can examine any kind of identity. This often leads to confusion because equality of two different objects will return  **`False`** .

forgiveness : As some exception can be tolerated, a few percentage of “is” for checking identity of two objects other than singleton should be allowed in the model.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/%60not%20…%20is%60%20used%20instead%20of%20%60is%20not%60/4ORGpHyx

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
