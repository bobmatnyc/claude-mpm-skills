---
title: The code contains too many “SELECT *” requests
url: https://doc.casthighlight.com/alt_complexquery-code-contains-many-select-requests/
slug: alt_complexquery-code-contains-many-select-requests
content_type: rule
category: Robustness
has_code_examples: false
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/software-elegance/)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity)

# **Why you should care**

A query that retrieves all columns of a table with a SELECT \* or SELECT SINGLE \* can potentially be the source of important performance problems: Such performance problems may arise when the execution of the query returns a large result sets (many row with all the columns may then become a huge amount of data to transport over the network). However, there are some exceptions with standard tables such as parameter tables.

Also, when using such queries, one cannot control how the columns will be ordered and returned to the client. This can lead to important data inconsistencies and thus stability issues.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Limit the number of field selected by naming those which are expecting only.

# **How we detect**

This Code Insight counts one occurrence each time a “SELECT \*” or “SELECT SINGLE \*” query is found.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
