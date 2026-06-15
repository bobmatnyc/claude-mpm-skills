---
title: Avoid having too many conditions using variables without operators
url: https://doc.casthighlight.com/alt_variabledefinitioncheck/
slug: alt_variabledefinitioncheck
content_type: rule
languages: [php]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

When a variable without any operators is found within a ‘IF’ condition, in most of cases, it means that the developer wanted to perform some controls on this variable. However, in order to avoid any unexpected behavior during the execution, and depending on the verification type the developer intends to perform (existing/set or empty or true/false or null variable?), it is recommended to use the appropriate method, so that the risk of misinterpretation of the verification is limited.

# **Business Impacts**

It is recommended to use an explicit method to verify conditions of your variables, in order to avoid misinterpretation and possible bugs.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends checking your variables with the appropriate method, depending on your specific case (e.g. isset() to check the variable exists, empty(), is\_null, etc.) in order to avoid any misinterpretation of the verification (boolean, empty, exist).

# **References**

<https://stackoverflow.com/questions/6693876/how-exactly-does-ifvariable-work>  
<https://stackoverflow.com/questions/30191521/php-check-if-variable-is-undefined>

# **How we detect**

This Code Insight counts one occurrence each time a variable is found in a codition, without any operator.

Example:

if($\_GET[‘myvariable’]) { … }  
if($foo) { … }

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
