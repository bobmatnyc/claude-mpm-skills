---
title: len() as upper boundary makes code less readable
url: https://doc.casthighlight.com/alt_rangeboundary-avoid-using-len-as-upper-boundary/
slug: alt_rangeboundary-avoid-using-len-as-upper-boundary
content_type: rule
languages: [python]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **len() as upper boundary makes code less readable**

This code insight shows that  
Python tries to make the task of slicing lists and numpy.arrays as convenient as possible.

If one needs a slice which reaches till the end of the object the upper boundary can be left empty.

When negative numbers are used the indexing will start at the end.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

Quantified code :

https://www.quantifiedcode.com/knowledge-base/readability/Omit%20%60len%28%29%60%20as%20upper%20boundary/27a0ZNa7

https://www.quantifiedcode.com/knowledge-base/Omit%20%60len()%60%20for%20indexing/slicing/49Cho3Zk

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
