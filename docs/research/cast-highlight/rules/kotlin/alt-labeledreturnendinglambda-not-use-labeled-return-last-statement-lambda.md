---
title: Do not use a labeled return for the last statement in a lambda
url: https://doc.casthighlight.com/alt_labeledreturnendinglambda-not-use-labeled-return-last-statement-lambda/
slug: alt_labeledreturnendinglambda-not-use-labeled-return-last-statement-lambda
content_type: rule
languages: [kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

The return keyword is relative to the nearest enclosing function (or anonymous function). So for returning from lambda, a labeled return is needed. But as recommended by official Kotlin coding convention, do not use a labeled return for the last statement in a lambda. Prefer lambda mechanism based on implicit return of the last expression used. If you need explicit return, then for a lambda you would have to use a heavy labeled return syntax. So in this case, prefer converting the lambda into anonymous function that use a simple return syntax.

# **How we detect**

CAST Highlight counts one occurrence each time a labeled return is the last instruction of a lambda.

```
fun foo1() {
listOf(1, 2, 3, 4, 5).forEach lit@{
if (it == 3) return@lit
print(it)

return @lit // terminal labeled return => +1 VIOLATION
}
}
```

# **References**

<https://kotlinlang.org/docs/coding-conventions.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
