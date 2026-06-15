---
title: CASE is better to understand than DECODE
url: https://doc.casthighlight.com/alt_decode-avoid-using-decode/
slug: alt_decode-avoid-using-decode
content_type: rule
languages: [sql]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

The DECODE function belongs to PLSQL and has the functionality of an IF-THEN statement. It’s syntax is as follows DECODE( expression , search , result [, search , result]…[, default] )  
expression – The value to compare  
search – The value is compared against expression  
result – The value returned, if expression is equal to search  
default – Optional. If not matches are found, the DECODE function will return default. If default is omitted, then the DECODE function will return null (if no matches are found).  
With that being said, CASE is a better function as it is simpler to write and can be used in PL/SQL. CASE is easier to read, understand and maintain the code.

# **Business Impacts**

DECODE function is an old function replaced by CASE because the latter is less risky to use and more productive. This is because CASE is easier to read, understand and maintain.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://stackoverflow.com/questions/3193692/case-vs-decode>

<https://www.oratable.com/decode-case-differences/>

<https://www.dba-oracle.com/t_difference_decode_case.htm>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that DECODE is an old function that has been replaced by the easier-to-understand and more common CASE function. Contrary to the DECODE statement CASE may also be used directly within PL/SQL

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
