---
title: Force casts should not be used
url: https://doc.casthighlight.com/alt_dangerouscast-force-casts-not-used/
slug: alt_dangerouscast-force-casts-not-used
content_type: rule
languages: [swift, cpp]
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Because force casting (*as!*) does not perform any type safety validations, it is capable of performing dangerous conversions between unrelated types. When the types are truly unrelated, the cast will cause a system crash.

# **How we detect**

CAST Highlight counts one occurrence each time a “*as!*” pattern is detected in source code.

**Bad Code**

```
foo as! MyClass // Noncompliant
```

**Good Code**

```
foo as? MyClass
```

# **References**

CppCoreGuidelines, Type safety profile – Type.1: Don’t use reinterpret\_cast  
<https://rules.sonarsource.com/swift/RSPEC-3630>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
