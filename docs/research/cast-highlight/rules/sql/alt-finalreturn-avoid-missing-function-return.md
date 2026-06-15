---
title: RETURN should be used to terminate a database query or a stored procedure
url: https://doc.casthighlight.com/alt_finalreturn-avoid-missing-function-return/
slug: alt_finalreturn-avoid-missing-function-return
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The RETURN statement is useful as it terminates a query, stored procedure or batch.

When used in a stored procedure, the RETURN statement specifies an integer value to return to the calling application, batch, or procedure. If no value is specified then the stored procedure returns the value to 0. None of the statements in a stored procedure are executed after the RETURN statement is executed.

# **Business Impacts**

It is recommended to use the RETURN statement as the last instruction since it could be a risky move from a business standpoint.

One of the risks include decrease in Productivity if the RETURN statement was not used as a last instruction. Lack of a RETURN statement would cause the code to function improperly and result in a loss of time.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://sqlmag.com/t-sql/t-sql-control-flow-statements>

<https://technet.microsoft.com/en-us/library/ms187009(v=sql.105).aspx>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight verifies that the last instruction of a procedure or a function should be return. Depending on specific thresholds CAST has set to ensure that not using RETURN is not a too frequent pattern, Highlight counts penalty points to the given scanned file.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
