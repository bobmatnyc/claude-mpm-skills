---
title: Not all Tag libraries should be imported
url: https://doc.casthighlight.com/alt_uselessdependencies-avoid-useless-taglib/
slug: alt_uselessdependencies-avoid-useless-taglib
content_type: rule
languages: [java]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

A tag library defines a collection of custom actions. The tags can be used directly by developers in manually coding a JSP page, or automatically by Java development tools. A tag library must be portable between different JSP container implementations.  
If the tag library is not utilized, the custom actions are not defined resulting in specification issues

# **Business Impacts**

Having more tag libraries than necessary is risky for the code. It is best to only have tag libraries that are used so that the code can be more productive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://www.servletsuite.com/servlets/jscalltag.htm>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight establishes that only tag libraries that are being used in a page should be imported

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
