---
title: Avoid catches that only rethrow
url: https://doc.casthighlight.com/alt_onlyrethrowingcatches-avoid-catches-rethrow/
slug: alt_onlyrethrowingcatches-avoid-catches-rethrow
content_type: rule
languages: [java]
category: Robustness
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

A catch clause that only rethrows the caught exception has the same effect as omitting the catch altogether and letting it bubble up automatically, but with more code and the additional detrement of leaving maintainers scratching their heads.

Such clauses should either be eliminated or populated with the appropriate logic.

# **How we detect**

CAST Highlight counts one occurrence each time the only instruction of a catch is to rethrow the catched exception.

**Bad Code**

```
catch (<exception type> <exception name>) {
throw <Exception name> ;
}
```

# **References**

<https://stackoverflow.com/questions/44419928/does-catching-and-rethrowing-the-exact-same-exception-mean-anything>  
<https://rules.sonarsource.com/java/RSPEC-2737>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
