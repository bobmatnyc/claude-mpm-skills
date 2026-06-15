---
title: The code contain too many unused private methods
url: https://doc.casthighlight.com/alt_unusedprivatemethods-code-contain-many-unused-private-methods/
slug: alt_unusedprivatemethods-code-contain-many-unused-private-methods
content_type: rule
languages: [kotlin]
category: Transferability
has_code_examples: true
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/software-elegance/)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

Private methods that are never executed are dead code: unnecessary, inoperative code that should be removed. Cleaning out dead code decreases the size of the maintained codebase, making it easier to understand the program and preventing bugs from being introduced.

# **How we detect**

CAST Highlight counts one occurrence each time a private method is never used.

```
class toto {

private fun meth1() { // +1 VIOLATION : meth1 is never used
val newSourcePath = projectRoot.resolve("src/${asRelativePath()}").canonicalFile.invariantSeparatorsPath
return 0
}

private fun asRelativePath(): String = // +0 VIOLATION : asRelativePath is used by the method meth1
if (scope.isBlank()) name else scope.replace('.', '/') + '/' + name

}
```

# **References**

<https://rules.sonarsource.com/kotlin/RSPEC-1144>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
