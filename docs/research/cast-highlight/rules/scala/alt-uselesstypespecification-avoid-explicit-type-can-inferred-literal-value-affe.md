---
title: Avoid explicit type when it can be inferred from literal value affected
url: https://doc.casthighlight.com/alt_uselesstypespecification-avoid-explicit-type-can-inferred-literal-value-affected/
slug: alt_uselesstypespecification-avoid-explicit-type-can-inferred-literal-value-affected
content_type: rule
languages: [scala, kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

For code readability purpose, if a property initializer is a scalar value or the return type can be clearly inferred from the body then it can be omitted.

# **How we detect**

CAST Highlight counts one occurrence each time a variable (or class property) is declared with an explicit type and initialized with one of the following scalar values:

- “…” or ‘…’ (string)
- false or true (boolean)
- integer or signed integer
- decimal : a dot followed by a digit number

**Bad Code**

```
var a : String = "it's a string" // +1 VIOLATION
val b : Boolean = false // +1 VIOLATION
const val c : Int = 123 // +1 VIOLATION
val d : Any = -123 // +1 VIOLATION
val e : Float = .123 // +1 VIOLATION
```

# **References**

<https://developer.android.com/kotlin/style-guide>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
