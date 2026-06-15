---
title: "A Program, User-Exit or Include contains too many Open SQL queries that access SAP standard tables in modification"
url: https://doc.casthighlight.com/alt_standardtablemodification-program-user-exit-include-contains-many-open-sql-queries-access-sap-standard-tables-modification/
slug: alt_standardtablemodification-program-user-exit-include-contains-many-open-sql-queries-access-sap-standard-tables-modification
content_type: rule
languages: [abap, sql]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

SAP standard tables are part of the SAP software and they must not be modified by custom components. These can be affected by the modification of the SAP system tables, in terms of structure, content or business rules. In addition, they can lead to data corruption and unpredictable behavior of SAP packages. The best way is to use standard functions and badis released by SAP.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

You should call SAP standard functions and badis to modify the content of SAP standard tables.

# **How we detect**

This Code Insight counts one occurrence each time an OpenSQL query is found accessing a standard table in modification from a custom program, a user-exit, an include, a function or a method.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
