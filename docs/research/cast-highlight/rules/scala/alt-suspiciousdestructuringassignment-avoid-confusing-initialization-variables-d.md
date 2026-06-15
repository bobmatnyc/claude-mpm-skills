---
title: Avoid confusing initialization for variables declared on the same line
url: https://doc.casthighlight.com/alt_suspiciousdestructuringassignment-avoid-confusing-initialization-variables-declared-line/
slug: alt_suspiciousdestructuringassignment-avoid-confusing-initialization-variables-declared-line
content_type: rule
languages: [scala]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Destructuring assignment are a practical sugar syntax, but due to dynamic typing, ommitting the parentheses lead to a syntactically correct, but however functionnally incorrect, implementation.

# **How we detect**

CAST Highlight counts one occurrence each time a variable is initialized with a tab, variable (or function call) in the following context :

- the variable is preceded by another declaration on the same line
- the variables are not inside a destructuring parentheses syntax.

```
    def a, b = [1, 2]              // +1 VIOLATION (bad, b is null)
    def c, d, e = [1, 2, 3] // +1 VIOLATION  (bad, c and d are null)
    def a, b = functionReturningTad()  // +1 VIOLATION (bad, b is null, even if the function is returning a tab!!)
    class MyClass {
        def a, b, c = [1, 2, 3]  // +1 VIOLATION (bad, a and b are null)
    }
    
    def x = [1, 2, 3]       // ok
    def (f, g) = [1, 2]    // ok
    (a, b, c) = [1, 2, 3]  // ok
```

# **References**

<https://codenarc.org/codenarc-rules-groovyism.html#confusingmultiplereturns-rule>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
