---
title: The code contains too many hard coded absolute file system paths in include directives
url: https://doc.casthighlight.com/code-contains-many-hard-coded-absolute-file-system-paths-include-directives/
slug: code-contains-many-hard-coded-absolute-file-system-paths-include-directives
content_type: rule
languages: [abap]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

In order to ease change and to hide platform specific information from any potential misuse, it is highly recommended to use SAP ABAP logical paths instead of hard-coded paths.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Use standard SAP ABAP logical paths instead of hard-coded paths and the standard ABAP function “FILE\_GET\_NAME” instead.

# **How we detect**

This Code Insight counts one occurrence each time a hard-coded path is detected.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
