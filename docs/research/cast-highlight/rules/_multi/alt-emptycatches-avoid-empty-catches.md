---
title: Empty Catches may cause security risks
url: https://doc.casthighlight.com/alt_emptycatches-avoid-empty-catches/
slug: alt_emptycatches-avoid-empty-catches
content_type: rule
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Most developers contend that it’s not ideal to have an empty catch block. Empty Catch is the cause of an exception occurring where nothing happens and the program fails. When such an exception occurs, it can be thrown up to the caller, or caught in catch block. Usually its considered to be flawed programming practice when an empty catch occurs. It can result in exposing a stack trace or maybe even a security risk.

# **Business Impacts**

Empty catch blocks are considered a risk from a business perspective as it can pose security issues. Risks can involve programmers and/or the company are unaware of the security being compromised.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

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
