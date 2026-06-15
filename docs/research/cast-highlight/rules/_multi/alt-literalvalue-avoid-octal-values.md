---
title: Avoid octal values
url: https://doc.casthighlight.com/alt_literalvalue-avoid-octal-values/
slug: alt_literalvalue-avoid-octal-values
content_type: rule
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Integer literals starting with a zero are octal rather than decimal values. While using octal values is fully supported, most developers do not have experience with them. They may not recognize octal values as such, mistaking them instead for decimal values.

# **How we detect**

This Code Insight counts one occurrence each time an octal value is detected in the source code. Octal values are identified with the following regular expression:

```
[+-]?0[0..7]+
```

# **References**

<https://wiki.sei.cmu.edu/confluence/display/c/DCL18-C.+Do+not+begin+integer+constants+with+0+when+specifying+a+decimal+value>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
