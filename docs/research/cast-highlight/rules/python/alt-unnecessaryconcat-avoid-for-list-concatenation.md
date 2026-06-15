---
title: Having + for list concatenation
url: https://doc.casthighlight.com/alt_unnecessaryconcat-avoid-for-list-concatenation/
slug: alt_unnecessaryconcat-avoid-for-list-concatenation
content_type: rule
languages: [python]
category: Efficiency
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Having + for list concatenation**

This code insight counts one violation each time a “+” operator is involved in list concatenation.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Extending a list through a reassignment is not recommended since Python offers other solution for that task with significant performance benefits.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/performance/Use%20%60extend%28%29%60%20for%20list%20concatenation/3kr7yXet

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
