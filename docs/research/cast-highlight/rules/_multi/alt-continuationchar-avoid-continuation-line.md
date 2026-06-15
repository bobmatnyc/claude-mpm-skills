---
title: Avoid Backslash to continue command
url: https://doc.casthighlight.com/alt_continuationchar-avoid-continuation-line/
slug: alt_continuationchar-avoid-continuation-line
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/Code-Readability/)

# **Why you should care**

With line-oriented text, the backslash is used at the end of a line to indicate that the trailing newline character is to be ignored. In other words, with the backslash, the following line belongs on the same line as the line prior. As in they are both on the same line as a “continuation”.

Unfortunately, this equivalent to adding multiple instructions on the same line which results in causing readability issues and a harder code to understand as well as possible bugs in the code.

# **Business Impacts**

Utilizing backslash can make the code less readable and less understandable when having commands continued on the next line. It adds risk and reduces productivity.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://stackoverflow.com/questions/7711745/what-does-backslash-means-at-the-end-of-line>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight suggests to avoid utilizing the blackslash in order continue the command on the next line.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
