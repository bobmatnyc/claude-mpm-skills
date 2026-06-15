---
title: Care must be taken while selecting a Candidate key as Primary
url: https://doc.casthighlight.com/alt_fetchinloop-avoid-cursors-inside-a-loop/
slug: alt_fetchinloop-avoid-cursors-inside-a-loop
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Candidate Key can be any column or a combination of columns that can qualify as a unique key in the database. There can be multiple Candidate keys in one table. Each candidate key can qualify as Primary Key.  
Primary Key is a column or combination of columns that uniquely identify a record. Only one candidate key can be a primary key.  
There has be care taken in selecting the Primary Key as an incorrect selection can have negative impact on the database architect and future normalization.  
A candidate key should be Non-NULL and unique in any domain to qualify as a Primary Key

# **Business Impacts**

It is recommended to take care when using candidate keys as failing to so can result in adding risks and lack of productivity to a program.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://stackoverflow.com/questions/34303878/what-is-the-candidate-key-in-sql-server>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that in a relational database design, a candidate key is just a unique identifier. Next a primary key is a candidate key that’s been singled out to uniquely identify each row in a table.  
A unique key or primary key comprises a single column or set of columns. No two distinct rows in a table can have the same value (or combination of values) in those columns.  
Depending on its design, a table may have arbitrarily many unique keys but at most one primary key.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
