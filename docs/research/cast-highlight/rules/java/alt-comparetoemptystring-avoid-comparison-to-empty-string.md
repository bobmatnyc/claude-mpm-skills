---
title: "CompareTo Empty is unreliable as it tests reference equality, not object equality"
url: https://doc.casthighlight.com/alt_comparetoemptystring-avoid-comparison-to-empty-string/
slug: alt_comparetoemptystring-avoid-comparison-to-empty-string
content_type: rule
languages: [java]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Using a CompareTo Empty string is considered unreliable as it tests reference equality and not object equality. Generally when programming, one cannot entirely rely on reference equality as it tends to be inaccurate and unreliable which is not ideal for the code.

# **Business Impacts**

It is recommended to avoid CompareTo as it provides inaccurate results which is risky for the code.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://stackoverflow.com/questions/531779/comparing-a-string-with-the-empty-string-java

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that, in Oracle, an empty string is equivalent to NULL which may not work, as expected, in an equality comparison statement. It is recommended to utilize IS NULL instead.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
