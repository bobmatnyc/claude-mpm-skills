---
title: Conditional comments are designed exclusively for IE
url: https://doc.casthighlight.com/alt_ieconditionalcomments-avoid-ies-conditional/
slug: alt_ieconditionalcomments-avoid-ies-conditional
content_type: rule
languages: [java, javascript]
category: Changeability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Conditional Comments are designed exclusively for Internet Explorer (IE), and hence they operate greatly in that specific browser as these comments are suited to give special instructions that are only meant for IE. As a result, conditional comments are considered a hindrance when run in a browser, other than IE, and should not appear in the code.

# **Business Impacts**

Conditional Comments are not accessible as they exclusively work in Internet Explorer. This greatly reduces the code’s potential to be accessible and productive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://www.quirksmode.org/css/condcom.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight suggests to avoid:  
var f = function () {  
/\*@cc\_on if (@\_jscript) { return 2\* @\*/ 3; /\*@ } @\*/  
};  
Conditional Comments hinder automated tools as they can vary the JavaScript syntax tree at runtime.  
Conditional compilation is allowed outside comment, but should strongly avoided as it may cause an invalid syntax for other browser than IE.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
