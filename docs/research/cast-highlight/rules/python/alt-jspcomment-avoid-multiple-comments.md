---
title: Multiple JSP Comments can increase costs
url: https://doc.casthighlight.com/alt_jspcomment-avoid-multiple-comments/
slug: alt_jspcomment-avoid-multiple-comments
content_type: rule
languages: [python, java]
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Multiple JSP Comments can increase costs

This code insight counts one violation each time too consécutive comment blocs are encountered.

JSP comments **<%–** are concerned as well as java comment **/\*** or **//** inside a scriptlet.

HTML comments are not considered.

If two JSP comments are separated by HTML code (not containing any JSP tag), they are not considerered following each other, so there is no violation.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Multiple comments can hamper the agility of the code.

## **Business Impacts**

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/Avoid%20%22non-Pythonic%22%20attribute%20names/3ueqPTsn

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
