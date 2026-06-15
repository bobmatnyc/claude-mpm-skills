---
title: Multiple lines makes code harder to read
url: https://doc.casthighlight.com/alt_multilinestring-avoid-multiline-string-literals/
slug: alt_multilinestring-avoid-multiline-string-literals
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Having multiple lines as one line of code remarkably decreases readability of the code. This makes the source code tougher to understand, and execute, causing it to more error prone and susceptible to bugs in the near-future.

# **Business Impacts**

Combining multiple lines of code on one line is risky because it makes the code unreadable and less productive in the long run.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://softwareengineering.stackexchange.com/questions/104066/single-line-statements-good-practices>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that the whitespace at the beginning of each line can’t be safely stripped at compile time;  
whitespace after the slash will result in tricky errors;  
and while most script engines support this, it is not part of ECMAScript.  
Use string concatenation instead.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
