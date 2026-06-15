---
title: Avoid generic catch
url: https://doc.casthighlight.com/alt_genericcatches-avoid-generic-catch/
slug: alt_genericcatches-avoid-generic-catch
content_type: rule
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

You should not ignore exceptions. It can be tempting to be lazy when catching exceptions and do something like this: (see example below).

Developers should avoid this. In almost all cases, it’s inappropriate to catch generic Exception or Throwable (preferably not Throwable because it includes Error exceptions). It’s dangerous because it means that exceptions you never expected (including runtime exceptions like ClassCastException) get caught in app-level error handling. It obscures the failure- handling properties of your code, meaning if someone adds a new type of exception in the code you’re calling, the compiler won’t point out that you need to handle the error differently. In most cases you shouldn’t be handling different types of exceptions in the same way.

The rare exception to this code insight is test code and top-level code where you want to catch all kinds of errors (to prevent them from showing up in a UI, or to keep a batch job running). In these cases, you may catch generic Exception (or Throwable) and handle the error appropriately. Think carefully before doing this, though, and put in comments explaining why it’s safe in this context.

# **How we detect**

CAST Highlight counts one occurrence each time a catch instruction is dealing with generic exception type : *Throwable* and *Exception*.

```
 try {
someComplicatedIOFunction(); // may throw IOException
someComplicatedParsingFunction(); // may throw ParsingException
someComplicatedSecurityFunction(); // may throw SecurityException
// phew, made it all the way
} catch (Exception e) { // I'll just catch all exceptions
handleError(); // with one generic handler!
}
```

# **References**

<https://source.android.com/setup/contribute/code-style#dont-catch-generic-exception>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
