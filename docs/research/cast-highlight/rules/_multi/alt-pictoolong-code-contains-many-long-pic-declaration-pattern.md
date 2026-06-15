---
title: The code contains too many long PIC declaration pattern
url: https://doc.casthighlight.com/alt_pictoolong-code-contains-many-long-pic-declaration-pattern/
slug: alt_pictoolong-code-contains-many-long-pic-declaration-pattern
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

While describing a PICTURE, once the length of a sequence exceeds 3 characters, use the factorized notation. Edition pictures (presence of Z) are not concerned.

# **How we detect**

CAST Highlight counts one occurrence each time in the WORKING SECTION a PICTURE description not containing “Z” exceed sequences of more than three characters. In the following patterns, where sequences do not contain parentheses:

- PIC <sequence 1>
- PIC S<sequence 1>
- PIC <sequence 1>V<sequence 2>
- PIC S<sequence 1>V<sequence 2>

The length of *<sequence 1>* and *<sequence 2>* (if any) should not exceed 3 characters, excluding *s* if present.

Bad Code

```
PIC 9999
PIC 9999V9
PIC s9999V9
PIC XXXX
```

Good Code

```
PIC 9(4)
PIC 9(4)V9 
PIC s9(4)V9
PIC X(4)
PIC s999
PIC 9(7)V99999999999
```

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
