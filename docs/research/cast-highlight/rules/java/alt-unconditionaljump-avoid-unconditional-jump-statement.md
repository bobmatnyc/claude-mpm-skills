---
title: Avoid unconditional jump statement
url: https://doc.casthighlight.com/alt_unconditionaljump-avoid-unconditional-jump-statement/
slug: alt_unconditionaljump-avoid-unconditional-jump-statement
content_type: rule
languages: [java]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Having an unconditional break, return or throw in a loop renders it useless; the loop will only execute once and the loop structure itself is simply wasted keystrokes. Having an unconditional continue in a loop is itself wasted keystrokes. For these reasons, unconditional jump statements should never be used except for the final return in a function or method.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **References**

<http://cwe.mitre.org/data/definitions/484.html>  
<https://dl.acm.org/doi/abs/10.1145/143095.143144>  
<https://rules.sonarsource.com/java/RSPEC-128>

# **How we detect**

This Code Insight counts one occurrence each time one of these patterns is found into the source code:

```
return, break, continue is unconditional inside a loop.
return, throw is unconditional inside a method, unless it is the last instruction
break is unconditional in a case statement, unless it is the last instruction.
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
