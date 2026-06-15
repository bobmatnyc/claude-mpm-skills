---
title: Less efficient datatypes cause interchangeability issues
url: https://doc.casthighlight.com/alt_notefficiencytype-avoid-using-less-efficient-types/
slug: alt_notefficiencytype-avoid-using-less-efficient-types
content_type: rule
languages: [sql]
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Every constant, variable, and parameter has a datatype (or type) which specifies a storage format, constraints, and valid range of values. PL/SQL provides a variety of predefined datatypes which tend to be inefficient in nature.

It’s recommended to use efficient practices over inefficient types to ensure the code runs efficiently and interchangably across platforms. It also ensures that the code is not complex in the process

# **Business Impacts**

Using less efficient types is absolutely risky for the code because it’s name is certainly a giveaway. It is best practice to avoid less efficient types so that the code can be more productive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://docs.oracle.com/cd/A97630_01/appdev.920/a96624/03_types.htm>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that PLS\_INTEGER should be used for its efficiency, avoid type conversion, and constrained types when its possible.  
PLS\_INTEGER is defined in the STANDARD package as a subtype of BINARY\_INTEGER. PLS\_INTEGER operations use machine arithmetic, so they are generally faster than NUMBER and INTEGER operations. Also, prior to Oracle Database 10g, they are faster than BINARY\_INTEGER. In Oracle Database 10g, however, BINARY\_INTEGER and PLS\_INTEGER are now identical and can be used interchangeably.  
The types NATURALN and POSITIVEN are defined to be NOT NULL subtypes of NATURAL and POSITIVE, respectively; thus, you will incur the performance penalty described in the NotNullVariables alert description when you use them.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
