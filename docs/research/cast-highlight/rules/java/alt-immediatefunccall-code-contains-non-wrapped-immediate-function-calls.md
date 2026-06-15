---
title: The code contains non-wrapped immediate function calls
url: https://doc.casthighlight.com/alt_immediatefunccall-code-contains-non-wrapped-immediate-function-calls/
slug: alt_immediatefunccall-code-contains-non-wrapped-immediate-function-calls
content_type: rule
languages: [java, javascript]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

When a function is to be invoked immediately, the entire invocation expression should be wrapped in parents. Wrapping an immediate function invocation in parentheses is usefull to assist the reader in understanding that the expression is the result of a function, and not the function itself.

# **How we detect**

CAST Highlight counts one occurrence each time a function called immediatelly is not wrapped into parenthesis. This concerns only function expression, not function declarations.

**Bad Code**

```
var collection = function () {
        ...
        [ some code ]

        ...
} ();
```

**Good Code**

```
var collection = (function () {
        ...
        [ some code ]
        ...

} ());
```

# **References**

<http://crockford.com/javascript/>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
