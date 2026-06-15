---
title: Artifacts and Subqueries decrease code agility
url: https://doc.casthighlight.com/alt_subqueries-avoid-artifacts-with-sql-statement-including-subqueries/
slug: alt_subqueries-avoid-artifacts-with-sql-statement-including-subqueries
content_type: rule
languages: [sql]
category: Efficiency
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/Code-Readability/)

# **Why you should care**

Having Complex queries in SQL Artifacts lead to causing performance problems and decrease in code agility. Subqueries are considered to be complicated in nature.

# **Business Impacts**

Complex queries are not recommended as they reduce code agility thereby increasing costs.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Subqueries are generally considered fine unless they are dependent subqueries therefore it is recommended for developers to use independent subqueries with appropriate indexes.

A subquery is independent if it can be run without context and those should be used for added performance.

# **References**

<https://www.appmarq.com/public/efficiency,4772,Avoid-SQL-Artifacts-with-SQL-statement-including-Subqueries-JEE>

<https://stackoverflow.com/questions/4799820/when-to-use-sql-sub-queries-versus-a-standard-join>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that artifacts should not use SQL statements including subqueries or at the very least subqueries should be avoided.

# **Cloud Readiness**

Complexity - SQL Queries

**Ineffective Interprocess Communications:** Utilizing complex subqueries in SQL causes complications during cloud migration as the database application could constrained by physical machines which might using other services.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
