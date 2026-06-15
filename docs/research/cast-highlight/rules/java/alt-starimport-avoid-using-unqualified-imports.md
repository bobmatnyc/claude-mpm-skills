---
title: A static or unqualified import is harmful to readability.
url: https://doc.casthighlight.com/alt_starimport-avoid-using-unqualified-imports/
slug: alt_starimport-avoid-using-unqualified-imports
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

A static or unqualified report is found in the JSP which is analogous to normal import declaration. The report is unqualified after adding a star(\*) at the end of the import statement.  
However the issue with the unqualified report is that they make one’s program unreadable impacting all the members that are imported as well. All static or unqualified members from a class can be particularly harmful to readability.

# **Business Impacts**

A static or unqualified report is a risky contributor to a JSP script causing readability issues.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://docs.oracle.com/javase/8/docs/technotes/guides/language/static-import.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that having unqualified (i.e. imports finishing with .\*) means that potentially every Class in the Package imported could be accessed.  
Example of an unqualified import: Import com.castsoftware.product.\*

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
