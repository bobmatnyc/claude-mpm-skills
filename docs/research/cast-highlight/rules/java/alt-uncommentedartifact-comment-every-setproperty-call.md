---
title: Commenting on setProperty() method allows for software to be resilient
url: https://doc.casthighlight.com/alt_uncommentedartifact-comment-every-setproperty-call/
slug: alt_uncommentedartifact-comment-every-setproperty-call
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

setProperty() method interface sets a new value for a property on a CSS declaration object. Without commenting on the setProperty() method, it is left ambigous which is not ideal for good programming practice causing reliability issues which can result in an error prone software.

# **Business Impacts**

It is recommended to comment on setProperty() methods and other methods to ensure the code is less prone to risks and is more productive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://developer.mozilla.org/en-US/docs/Web/API/CSSStyleDeclaration/setProperty

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight focuses on JSP technology to provide a convenient element which initializes all PropertyDescriptor-identified properties of a JavaBeans component. For instance:

However, this should be used with caution. First, if the bean has a property, say, amount, and there is no such parameter (amount) in the current ServletRequest object or the parameter value is “”, nothing is done: the JSP page does not even use null to set that particular property of the bean. So, whatever value is already assigned to amount in the bankClient bean is unaffected. Second, non-elementary properties that do not have PropertyEditors defined may not be implicitly initialized from a String value of the ServletRequest object and explicit conversion may be needed. Third, malicious users can add additional request parameters and set unintended properties of the bean, if the application is not carefully designed.

If you still prefer to use property=”\*” in the jsp:setProperty tag for the purpose of producing neater code, then we recommend that you add a comment preceding the jsp:setProperty tag about parameters expected to be present in the ServletRequest object to initialize the bean. So, in the following example, from the comment we know that both firstName and lastName are required to initialize the bankClient bean:  
<%– – requires firstName and lastName from the ServletRequest –%>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
