---
title: Pure JSP Comments can decrease Costs
url: https://doc.casthighlight.com/alt_jspcomment-prefer-pure-jsp-comments/
slug: alt_jspcomment-prefer-pure-jsp-comments
content_type: rule
languages: [python, java]
category: Changeability
has_code_examples: false
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Pure JSP Comments can decrease Costs

This code insight counts one violation each time a scriptlet contains only java comments.

This includes for example the following patterns :

**<% /\*\* … \*/ %>**  
**<% /\* … \*/ %>**  
**<% // … %>**

Including cases with several comments:

**<% /\* … \*/** **/\* … \*/****%>**

And of course cases using XML format tags:

**<jsp:scriptlet> /\* …\*/ </jsp:scriptlet>**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Java comments are for commenting java code. If a JSP scriptlet contains no java code, then no java comment is needed. A scriptlet containing only java comment is symptomatic of :

- a comment aiming to produce documentation at JSP script level. In this case a JSP comment would be more appropriated.
- a commented out java code: this is a bad practice because useless code should be removed.

so <%– … %> is prefered to

<% /\*\* … \*/ %>  
<% /\* … \*/ %>  
<% // … %>

## **Business Impacts**

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/readability/Avoid%20%22non-Pythonic%22%20attribute%20names/3ueqPTsn

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
