---
title: The code contains too many dangerous usage patterns in file management
url: https://doc.casthighlight.com/alt_seriousfilepb-code-contains-many-dangerous-usage-patterns-file-management/
slug: alt_seriousfilepb-code-contains-many-dangerous-usage-patterns-file-management
content_type: rule
languages: [cobol]
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Avoid dangerous file usage patterns. File management contains dangerous usage patterns.

# **How we detect**

CAST Highlight counts one occurrence each time one of these patterns are detected in source code:

- a file (only FD) declared in data division is open and not closed, or is closed without having been openned
- a COBOL source file has no **INPUT-OUTPUT SECTION**
- a COBOL source file has no **FILE SECTION**
- a **FD *<file>*** or **SD *<file>*** in file section is not declared with a **SELECT *<file>*** instruction in input-output section

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
