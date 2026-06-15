---
title: Object Qualification improves readability
url: https://doc.casthighlight.com/alt_dbobjectqualification-avoid-missing-object-qualification/
slug: alt_dbobjectqualification-avoid-missing-object-qualification
content_type: rule
languages: [java]
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/Code-Readability/)

# **Why you should care**

Object Qualification is the process of determining whether a persistent object satisfies a set of specified conditions. It is typically performed as part of a search operation that finds a group of persistent objects based on the values of one or more of their attributes. It is tested against a candidate object and its attribute values and thus the predicate string evaluates to true or false. Without Object Qualification, the code can be unreadable causing confusion and possible bugs.

# **Business Impacts**

It is recommended to implement object qualification as it allows the program to be read and understood easier which prevents confusion resulting in cost-reduction.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://support.objectivity.com/sites/default/files/docs/objy/R11_0_0/html/java/guide/jgdObjectQualification.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight highlights that database objects should be fully qualified : prefix the object names with the owner’s name, as this improves readability and avoids any unnecessary confusion

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
