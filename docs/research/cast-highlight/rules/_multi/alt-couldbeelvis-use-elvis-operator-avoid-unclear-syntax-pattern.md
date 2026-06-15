---
title: Use Elvis operator to avoid unclear syntax pattern
url: https://doc.casthighlight.com/alt_couldbeelvis-use-elvis-operator-avoid-unclear-syntax-pattern/
slug: alt_couldbeelvis-use-elvis-operator-avoid-unclear-syntax-pattern
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Elvis operator ?: is an syntactic sugar for if (!x) { x=something }. Prefer Elvis notation for readability considerations.

# **How we detect**

CAST Highlight counts one occurrence each time the following pattern is encountered :

- if ( ! x)
- { x = … }
- x ? x : …

```
 if (!x) { // +1 VIOLATION
x = 'some value'
}

if (!x) // +1 VIOLATION
x = "some value"

if (!params.max) { // +1 VIOLATION
params.max = 10
}

x ?: 'some value' // OK

// TERNARY NOTATION
x ? x : false // +1 VIOLATION (can simplify to x ?: false)

foo() ? foo() : bar() // +1 VIOLATION (can simplify to foo() ?: bar())
foo(1) ? foo(1) : 123 // +1 VIOLATION (can simplify to foo(1) ?: 123)

(x == y) ? same : diff // OK
x ? y : z // OK
x ? x + 1 : x + 2 // OK
x ? 1 : 0 // OK
x ? !x : x // OK
!x ? x : null // OK

foo() ? bar() : 123 // OK
foo() ? foo(99) : 123 // OK
foo(x) ? foo() : 123 // OK
foo(1) ? foo(2) : 123 // OK
```

# **References**

<https://codenarc.org/codenarc-rules-convention.html#couldbeelvis-rule>  
<https://codenarc.org/codenarc-rules-convention.html#ternarycouldbeelvis-rule>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
