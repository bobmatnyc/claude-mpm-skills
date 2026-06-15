---
title: Avoid to update static fields from instance methods
url: https://doc.casthighlight.com/alt_assignmenttostaticfieldfrominstancemethod-avoid-update-static-fields-instance-methods/
slug: alt_assignmenttostaticfieldfrominstancemethod-avoid-update-static-fields-instance-methods
content_type: rule
languages: [scala]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Correctly updating a static field from a non-static method is tricky to get right and could easily lead to bugs if there are multiple class instances and/or multiple threads in play. Ideally, static fields are only updated from synchronized static methods.

# **How we detect**

CAST Highlight counts one occurrence each time a static field is directly updated from a non-static method with one of the following operators : =, +=, -=, \*=, /=, %=, ++, – –

```
class toto {
static def i = 0
def void meth1(int v) {
i = v // +1 VIOLATION
}

def void meth2(int v) {
int i
i = v // OK (i is the local variable)
}
def void meth3(int v) {
int i
this.i = v // +1 VIOLATION
}
def void meth4(int i, int v) {
i = v // OK (i is the parameter)
}
}
```

# **References**

<https://codenarc.org/codenarc-rules-design.html#assignmenttostaticfieldfrominstancemethod-rule>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
