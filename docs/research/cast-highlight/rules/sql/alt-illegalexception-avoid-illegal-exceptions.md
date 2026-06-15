---
title: Illegal exception occurs when user declares a standard exception.
url: https://doc.casthighlight.com/alt_illegalexception-avoid-illegal-exceptions/
slug: alt_illegalexception-avoid-illegal-exceptions
content_type: rule
languages: [sql]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

In PLSQL, an exception is a warning or a type of error condition. They can internally defined (by the run-time system) or user defined. An illegal exception occurs when a standard exception is declared by the user because such expressions are declared by PLSQL.

Having illegal expressions in the code can decrease code reliability which can cause the code to be prone to errors.

# **Business Impacts**

Illegal exceptions are highly risky to the code as they are considered to be a warning that needs to be addressed quickly. They cause the code to be greatly unproductive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://docs.oracle.com/cd/A97630\_01/appdev.920/a96624/07\_errs.htm

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight does not recommend declaring standard exceptions.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
