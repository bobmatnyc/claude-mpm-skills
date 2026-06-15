---
title: Avoid having too many unused variables
url: https://doc.casthighlight.com/alt_varnotused-avoid-many-unused-variables/
slug: alt_varnotused-avoid-many-unused-variables
content_type: rule
languages: [cobol]
category: Efficiency
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Having too many variables that are unused somewhere in your software can make the software consume more memory than it should as the resource is allocated for each declared variable, whether it is use or not during the execution. It also doesn’t help developers get clear view on effectively used variables in a program.

# **Business Impacts**

It is recommended to declare only variables that will be used. At large scale, having a lot of these pattern occurrences could prevent the code from being efficient and cost-effective.

[COST](https://doc.casthighlight.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends declaring only variables that are effectively used in a program.

# **References**

<https://www.ibm.com/support/knowledgecenter/en/SSQ2R2_14.1.0/com.ibm.etools.rdz.language.editors.doc/topics/r_identify_unused.html>

# **How we detect**

This Code Insight counts one violation each time a variable 66, 77 or 88 declared in Working Storage section is never used in Procedure Division.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
