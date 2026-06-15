---
title: $$ creates unique temporary filenames
url: https://doc.casthighlight.com/alt_tmpfilename-always-use-in-tempo-filename/
slug: alt_tmpfilename-always-use-in-tempo-filename
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

$$ is used to making temporary names with the process ID in KSH. It allows for the name to be unique to the process.

# **Business Impacts**

$$ prevents risks and is helpful in making KSH code more productive by giving it more uniqueness.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://stackoverflow.com/questions/1846802/in-kornshell

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that $$ gives the process number of the script being executing. It is also important to always tag tmp file name with this number.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
