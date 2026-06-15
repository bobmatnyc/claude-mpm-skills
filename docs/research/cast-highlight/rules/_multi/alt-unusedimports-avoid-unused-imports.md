---
title: Unused imports cause risks in code
url: https://doc.casthighlight.com/alt_unusedimports-avoid-unused-imports/
slug: alt_unusedimports-avoid-unused-imports
content_type: rule
category: Changeability
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Unused imports cause risks in code**

This code insight counts one violation each time a import is nerver used.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Usually, when this issue is encountered, it means that you began implementing a module but did not finish it. Other times, you might have refactored a module, but you forgot to remove the import statement. Treat this issue as a warning and review the module in question.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/Clean%20up%20unused%20imports/22jm8C6t

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
