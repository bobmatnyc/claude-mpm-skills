---
title: The code contains too many throws to system exceptions
url: https://doc.casthighlight.com/alt_illegalthrows-the-code-contains-too-many-throws-to-system-exceptions/
slug: alt_illegalthrows-the-code-contains-too-many-throws-to-system-exceptions
content_type: rule
languages: [java]
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The code contains too many thows to system exceptions (java.lang.Error, java.lang.RuntimeException). Application should have their own error exception classes. Throwing generic exception force callers to use generic catches. Prefer to use applicative and more specialized exceptions.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **References**

<https://www.codegrepper.com/code-examples/java/java+throw+an+exception>  
<https://dzone.com/articles/9-best-practices-to-handle-exceptions-in-java>

# **How we detect**

This Code Insight counts one occurrence each time one of these patterns are found into the source code:

```
java.lang.Error
java.lang.RuntimeException
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
