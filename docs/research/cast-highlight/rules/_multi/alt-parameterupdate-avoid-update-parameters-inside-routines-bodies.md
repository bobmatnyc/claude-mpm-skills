---
title: Avoid to update parameters inside routine’s bodies
url: https://doc.casthighlight.com/alt_parameterupdate-avoid-update-parameters-inside-routines-bodies/
slug: alt_parameterupdate-avoid-update-parameters-inside-routines-bodies
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Reassigning parameter of function to a new value within the body of the method/closure, is a confusing and questionable practice. Use a temporary variable instead.

# **How we detect**

CAST Highlight counts one occurrence each time a parameter is updated inside the body of the function/method/closure, using the following operators =, +=, -=, \*=, /=, %=, ++, – -.

```
class toto {
String field = "";
public String getFoo(int param, String field)
{
param = 0 // +1 VIOLATION
param++ // +1 VIOLATION
param -= 10 // +1 VIOLATION

a = (param == 0 ? 1 : null) // OK
my_param = 0 //OK

this.field = "Yo!" // OK because field is not the parameter.
}
}
```

# **References**

<https://codenarc.org/codenarc-rules-convention.html#parameterreassignment-rule>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
