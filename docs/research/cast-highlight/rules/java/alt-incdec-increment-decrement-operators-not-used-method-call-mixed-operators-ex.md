---
title: Increment (++) and decrement (–) operators should not be used in a method call or mixed with other operators in an expression
url: https://doc.casthighlight.com/alt_incdec-increment-decrement-operators-not-used-method-call-mixed-operators-expression/
slug: alt_incdec-increment-decrement-operators-not-used-method-call-mixed-operators-expression
content_type: rule
languages: [java]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

The use of increment and decrement operators in method calls or in combination with other arithmetic operators is not recommended, because:

- It can significantly impair the readability of the code.
- It introduces additional side effects into a statement, with the potential for undefined behavior.
- It is safer to use these operators in isolation from any other arithmetic operators.

# **How we detect**

CAST Highlight counts one occurrence each time an operator ++ or – – is not the only one in the statement or an operator ++ or – – is used as a parameter in function call.

**Bad Code**

```
u8a = ++u8b + u8c--
foo = bar++ / 4
myMethodCall(foo++)
myMethodCall(bar--)
myMethodCall(++foo)
myMethodCall(--bar)
```

Good Code

```
++u8b
u8a = u8b + u8c
u8c--
foo = bar / 4
bar++
```

# **References**

<https://rules.sonarsource.com/java/RSPEC-1066>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
