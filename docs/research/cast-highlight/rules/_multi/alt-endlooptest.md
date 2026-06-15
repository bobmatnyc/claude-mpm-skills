---
title: Avoid equality in loop termination condition
url: https://doc.casthighlight.com/alt_endlooptest/
slug: alt_endlooptest
content_type: rule
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Testing for loop termination using an equality operator (== and !=) is dangerous, because it could set up an infinite loop. Using a broader relational operator instead casts a wider net, and makes it harder (but not impossible) to accidentally write an infinite loop.

# **How we detect**

CAST Highlight counts one occurrence each time a loop (for or while) use an equality in its termination condition, except for comparisons to NULL.

An equality is an expression using an operator == or !=

**Bad Code**

```
for (int i = 1; i != 10; i += 1) {
  //...
}
while (i != 10) {
  //...
}
```

**Good Code**

```
for (int i = 1; i < 10; i += 1) {
  //...
}
while (i != null) {
  //...
}
```

# **References**

<http://cwe.mitre.org/data/definitions/835>  
<https://wiki.sei.cmu.edu/confluence/display/c/MSC21-C.+Use+robust+loop+termination+conditions>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
