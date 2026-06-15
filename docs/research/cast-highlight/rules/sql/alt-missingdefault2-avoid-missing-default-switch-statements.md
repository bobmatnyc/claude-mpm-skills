---
title: Missing default in switch statements can cause Production Risk
url: https://doc.casthighlight.com/alt_missingdefault2-avoid-missing-default-switch-statements/
slug: alt_missingdefault2-avoid-missing-default-switch-statements
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Missing default in switch statements can cause Production Risk

This code insight ensures that the keyword “default” is executed when none of the conditions being tested for in the switch statement are met or executed. Having no default keyword, means that there is no backup. The cases that are “impossible” today are those most likely to be the causes of untraceable bugs in the future, when the impossible changes to the standard.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://technet.microsoft.com/en-us/library/ms187009(v=sql.105).aspx

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
