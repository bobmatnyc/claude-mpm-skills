---
title: Mixing DDL & DML operations can cause recompilation
url: https://doc.casthighlight.com/alt_sqlinterleaving-avoid-ddl-and-dml-interleaving/
slug: alt_sqlinterleaving-avoid-ddl-and-dml-interleaving
content_type: rule
languages: [sql]
category: Transferability
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

Developers do not recommend mixing DDL and DML Operations. They are generally avoided because such mxing can cause a Recompile which results in resetting the code differently and causing a mess in the process. It is recommended to place all DDL statements at the top of the stored procedures and perform the necessary query work.

# **Business Impacts**

It is advised that DML and DDL operations should not be mixed as they can slow down the innovative qualities of the code and cause loss of time. It also makes it unsuitable for clients to utilize a slower version of an otherwise well written code.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://ubitsoft.com/help_19/html/6aad3a30-a429-4e4c-bbb8-2ef1a0fef14e.htm>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight establishes that functions, procedures and triggers should not have too many parameters. Depending on thresholds observed in the benchmark of thousands of applications and billions lines of code, Highlight accounts penalty points to the given scanned files.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
