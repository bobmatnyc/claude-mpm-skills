---
title: Bad method names can increase costs
url: https://doc.casthighlight.com/alt_badnaming-avoid-bad-method-name/
slug: alt_badnaming-avoid-bad-method-name
content_type: rule
languages: [python]
category: Transferability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Bad method names can increase costs

This code insight counts one violation each time the name do not complies with:

**[a-z\_][a-z0-9\_]$**

- underscore allowed
- lowercase

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

The name of the method does match the naming convention. This error is a stylistic warning. The code will execute. But you can improve the readability of the code by renaming the method to match the following regular expression: `[a-z_][a-z0-9_]{2,}$`.

## **Business Impacts**

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Avoid%20%22non-Pythonic%22%20method%20names/2QdgB8ll

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
