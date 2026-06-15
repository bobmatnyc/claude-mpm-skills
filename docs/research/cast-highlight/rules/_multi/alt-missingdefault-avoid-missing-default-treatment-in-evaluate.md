---
title: EVALUATE instructions without default treatment causes Production Risk
url: https://doc.casthighlight.com/alt_missingdefault-avoid-missing-default-treatment-in-evaluate/
slug: alt_missingdefault-avoid-missing-default-treatment-in-evaluate
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# EVALUATE instructions without default treatment causes Production Risk

This code insight counts one violation each time the statement **WHEN OTHER** is missing for an EVALUATE instruction.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Each EVALUATE structure should have a WHEN OTHER statement to provide a default treatment in case the program has an unexpected behaviour.

Nested EVALAUTE instructions should have their own default treatment.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
