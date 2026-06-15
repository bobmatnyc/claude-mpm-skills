---
title: Avoid long ‘if/else if’ chains that could be replaced by a ‘switch’ statement
url: https://doc.casthighlight.com/alt_elseif-avoid-long-else-chains-replaced-switch-statement/
slug: alt_elseif-avoid-long-else-chains-replaced-switch-statement
content_type: rule
languages: [java]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

For code readability purpose, prefer using *switch* if there are three or more options in a *if*.

# **How we detect**

CAST Highlight counts one occurrence each time a *elseif* chain is managing 3 or more conditions. That is, each time an *elseif* chain contains 2 “else if” or more.

**Example**

```
def iconstNode(value: Int) {
// FIRST OPTION
if (value >= -1 && value <= 5) {
InsnNode(Opcodes.ICONST_0 + value)
}
// SECOND OPTION
else if (value >= java.lang.Byte.MIN_VALUE && value <= java.lang.Byte.MAX_VALUE) {
IntInsnNode(Opcodes.BIPUSH, value)
}
// THIRD OPTION ==> +1 VIOLATION !!!!!
else if (value >= java.lang.Short.MIN_VALUE && value <= java.lang.Short.MAX_VALUE) {
IntInsnNode(Opcodes.SIPUSH, value)
}
else {
LdcInsnNode(Integer(value))
}
}
```

# **References**

<https://codenarc.org/codenarc-rules-convention.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
