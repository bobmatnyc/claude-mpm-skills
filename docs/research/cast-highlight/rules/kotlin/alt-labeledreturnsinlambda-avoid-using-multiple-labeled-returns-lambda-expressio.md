---
title: Avoid using multiple labeled returns in lambda expression
url: https://doc.casthighlight.com/alt_labeledreturnsinlambda-avoid-using-multiple-labeled-returns-lambda-expression/
slug: alt_labeledreturnsinlambda-avoid-using-multiple-labeled-returns-lambda-expression
content_type: rule
languages: [kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

The return keyword is relative to the nearest enclosing function (or anonymous function). So for returning from lambda, a labeled return is needed. But as recommended by official Kotlin coding convention, avoid using multiple labeled returns in a lambda. Consider restructuring the lambda so that it will have a single exit point. If that’s not possible or not clear enough, consider converting the lambda into an anonymous function.

# **How we detect**

CAST Highlight counts one occurrence each time a lambda is using several labeled returns.

```
fun foo1() {
listOf(1, 2, 3, 4, 5).forEach lit@{
if (it == 3) return@lit // first labeled return 
print(it)
return @lit // second labeled return => VIOLATION
}
}
```

# **References**

<https://kotlinlang.org/docs/coding-conventions.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
