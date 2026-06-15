---
title: The Web Dynpro code contains too many direct calls to routines using “me–>”
url: https://doc.casthighlight.com/alt_reftome-web-dynpro-code-contains-many-direct-calls-routines-using/
slug: alt_reftome-web-dynpro-code-contains-many-direct-calls-routines-using
content_type: rule
languages: [abap]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Special rules apply for the implementation of Web Dynpro routines, such as “wd\_Do\_Init” methods. Some ABAP language statements cannot be used. Other routines cannot be called directly – instead they must be called with the “wd\_This” instance. The reason for this is that a direct call makes any extensions made from restructured layers impossible.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Replace the “me->” calls with a delegation using “wd\_This->”.

# **How we detect**

This Code Insight counts one occurrence each time a direct call to routine using the “me–>” instance is found in Web Dynpro source code.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
