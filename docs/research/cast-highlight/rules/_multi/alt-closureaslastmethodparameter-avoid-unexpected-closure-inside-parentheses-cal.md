---
title: Avoid unexpected closure inside parentheses call
url: https://doc.casthighlight.com/alt_closureaslastmethodparameter-avoid-unexpected-closure-inside-parentheses-call/
slug: alt_closureaslastmethodparameter-avoid-unexpected-closure-inside-parentheses-call
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

If a method is called and the last parameter is an inline closure then it can be declared outside of the method call parentheses, to comply with Groovy style programming.

# **How we detect**

CAST Highlight counts one occurrence each time an inline closure is encountered inside parameters, in last position of the call parameters.

```
    [1,2,3].each({ println it })   // +1 VIOLATION
    [1,2,3].each { println it }    // OK
```

# **References**

<https://codenarc.org/codenarc-rules-groovyism.html#closureaslastmethodparameter-rule>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
