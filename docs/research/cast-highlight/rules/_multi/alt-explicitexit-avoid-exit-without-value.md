---
title: No explicit EXIT instruction in last statement in KSH can be risky
url: https://doc.casthighlight.com/alt_explicitexit-avoid-exit-without-value/
slug: alt_explicitexit-avoid-exit-without-value
content_type: rule
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **No explicit EXIT instruction in last statement in KSH can be risky**

This code insight counts one violation each time the last instruction of the script is not **EXIT**.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

If no exit is used, the default behaviour is to exit with the return code of the last command executed. A well controlled error management practice is to to terminate with an explicit EXIT statement.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
