---
title: The code contains too many unchecked returns of functions calls
url: https://doc.casthighlight.com/alt_uncheckedreturn-code-contains-many-unchecked-returns-functions-calls/
slug: alt_uncheckedreturn-code-contains-many-unchecked-returns-functions-calls
content_type: rule
languages: [abap, sql]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Missing return code checks after an Open SQL statement can result in unpredictable behavior and untraceable execution errors. This is why it is extremely important to report and handle errors as soon as they occur.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Check the system field SY-SUBRC after SQL commands, internal table commands and file-handling commands.

# **References**

Enhancing the Quality of ABAP Development, Meijs-Krouwels-Heulmans-Sommen, SAP Press ISBN 1-59229-030-2

# **How we detect**

This Code Insight counts one occurrence each time an SQL statement is found without return code checks.

Example:

select date\_e into zdate\_e   
from zkopcor  
where date\_e lt p\_run  
and p\_doc eq ‘TT’.

<statements>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
