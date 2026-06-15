---
title: Avoid using ellipsis in functions
url: https://doc.casthighlight.com/alt_ellipsis-avoid-using-ellipsis-functions/
slug: alt_ellipsis-avoid-using-ellipsis-functions
content_type: rule
languages: [java, cpp]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Functions should not be defined with a variable number of arguments. Varargs methods are a convenient way to define methods that require a variable number of arguments, but they should not be overused. They can produce confusing results if used inappropriately.

# **How we detect**

This Code Insight counts one occurrence each time the following pattern is detected in the source code:

```
void function ( String... strings )
{
// ...
}
```

# **References**

<https://www.baeldung.com/java-varargs>  
<http://jtechies.blogspot.com/2012/07/item-42-use-varargs-judiciously.html>  
<https://github.com/isocpp/CppCoreGuidelines/blob/036324/CppCoreGuidelines.md#f55-dont-use-va_arg-arguments>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
