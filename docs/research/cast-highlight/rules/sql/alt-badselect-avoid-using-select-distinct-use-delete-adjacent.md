---
title: "Avoid using “SELECT DISTINCT”, use DELETE-ADJACENT"
url: https://doc.casthighlight.com/alt_badselect-avoid-using-select-distinct-use-delete-adjacent/
slug: alt_badselect-avoid-using-select-distinct-use-delete-adjacent
content_type: rule
languages: [sql]
category: Efficiency
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Avoid using “SELECT DISTINCT”, use DELETE-ADJACENT

#

This code insight ensures for performance reason, if some of the fields are not part of an index, then it is often better to avoid using SELECT DISTINCT.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://technet.microsoft.com/en-us/library/ms187009(v=sql.105).aspx

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
