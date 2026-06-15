---
title: Semicolon is used to terminate statement
url: https://doc.casthighlight.com/alt_withoutsemicolumn_end_semicolon-used-terminate-statement/
slug: alt_withoutsemicolumn_end_semicolon-used-terminate-statement
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Semicolons are utilized in PLSQL to terminate a statement. Without it the statement is not terminated and sends back an error.

# **Business Impacts**

Semicolons are essential to any code that runs a working program. Without it, the code does not work.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://www.toadworld.com/platforms/oracle/w/wiki/1767.plsql-semicolon-delimiter-plf4>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that END instructions should be terminated with semicolon.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
