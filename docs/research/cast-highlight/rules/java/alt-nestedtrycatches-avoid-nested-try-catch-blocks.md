---
title: Avoid nested try-catch blocks
url: https://doc.casthighlight.com/alt_nestedtrycatches-avoid-nested-try-catch-blocks/
slug: alt_nestedtrycatches-avoid-nested-try-catch-blocks
content_type: rule
languages: [java]
category: Robustness
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Although this is sometimes unavailable, nesting try/catch blocks severely impacts the readability of the source code as it makes it difficult to understand which block will catch which exception.

# **How we detect**

CAST Highlight counts one occurrence each time a try block contains one or more nested other try.

**Bad Code**

```
try {
  // some stuff
  // ....
  if (toto) {
    try {         // ===> VIOLATION
      // another stuff
      // ...
    }
    catch (Exception e) {
      throw e;
    }
  }
}
catch (Exception e) {
  throw e;
}
```

**Good Code**

```
try {
  // some stuff
  // ....
}
catch (Exception e) {
 throw e;
}
if (toto) {
  try {
    // another stuff
    // ...
  }
  catch (Exception e) {
     throw e;
  }
}
```

# **References**

<https://softwareengineering.stackexchange.com/questions/118788/is-using-nested-try-catch-blocks-an-anti-pattern>  
<https://rules.sonarsource.com/java/RSPEC-1141>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
