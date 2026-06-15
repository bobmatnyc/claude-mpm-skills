---
title: JSP standard is XML-compliant but certain elements cannot be mixed causing agility issues
url: https://doc.casthighlight.com/alt_heterogeneouscode-do-not-mix-jsp-standard-syntax-with-jsp-xml-syntax/
slug: alt_heterogeneouscode-do-not-mix-jsp-standard-syntax-with-jsp-xml-syntax
content_type: rule
languages: [php]
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/Code-Readability/)

# **Why you should care**

Mixing JSP standard syntax and JSP XML syntax is considered somewhat common as much of the standard JSP syntax is already XML-compliant including all the standard actions. However there are certain elements that are not compliant with an XML syntax. Such elements include Comments where Standard Syntax comments are written as <%– and XML syntax comments are written as <!–. Mixing up those elements can cause readability and agility issues which can result in software that is bug and error prone.

# **Business Impacts**

It is recommended to take care when mixing JSP standard and XML syntax because over-mixture can cause agility issues which results in greater costs and waste of resources.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends establishing an internal standard for code commenting. Ensuring that each application and their corresponding development team has a unified style guide, in order to standardize the type and commonality of comments.

Developers and project leaders should think about what portions of their codebase may require effort to understand and make appropriate, meaningful additions.  Nonetheless, they should avoid superfluous additions to sections that are self-explanatory. And finally there should be an emphasis on writing comments alongside the development process, rather than after the fact.

# **References**

https://wiki.php.net/rfc/group\_use\_declarations

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows the purpose of Readability

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
