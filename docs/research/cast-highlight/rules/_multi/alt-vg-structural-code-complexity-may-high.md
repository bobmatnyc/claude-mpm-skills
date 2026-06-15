---
title: Structural code complexity may be too high
url: https://doc.casthighlight.com/alt_vg-structural-code-complexity-may-high/
slug: alt_vg-structural-code-complexity-may-high
content_type: rule
category: Transferability
has_code_examples: false
---

## **Structural code complexity may be too high**

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

This code insight – derived from Tom McCabe’s Cyclomatic Complexity – estimates the level of strutural complexity of a piece of source code by counting and summing the total number of logical conditions (if, while, for, case, default), functions and methods. Depending on specific thresholds CAST has developed for each technology, Highlight counts penalty points for the scanned file.

### **Why you should care**

Code complexity is the “arthritis” of software.  If not managed by your development teams, it can quickly impact many aspects of your applications such as: a) maintainability; b) the ability to add new features because the underlying code foundation is just too complex; and c) the testability and the corresponding QA effort.

More importantly, it is generally agreed that a high level of code complexity correlates with the number of introduced software defects, since it’s very difficult for a developer to decipher many conditions at the same time while modifying a code base.

Long story short, software complexity is error-prone and means higher maintenance and test costs.

References:  
<https://en.wikipedia.org/wiki/Cyclomatic_complexity>  
<http://www.drdobbs.com/architecture-and-design/measuring-complexity-correctly/240007928>  
<https://dzone.com/articles/measuring-code-complexity>  
<https://dzone.com/articles/code-complexity-is-killing-us>

### **CAST recommendations**

Although code complexity could be considered as part of the software entropy (software quality tends to naturally decreases over time), it is also part of your technical debt. You should ensure your team takes care of controlling structural complexity overy time by  regularly refactoring the most complex parts of your source code.

[How it works](http://casthighlight.wpengine.com/how-it-works/)[Features & Analytics](http://casthighlight.wpengine.com/outputs-analytics/)
