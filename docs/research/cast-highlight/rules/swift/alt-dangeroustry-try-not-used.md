---
title: try! should not be used
url: https://doc.casthighlight.com/alt_dangeroustry-try-not-used/
slug: alt_dangeroustry-try-not-used
content_type: rule
languages: [swift]
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The use of Swift 2.0’s try! lets you execute code that might throw an exception without using the do and catch syntax normally required for such code. By using it, you’re guaranteeing that the executed code will never fail. But there might be some exceptions… And when it does fail, the program will exit abruptly, probably without cleaning up after itself.

# **How we detect**

CAST Highlight counts one occurrence each time a “try!” pattern is used.

**Bad Code**

```
let myvar = try! dangerousCode(foo);  // Noncompliant
// ...
```

**Good Code**

```
do {
  let myvar = try dangerousCode(foo);
  // ...
} catch {
  // handle error
}
```

# **References**

<https://rules.sonarsource.com/swift/RSPEC-3661>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
