---
title: If & else statements can be taxing for the CPU
url: https://doc.casthighlight.com/alt_unconditionnal-avoid-unconditional-if-and-elseif-statements/
slug: alt_unconditionnal-avoid-unconditional-if-and-elseif-statements
content_type: rule
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

If and else statements are considered to be time consuming in nature as they tend to be repetitive in order to execute the code properly which causes is not ideal for a programmer and can also be considered taxing for the CPU.

# **Business Impacts**

While if and else statements are an essential component of the code, overusing them can be risky because it can slow down the code. This makes the code unproductive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://stackoverflow.com/questions/2086529/what-is-the-relative-performance-difference-of-if-else-versus-switch-statement-i>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight’s rationale is that using unconditional if, and else, tends to greatly consume time as well as memory. It is recommended to review the source code and reduce the number of unconditional if and else-if statements.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
