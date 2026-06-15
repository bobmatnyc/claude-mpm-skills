---
title: Avoid Equals methods not testing their parameters
url: https://doc.casthighlight.com/alt_equalsnottestingparameter-avoid-equals-methods-not-testing-parameters/
slug: alt_equalsnottestingparameter-avoid-equals-methods-not-testing-parameters
content_type: rule
languages: [java]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Because the equals method takes a generic Object as a parameter, any type of object may be passed to it. The method should not assume it will only be used to test objects of its class type. It must instead check the parameter’s type.

CAST Highlight considers that the type of the parameter will be checked if the Equals method contains a “if” statement whose condition is checking <p>.getClass(), where <p> is the name of the parameter.

# **How we detect**

CAST Highlight counts one occurrence each time an Equals method doesn’t test its parameter type using if + <p>.getClass().

**Bad Code**

```
class myClass {
equals(Object c) {
// no if (c.getGlass() ....) check ...
}
}
```

**Good Code**

```
class myClass {
equals(Object c) {
if (c.getClass() eq "myClass") {
...
}
...
}
}
```

# **References**

<https://rules.sonarsource.com/java/RSPEC-2097>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
