---
title: Specify precision otherwise error occurs
url: https://doc.casthighlight.com/alt_missingprecision-avoid-missing-precision-when-declaring-data/
slug: alt_missingprecision-avoid-missing-precision-when-declaring-data
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Specify precision which is the total number of digits, and scale, which is the number of digits to the right of the decimal point. The range of a Char variable is from 1 to 32767 bytes. When the expression falls outside this range, it is no longer precise and a numeric overflow or undeflow error occurs.

# **Business Impacts**

It is recommended to specify precision as it helps alleviate potential risks in the code and ensure that the code is reliable and accessible

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://docs.oracle.com/cd/B19306_01/appdev.102/b14261/datatypes.htm>  
<https://docs.oracle.com/cd/A97630_01/appdev.920/a96624/03_types.htm>  
<https://docs.oracle.com/cd/B28359_01/appdev.111/b28370/datatypes.htm#i43252>  
<https://stackoverflow.com/questions/1171196/what-is-the-difference-between-varchar-and-varchar2>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that char-based variable must always be declared.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
