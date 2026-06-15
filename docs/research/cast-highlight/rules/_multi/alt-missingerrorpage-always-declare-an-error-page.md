---
title: Declaring errors prevents security risks
url: https://doc.casthighlight.com/alt_missingerrorpage-always-declare-an-error-page/
slug: alt_missingerrorpage-always-declare-an-error-page
content_type: rule
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Exception handling is the process in JSP to handle runtime errors. Any number of exceptions can arise when JSP page is executed. Without defining or declaring the errors, the error is not undeclared and is left unverified causing it have security risks and flawed resiliency which is not ideal for the code.

# **Business Impacts**

It is recommended to declare an error page so that the code has fewer security risks which boosts code resiliency.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://docs.oracle.com/cd/E19159-01/819-3669/bnalq/index.html  
https://docs.oracle.com/cd/E19316-01/819-3669/bnahi/index.html

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows while a thrown exception’s stack trace proves extremely useful for developers when debugging their code, it is rarely desirable to share an entire exception stack trace with the software’s users.  
Lengthy stack traces are not aesthetically pleasing and can increase security risks by exposing information that does not need to be released. JSPs allow developers to catch and handle exceptions in the code, resulting in more secure and aesthetically pleasing exception handling.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
