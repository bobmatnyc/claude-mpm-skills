---
title: Avoid abstract classes without abstract or concrete methods
url: https://doc.casthighlight.com/alt_badabstractclass-avoid-abstract-classes-without-abstract-concrete-methods/
slug: alt_badabstractclass-avoid-abstract-classes-without-abstract-concrete-methods
content_type: rule
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Abstract classes can have public constructors, and this is required in [some particular cases](https://stackoverflow.com/questions/260666/can-an-abstract-class-have-a-constructor/261159). But a public constructor means that the class can be instantiated directly while, by design, abstract classes are aimed to not be instantiable.

# **How we detect**

CAST Highlight counts one occurrence each time an abstract class is defining a public constructor.

```
abstract class MyClass {
def I = 0

public MyClass() { } // +1 VIOLATION

MyClass(int i) { // +1 VIOLATION (members are public by default)
I = i
}
}
```

# **References**

<https://codenarc.org/codenarc-rules-design.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
