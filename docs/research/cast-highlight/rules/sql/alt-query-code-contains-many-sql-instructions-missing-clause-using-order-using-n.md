---
title: "The code contains too many SQL instructions with a missing where clause, or using “order by”, or using “not” operator or “is null” check in a where clause"
url: https://doc.casthighlight.com/alt_query-code-contains-many-sql-instructions-missing-clause-using-order-using-not-operator-null-check-clause/
slug: alt_query-code-contains-many-sql-instructions-missing-clause-using-order-using-not-operator-null-check-clause
content_type: rule
languages: [sql, abap]
category: Efficiency
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

For reliability and performance purposes, avoid using too many SQL instructions with a missing WHERE clause. Also, using “ORDER BY”, “NOT LIKE” or “IS NULL” in a WHERE clause is not recommended.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

- **NOT LIKE operator in WHERE clauses**: A NOT LIKE operator in a WHERE clause does not allow to use database indexes and has an impact in terms of performance. It is better to invert the logical expression in data selection. If possible, avoid using the NOT operator in the WHERE clause because it is not supported by database indexes; invert the logical expression instead.
- **IS NULL in WHERE clauses**: Some addition automatically bypass buffer. Bypassing buffer means that SELECT will not go to buffered results but always directly to the database. This can impact the performance significantly. Check if the IS NULL addition is really necessary and use this addition carefully.
- **ORDER BY in WHERE clauses**: The ORDER BY clause is executed on the database server while the ABAP SORT statement is executed on the application server. The database server will usually be the bottleneck so, for performance reason, it is often better to move the sort from the database server to the application server. If you are not sorting by the primary key ( E.g. using the ORDER BY PRIMARY key statement) but are sorting by another key, it could be better to use the ABAP SORT statement to sort the data in an internal table. Note however that for very large result sets it might not be a feasible solution and you would want to let the database server sort it.
- **SQL queries with missing WHERE clauses**: To reduce the number of data records to be transferred, for each SQL statement you must specify a WHERE clause that is as selective as possible. A SELECT statement without a WHERE condition is an indication of a design error in the program

# **How we detect**

This Code Insight counts one occurrence each time an SQL query is found with a missing WHERE clause, or NOT LIKE or IS NULL or ORDER BY are found in a WHERE clause.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
