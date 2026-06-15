---
title: The code contains too many PHP4 deprecated constructor naming.
url: https://doc.casthighlight.com/alt_constructornaming-code-contains-many-php4-deprecated-constructor-naming-since-php5-constructor-named-__construct/
slug: alt_constructornaming-code-contains-many-php4-deprecated-constructor-naming-since-php5-constructor-named-__construct
content_type: rule
languages: [php]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Developers should avoid using deprecated constructors. Since PHP5, constructor should be named \_\_construct.

# **How we detect**

CAST Highlight counts one occurrence each time:

- a method has the name of the class
- the constructor calls the parent constructor having the same name of the parent class

# **References**

<https://www.php.net/manual/en/migration70.deprecated.php>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
