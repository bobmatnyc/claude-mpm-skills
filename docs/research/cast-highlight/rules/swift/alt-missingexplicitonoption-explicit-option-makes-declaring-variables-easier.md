---
title: Explicit Option makes declaring variables easier
url: https://doc.casthighlight.com/alt_missingexplicitonoption-explicit-option-makes-declaring-variables-easier/
slug: alt_missingexplicitonoption-explicit-option-makes-declaring-variables-easier
content_type: rule
languages: [swift]
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

VB has specific behavior that enable the developer to use variables even if these variables have not been previously declared and typed. However, it is possible to avoid this default behavior using the Option Explicit : in this case, all variables will require a declaration prior use.  
This provides 2 main benefits.  
The first benefit is a lower memory consumption improving other all application’s performance. This is due to the fact that undeclared variables are automatically created as Variant (large memory consumption).  
The second benefit is that this option helps the developer to detect typing errors when writing code.

# **Business Impacts**

Option Explicit is recommended because it greatly increases productivity and makes the code more efficient and less consuming.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Option Explicit is recommended for VB users as it allows for improving the business aspects of the application portfolios that are developed in the company.  As such, Option Explicit should be utilized in the company’s style guides that encourage developers to focus on lowering memory consumption and improving performance for their respective applications.

# **References**

<https://docs.microsoft.com/en-us/dotnet/visual-basic/language-reference/statements/option-explicit-statement>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight retrieves all VB Modules and Frames not using the Option explicit.

# **Impacts**

[Cloud](http://casthighlight.wpengine.com/category/product/indicators-methodology/Efficiency/)[Memory, Network, & Disk Space Management](http://casthighlight.wpengine.com/category/product/indicators-methodology/Efficiency/)

**Physical Environments referenced in Code:** Option Explicit ensures resources, and memory, are not being wasted when portfolios are being adopted for Cloud-Computing purposes.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
