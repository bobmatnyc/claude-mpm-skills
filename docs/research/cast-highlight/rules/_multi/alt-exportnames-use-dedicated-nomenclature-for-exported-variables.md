---
title: Exported Variables are global in scope and store values
url: https://doc.casthighlight.com/alt_exportnames-use-dedicated-nomenclature-for-exported-variables/
slug: alt_exportnames-use-dedicated-nomenclature-for-exported-variables
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/Code-Readability/)

# **Why you should care**

Variables and parameters are used by the Korn shell to store values. The Korn shell supports data types and arrays. The Variables are global in scope and begin with an alphabetic or underscore character followed by one or more alphanumeric or underscore characters. Other variables include digits (0 – 9) or special characters. An attribute reserved for Exported Variables is that each variable should be uppercase and be of length that is 16 characters or less.

# **Business Impacts**

It is recommended to use dedicated nomenclature for exported variables In order to reduce costs and improve code readability.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://www.informit.com/articles/article.aspx?p=99035>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that exported variables should be uppercase and have a limited length.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
