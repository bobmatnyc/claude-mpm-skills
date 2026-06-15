---
title: Comparison operators compare values
url: https://doc.casthighlight.com/alt_missingidentical-avoiding-implied-typecasting/
slug: alt_missingidentical-avoiding-implied-typecasting
content_type: rule
languages: [java, javascript]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

This is important since Javascript has comparison operators such as “regular equality” (==) and “is not equal to” (!=) which compares two values (strings, numbers, boolean operands and so forth) for equality. With “regular equality”, two values are set to identical after being converted to a common type.  
“Is not equal to” is utilized to ensure that the values are not identical to each other. Without a comparison operator, values cannot be compared.

# **Business Impacts**

It is recommended to avoid implied typecasting as it causes confusion on the technical side. This results in allowing more risks in the code and leading to lack of productivity.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Comparison_Operators>

<https://www.w3schools.com/js/js_comparisons.asp>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight show that JavaScript implicitly typecasts variables when you compare them. That’s why comparisons such as false == 0 or “” == 0 return true.  
To avoid confusion caused by the implied typecasting, always use the === and !== operators that check both the values and the type of the expressions you compare, because the understanding of what is a falsy value may be confusing.  
The == and != operators do type coercion. In particular, do not use == to compare against false values.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
