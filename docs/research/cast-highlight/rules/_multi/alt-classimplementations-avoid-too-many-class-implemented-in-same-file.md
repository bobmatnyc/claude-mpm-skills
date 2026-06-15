---
title: Too many class implementations can increase costs
url: https://doc.casthighlight.com/alt_classimplementations-avoid-too-many-class-implemented-in-same-file/
slug: alt_classimplementations-avoid-too-many-class-implemented-in-same-file
content_type: rule
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Too many class implementations can increase costs

Count the number of distinct classes involved in the scope of implemented methods. ex :

**MyNamespace::MyClasse1**::MyMethods () {…}

**MyClasse2**::MyMethods () {…}

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
