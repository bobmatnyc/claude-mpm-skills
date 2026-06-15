---
title: Aliases can complicate and hide commands that hamper resiliency
url: https://doc.casthighlight.com/alt_alias-avoid-using-aliases/
slug: alt_alias-avoid-using-aliases
content_type: rule
languages: [sql]
category: Changeability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

An Alias is an alternative name or reference that can be defined in a T-SQL statement for use within that statement. They are not stored by the SQL server permanently. Usually they are one or two characters long and are not required in any part of the statement. However while they simplify syntax and improve readability, they can also complicate administration and takes a lot of joins in SQL to obtain a complete record which can be an issue in code reliability.

They can also hide commands that can resiliency issues as well

# **Business Impacts**

It is recommended to avoid using an alias as it masks commands which causes potential risks in the code that can lead to productivity issues.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

http://sqlmag.com/t-sql/aliases-t-sql

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight focuses on how aliases can hide dangerous or inappropriate commands. Prefer using the native command by specifying explicitly the options you need

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
