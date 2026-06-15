---
title: Inline comments can increase costs
url: https://doc.casthighlight.com/alt_inlinecomment-avoid-inline-comments/
slug: alt_inlinecomment-avoid-inline-comments
content_type: rule
languages: [python]
category: Changeability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Inline comments can increase costs

Count one violation each time an instruction statement is followed by a comment on the same line.

**bad** :

```
              x = y + z
```

**good**:

```
x = y + z
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

According to PEP8, trailing comments can be used but sparsely. To make your code readable, comments should be placed in a separate line, before the actual code. This ensures your comment is always visible and properly formatted.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/Avoid%20inline%20comments/2pqEXt6D

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
