---
title: The code contains too many instructions that initialize zones of data with zeros or spaces
url: https://doc.casthighlight.com/alt_badinit-code-contains-many-instructions-initialize-zones-data-zeros-spaces/
slug: alt_badinit-code-contains-many-instructions-initialize-zones-data-zeros-spaces
content_type: rule
category: Changeability
has_code_examples: false
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

For code readability purpose, avoid initializations with 0 or spaces.

# **How we detect**

CAST Highlight counts one occurrence each time one of the following patterns are encountered in the *WORKING STORAGE* section:

- VALUE 0
- VALUE +0
- VALUE ‘ ‘ (string containing only blanks)
- PIC X(<length>) VALUE ‘<string>’, where the length of <string> is different from <length>
- MOVE 0
- MOVE +0
- MOVE ‘ ‘

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
