---
title: Empty functions and methods should be avoided
url: https://doc.casthighlight.com/alt_emptyartifact-code-contains-many-empty-functions-procedures-methods-modules/
slug: alt_emptyartifact-code-contains-many-empty-functions-procedures-methods-modules
content_type: rule
languages: [scala, kotlin, swift, abap, dotnet, java]
category: Transferability
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

For maintainability aspect, it is not recommended to have empty functions, methods or classes, as it could decrease readability because readers need to guess whether it’s intentional or not.

Technology scope: ABAP, C#, Go, Groovy, Java, Kotlin, Scala, Swift.

Note that for Java and Kotlin, this code insight also applies for classes.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Check if the object is referenced. If not then remove it.

# **How we detect**

This Code Insight counts one occurrence each time a function, a method or a class is found and that it doesn’t contain any statement.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
