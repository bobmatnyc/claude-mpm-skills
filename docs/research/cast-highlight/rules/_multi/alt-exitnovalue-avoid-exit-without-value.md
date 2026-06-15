---
title: EXIT without parameters cause issues in the script
url: https://doc.casthighlight.com/alt_exitnovalue-avoid-exit-without-value/
slug: alt_exitnovalue-avoid-exit-without-value
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The KSH script starts at the first and essentially ends when the code encounters an “exit” or the last line. When exiting a code without parameters, it causes the code to become unreliable and cause errors that tend to become unmanageable.

# **Business Impacts**

It is recommended to have parameters in the script because lack of parameters will cause reliability issues leading to an unproductive and unmanageable code.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://www.well.ox.ac.uk/~johnb/comp/unix/ksh.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows when using exit with no parameters the default behavior is to exit with the return code of the last command executed. If you want to manage errors in your script, you must control your own error code system and return a specified value.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
