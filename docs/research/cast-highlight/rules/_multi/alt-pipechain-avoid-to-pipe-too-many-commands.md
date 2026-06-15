---
title: Too many pipe commands cause inefficiency
url: https://doc.casthighlight.com/alt_pipechain-avoid-to-pipe-too-many-commands/
slug: alt_pipechain-avoid-to-pipe-too-many-commands
content_type: rule
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Having too many pipe commands could result in code inefficiency as well as possible entry of bugs and crashes in the code due to increased stringing and redirections as a result.

# **Business Impacts**

Using pipes in a program can be a risky decision as it tends to be wasteful in both time and productivity. Using more pipes will further decrease productivity as well.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://www.tutorialspoint.com/unix/unix-pipes-filters.htm>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that while piping commands are useful, they should be avoided if too many of them exist.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
