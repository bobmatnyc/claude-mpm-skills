---
title: Avoid using complex operands
url: https://doc.casthighlight.com/alt_complexoperands-avoid-using-complex-operands/
slug: alt_complexoperands-avoid-using-complex-operands
content_type: rule
category: Transferability
has_code_examples: false
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/software-elegance/)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

This code insight sanctions data accesses in operands having a too high level of indirection. The level of indirection is determined by the path you need to go through in order to get your data from an object (e.g. myObject.a.b.c.myData). Too many occurrences of this pattern generally decreases readability of the code, especially when indirection layer names are not meaningful. It may also reveal a lack of Oriented-Object encapsulation.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends reducing the level of indirection when possible, whether by creating a variable that accesses to intermediate levels or by using Getters.

# **References**

<https://stackoverflow.com/questions/288623/level-of-indirection-solves-every-problem>

# **How we detect**

This Code Insight counts the level of indirection found in operands.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
