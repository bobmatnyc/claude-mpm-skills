---
title: The code contains too many queries leading to a high number of table columns
url: https://doc.casthighlight.com/alt_numberofcolumns-code-contains-many-queries-leading-high-number-table-columns/
slug: alt_numberofcolumns-code-contains-many-queries-leading-high-number-table-columns
content_type: rule
languages: [sql]
category: Efficiency
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Complex select clauses, i.e select clauses with many column can be difficult to read and does not help the reader who needs to identify the relevant columns to be retrieved. Also a query that retrieves many columns can potentially cause performance problems: Such performance problems may arise when the execution of the query returns a large result sets (many row with many colums may then become a huge amount of data to transport over the network).

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Avoid Artifacts with a SELECT clause returning more than 9 columns, with a ‘SELECT \*’ query or with a ‘SELECT ALL’ query for Artifacts. Such queries are considered complex. Review the SELECT statement to reduce the number of selected columns.

# **How we detect**

This Code Insight counts one occurrence each time an SQL query on more than 9 tables or a “SELECT \*” are detected.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
