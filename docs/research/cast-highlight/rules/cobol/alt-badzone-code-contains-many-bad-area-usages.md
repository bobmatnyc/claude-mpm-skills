---
title: The code contains too many bad area A usages
url: https://doc.casthighlight.com/alt_badzone-code-contains-many-bad-area-usages/
slug: alt_badzone-code-contains-many-bad-area-usages
content_type: rule
languages: [cobol]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

In a cobol file, area A (the first four columns) are reserved for divions, sections names, paragraph names and level 01 data declaration.

# **How we detect**

CAST Highlight counts one occurrence each time one of these patterns are detected in source code:

- a 01 level data is declared outside area A.(first four columns are empty
- a 88 level data is inside area A. (the fours columns are not empty)
- one of the following instruction is found in area A: **COPY, IF, AND, SET, MOVE, DIVIDE, READ, ADD, WRITE, MULTIPLY, PERFORM, OPEN, CLOSE, WHEN, EVALUATE, EXEC, INITIALIZE, GO TO**

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
