---
title: JSP can handle exceptions
url: https://doc.casthighlight.com/alt_missingcatch-use-exception-catching-with-number-parsing-methods-while-loops-and-tab-access/
slug: alt_missingcatch-use-exception-catching-with-number-parsing-methods-while-loops-and-tab-access
content_type: rule
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

When writing a JSP code, coding errors can happen at any part of the code. When an error occurs, the file cannot be found causing an exception. Such exceptions included are Checked exceptions, Runtime exceptions, Errors.

JSP provides ways to handle exceptions such as specifying Error Page for each JSP and the JSP container invokes the error page whenever the error throws an exception. Different exception objects including retrieving Messages, Causes, Strings, StackTrace, and so forth.

# **Business Impacts**

It is recommended to use exception catching methods as it helps solve potential errors in the code thus reducing risks and increasing productivity in the code.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://www.tutorialspoint.com/jsp/jsp_exception_handling.htm>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows If some data is present outside their respective bounds, then crashes are avoided in the process.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
