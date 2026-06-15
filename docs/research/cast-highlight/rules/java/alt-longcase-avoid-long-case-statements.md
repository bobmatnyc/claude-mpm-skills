---
title: Avoid long case statements
url: https://doc.casthighlight.com/alt_longcase-avoid-long-case-statements/
slug: alt_longcase-avoid-long-case-statements
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

The switch statement should be used only to clearly define some new branches in the control flow. As soon as a case clause contains too many statements this highly decreases the readability of the overall control flow statement. In such case, the content of the case clause should be extracted into a dedicated method.

# **How we detect**

CAST Highlight calculates the average lentgh of all “case” blocks in a source file. Depending on some benchmark thresholds, this code insight will be triggered.

The length is expressed in number of lines. The first line taken into account is the line of the “case” keyword, and the last is the line of the last instruction.

# **References**

<https://rules.sonarsource.com/java/tag/brain-overload/RSPEC-1151>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
