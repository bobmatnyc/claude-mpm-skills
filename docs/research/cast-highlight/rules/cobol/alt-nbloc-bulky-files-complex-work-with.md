---
title: Bulky files are complex to work with
url: https://doc.casthighlight.com/alt_nbloc-bulky-files-complex-work-with/
slug: alt_nbloc-bulky-files-complex-work-with
content_type: rule
languages: [cobol, java]
category: Efficiency
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/software-elegance/)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

Having too large source files could be compared to looking for a needle in a haystack. If developers have to massively scroll down to go to the portion of code they want to fix or to add a new functionality, it costs time and energy. Although there’s no ideal number of lines of code, it is generally accepted by software engineers that a fine-grained file base improves maintenance activities efficiency and reduces software complexity.

# **Business Impacts**

Developer time and effort may be higher when they are required to search and understand large source files. This can also impact the ability for a development team to debug in a time effective manner, since there is a larger portion of code to comb through.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/)[Time / Effort](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Although code refactoring may not be required in all cases, you may a) consider splitting some of your largest file artifacts or; b) inquiring if the development team can create the same functionality, but with less code.

# **References**

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts the total code lines that contain instructions or decorators (comments and docstring excluded) in a source file. Depending on the value and the technology being scanned (procedural COBOL programs are generally more voluminous than oriented-object Java files), Highlight counts penalty points contributing to the Software Elegance health factor if the source file exceeds a specific length limit.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See Features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
