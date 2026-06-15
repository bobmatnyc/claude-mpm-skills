---
title: Standard SQL API increases Production Risk in JSP
url: https://doc.casthighlight.com/alt_sql-avoid-use-of-standard-sql-api/
slug: alt_sql-avoid-use-of-standard-sql-api
content_type: rule
languages: [sql, java]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Standard SQL API increases Production Risk in JSP

This code insight counts one violation if there is at least one import directive:

**<%@ page import = “java.sql.\*” %>**  
**<%@ page import = “javax.sql.\*” %>**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Standard SQL APIs java.sql.\* and javax.sql.\* are symptoms of direct access to tables.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
