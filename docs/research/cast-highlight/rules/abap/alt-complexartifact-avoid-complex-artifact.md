---
title: SELECT clauses with many columns tend to be complex in nature.
url: https://doc.casthighlight.com/alt_complexartifact-avoid-complex-artifact/
slug: alt_complexartifact-avoid-complex-artifact
content_type: rule
languages: [abap, sql]
category: Efficiency
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

Artifacts with a SELECT clause tend to be complex in nature as SELECT clauses with many clauses are difficult to read and does not help the reader in identifying the columns that can be retrieved. Also a query that retrieves many columns can potentially cause performance problems as such performance problems may arise when the query is executed.

# **Business Impacts**

It is recommended to avoid complex artifacts in the code as their complex nature can result in loss of time and slow down the innovative capabilities of the code.  
These factors can make the code unsuitable for clients.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Instead of using SELECT, every column to be used in the query, should be explicitly listed while using a table alias.

For Example –

SELECT column1, column2, column3.  FROM TABLE

instead of

SELECT \* FROM TABLE

# **References**

<https://www.appmarq.com/public/efficiency,7108,Avoid-Artifacts-with-a-Complex-SELECT-Clause-ABAP>

<http://mansriva.blogspot.com/2014/12/sqlpl-sql-coding-standards-guidelines.html>

<https://stackoverflow.com/questions/3639861/why-is-select-considered-harmful>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight focuses on how functions, procedure and triggers should not have a too high cyclomatic complexity

# **How we detect**

Complexity - SQL Queries

**Ineffective Interprocess Communications:** Utilizing SELECT \* in SQL can create technical issues during the cloud migration process as the database application could constrained by physical machines which might using other services.  It can also disrupt the application when accessing it from the cloud.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
