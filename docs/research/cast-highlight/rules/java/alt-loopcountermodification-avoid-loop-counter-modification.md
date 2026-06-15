---
title: Avoid loop counter modification
url: https://doc.casthighlight.com/alt_loopcountermodification-avoid-loop-counter-modification/
slug: alt_loopcountermodification-avoid-loop-counter-modification
content_type: rule
languages: [java]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Loop counters shall not be modified in the body of the loop. However other loop control variables representing logical values may be modified in the loop, for example a flag to indicate that something has been completed, which is then tested in the for statement.

# **How we detect**

CAST Highlight counts one occurrence each time a “for” loop has its loop counter modified inside its body.

**Bad Code**

```
flag = 1;
for ( i = 0; (i < 5) && (flag == 1); i++ ) {
/* ... */
i = i + 3; /* loop counter updated */
}
```

**Good Code**

```
flag = 1;
for ( i = 0; (i < 5) && (flag == 1); i++ ) {
/* ... */
flag = 0; /* not the loop counter */
}
```

# **References**

<http://caxapa.ru/thumbs/468328/misra-c-2004.pdf>  
<https://rules.sonarsource.com/java/RSPEC-127>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
