---
title: Prefer using expression Form for ‘if’ or ‘when’ in place of statement syntax
url: https://doc.casthighlight.com/alt_missingexpressionform-prefer-using-expression-form-place-statement-syntax/
slug: alt_missingexpressionform-prefer-using-expression-form-place-statement-syntax
content_type: rule
languages: [kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

In Kotlin, “if” and “when” returns a value, and so can be used as expression. When possible, prefer using the expression form.

# **How we detect**

CAST Highlight counts one occurrence each time

a “if” or a “when” implemented with the statement syntax has all of his clauses factorizable by using the expression form.  
Clauses are factorizable if they all begin with the same pattern :

- return
- <identifier> =

Bad Code

```
foo1() {
if (x) // +1 VIOLATION
return foo()
else
return bar()

when(x) { // +1 VIOLATION
0 -> return "zero"
else -> return "nonzero"
}
}
fun foo2() {
// +1 VIOLATION
if (!shouldAlwaysStoreArrayInNewVar && value is StackValue.Local && value.type == asmLoopRangeType) {
arrayVar = value.index // no need to copy local variable into another variable
} else {
arrayVar = createLoopTempVariable(OBJECT_TYPE)
}
return arrayVar
}
```

Good Code

```
fun foo1() {
     return if (x) foo() else bar()
 
     return when(x) {
         0 -> "zero"
         else -> "nonzero"
     }
}
fun foo2() {
        // +1 VIOLATION
        arrayVar = if (!shouldAlwaysStoreArrayInNewVar && value is StackValue.Local && value.type == asmLoopRangeType) value.index else createLoopTempVariable(OBJECT_TYPE)
 
        return arrayVar
}
```

# **References**

<https://kotlinlang.org/docs/coding-conventions.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
