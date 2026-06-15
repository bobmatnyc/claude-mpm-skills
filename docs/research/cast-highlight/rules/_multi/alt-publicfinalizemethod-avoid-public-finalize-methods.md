---
title: Avoid Public finalize() methods
url: https://doc.casthighlight.com/alt_publicfinalizemethod-avoid-public-finalize-methods/
slug: alt_publicfinalizemethod-avoid-public-finalize-methods
content_type: rule
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

A program should never call finalize explicitly, except to call *super.finalize()* inside an implementation of *finalize()*. In mobile code situations, the otherwise error prone practice of manual garbage collection can become a security threat if an attacker can maliciously invoke one of your *finalize()* methods because it is declared with public access. If you are using *finalize()* as it was designed, there is no reason to declare *finalize()* with anything other than protected access.

# **How we detect**

CAST Highlight counts one occurrence each time a class is declaring a finalyze() method with public modifier or no modifier (visibility is public by default).

```
public class CrashedFinalizable { 
@Override
public void finalize() { // +1 VIOLATION 
System.out.print("");
}
}

public class CrashedFinalizable_2 { 
@Override
def finalize() { // +1 VIOLATION (public is the default visibility)
System.out.print("");
}
}
```

# **References**

<https://codenarc.org/codenarc-rules-security.html#publicfinalizemethod-rule>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
