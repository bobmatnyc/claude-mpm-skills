---
title: A Return Statement in the middle of a command makes it unreadable
url: https://doc.casthighlight.com/alt_withreturnoutsideexceptionhandler-avoid-returning-from-routine-before-the-end/
slug: alt_withreturnoutsideexceptionhandler-avoid-returning-from-routine-before-the-end
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

The RETURN statement is useful as it terminates a query, stored procedure or batch. 

When used in a stored procedure, the RETURN statement specifies an integer value to return to the calling application, batch, or procedure. If no value is specified then the stored procedure returns the value to 0. None of the statements in a stored procedure are executed after the RETURN statement is executed.

Having a RETURN statement in the middle of the procedure or function results in the values of the procedure or function, after the statement, to not be returned and executed.

# **Business Impacts**

Having the RETURN statement in the middle of the command makes rest of the code unproductive. Lack of a RETURN statement would cause the code to function improperly and result in a loss of time.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://technet.microsoft.com/en-us/library/ms187009(v=sql.105).aspx>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight ensures that the return statement should be at the end of a procedure or function should always be the last instruction.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
