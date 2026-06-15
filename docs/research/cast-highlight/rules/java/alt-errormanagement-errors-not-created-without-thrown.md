---
title: Errors should not be created without being thrown
url: https://doc.casthighlight.com/alt_errormanagement-errors-not-created-without-thrown/
slug: alt_errormanagement-errors-not-created-without-thrown
content_type: rule
languages: [java, javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Creating a new Error without actually throwing it is useless and is probably due to a mistake.

# **How we detect**

CAST Highlight counts one occurrence each time ‘*throw*‘ is not used before the ‘*new*‘ operator used to instanciate an error class (Error | EvalError | InternalError | RangeError | ReferenceError | SyntaxError | TypeError | URIError).

**Bad Code**

```
if (x < 0) {
  new Error("x must be nonnegative");
}
```

**Good Code**

```
if (x < 0) {
  throw new Error("x must be nonnegative");
}
```

# **References**

<https://developer.mozilla.org/fr/docs/orphaned/Web/JavaScript/Reference/Global_Objects/Error>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
