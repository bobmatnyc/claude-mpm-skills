---
title: CASE cannot be an instruction without a WHEN clause
url: https://doc.casthighlight.com/alt_missingwhenothers-the-code-contains-too-many-case-instructions-with-missing-default-statement-when-other/
slug: alt_missingwhenothers-the-code-contains-too-many-case-instructions-with-missing-default-statement-when-other
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

The PLSQL CASE has similar functionality of an IF-THEN-ELSE statement. The CASE statement evaluates a single expression and expresses it against several potential values or evaluates Boolean Values while choosing the first one that is TRUE.  
WHEN clauses are executed in order. WHEN clauses is executed only once. Without a WHEN clause the CASE statement generally does not end, or not fully executed causing errors.

# **Business Impacts**

It is recommended to have CASE be utilized with a WHEN clause so that there are less risks in the code and is more productive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://docs.oracle.com/cd/E19159-01/819-3669/bnalq/index.html

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that each case instruction should have a default clause.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
