---
title: Incomplete JSP fragments can cause readability errors.
url: https://doc.casthighlight.com/alt_filelocation-jsp-fragments-should-always-be-placed-in-web-infjspf/
slug: alt_filelocation-jsp-fragments-should-always-be-placed-in-web-infjspf
content_type: rule
languages: [php]
category: Transferability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

JSP fragments are a portion of a JSP code passed to a tag handler so it can be invoked as many times as required. They can be considered as a template that is used by a tag handler to produce customized content. A fragment attribute is evaluated by a tag handler during tag invocation unlike a simple attribute which is evaluated by the container. One can define the value of a fragment attribute by using a .jsp attribute element.

However when JSP fragments are left incomplete, they cannot be made accessible for client browsers as it can cause readability issues and a symptom for flawed programming practices

# **Business Impacts**

Incomplete JSP fragments are risky because they do present improper programming practice which will be greatly unappealing to potential clients.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://docs.oracle.com/cd/E19159-01/819-3669/bnalq/index.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows JSP fragments that are not complete pages should not be made not accessible for client browsers.  
But : it is a polemic diag, as explained here : “Some people also believe in putting them under the WEB-INF folder, so that they’re not accessible via a URL. I see no good reason to go to this extreme, since there’s no way to discover their existence from outside of the app-server. On the other hand, there’s a decided maintainability benefit to keeping refactored fragments together with their including file.”  
http://www.kdgregory.com/index.php?page=jsp.refactoring

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
