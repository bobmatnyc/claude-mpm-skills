---
title: Prefer to use an expression body for functions whose body consists of a single expression
url: https://doc.casthighlight.com/alt_unexpectedbody-prefer-use-expression-body-functions-whose-body-consists-single-expression/
slug: alt_unexpectedbody-prefer-use-expression-body-functions-whose-body-consists-single-expression
content_type: rule
languages: [kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Prefer using an expression body for functions with the body consisting of a single expression.

# **How we detect**

CAST Highlight counts one occurrence each time a function consisting of a single instruction is using a body implementation (instructions enclosed between accolades).

```
fun foo(): Int {     // +1 VIOLATION
    return 1 
}
 
fun foo() = 1        // +0 good
 
fun foo(): Int {     // +0  because instruction is a "if" statement
   if (toto) {
       return 1
    }
}
 
fun foo(): Int {     // +0  because instruction is a "if" statement
   if (toto) {
       return 1
    }
}
 
// +0 because the instruction is written over at least 5 lines.
public inline fun <T, K> Iterable<T>.groupingBy(crossinline keySelector: (T) -> K): Grouping<T, K> {
    return object : Grouping<T, K> {
        override fun sourceIterator(): Iterator<T> = this@groupingBy.iterator()
        override fun keyOf1(element: T): K = keySelector(element1)
        override fun keyOf2(element: T): K = keySelector(element2)
    }
}
```

# **References**

<https://kotlinlang.org/docs/coding-conventions.html#function-formatting>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
