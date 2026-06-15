---
title: Empty Catches cause code errors & unreliability
url: https://doc.casthighlight.com/alt_emptycatches-avoid-empty-catch-blocks-php/
slug: alt_emptycatches-avoid-empty-catch-blocks-php
content_type: rule
languages: [php]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

When an exception occurs during programming, it is usually caught in a catch block. Empty catch is when an exception occurs but the program fails because nothing occurs. As a result, they are a common source for obtaining errors in the code, and then executing these errors. It is also inefficient since it catches nothing and executes nothing.

# **Business Impacts**

Empty catch blocks are considered a risk from a business perspective as it can pose security issues. Risks can involve programmers and/or the company are unaware of the security being compromised.

[Security Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST Recommends enforcing a Style Guide for the company that strongly suggests avoiding the use of empty-catch blocks to solve a problem in the code.  Instead teams should be encouraged to collaborate and work on the problem together through communication.

# **References**

<https://stackoverflow.com/questions/1234343/why-are-empty-catch-blocks-a-bad-idea>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that catching an exception provides robustness treatment or error management. A catch doing nothing can masks an error, allowing the program to pursue and ignore the problem.

# **Cloud Readiness**

[Versions & Deprecated Code](#)

**Ineffective use of the provided stack:** Having an empty catch in the program can mask errors that can misinterpreted when migrating to the cloud.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
