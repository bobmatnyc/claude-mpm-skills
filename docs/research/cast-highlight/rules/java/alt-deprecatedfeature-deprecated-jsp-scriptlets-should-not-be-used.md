---
title: Deprecated features makes code less resilient
url: https://doc.casthighlight.com/alt_deprecatedfeature-deprecated-jsp-scriptlets-should-not-be-used/
slug: alt_deprecatedfeature-deprecated-jsp-scriptlets-should-not-be-used
content_type: rule
languages: [java, javascript]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Deprecated features are usable but should not be used because they are expected to be removed entirely in the near-future and placing them in the code can cause potential bugs and be less resilient.

# **Business Impacts**

Deprecated features are considered to be highly risky and unproductive in nature since they are considered to be obsolete which can cause potential bugs in the code. Bugs are equivalent to lack of productivity which makes the code less resilient in the long run.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Deprecated_and_obsolete_features>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that JSP scripts have been deprecated because they:  
Are not unit testable.  
Are not reusable.  
Cannot make use of object oriented concepts such as inheritence.  
Have poor error handling capabilities: if an exception is thrown, an empty page is rended.  
Mix the business and presentation logic.  
JSP Standard Tag Library (JSTL) and Expression Language should be used instead, enabiling the adoption of the model-view-controller (MVC) design pattern which reduces the coupling between the presentation tier and the business logic.  
Noncompliant Code Example  
< input name =””foo”” type=””text”” value=””<%=” />” />  
Compliant Solution  
< input name =””foo”” type=””text”” value=””${fn:escapeXml(param.foo)}”” />  
http://nemo.sonarqube.org/coding\_rules#languages=web|tags=jsp-jsf

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
