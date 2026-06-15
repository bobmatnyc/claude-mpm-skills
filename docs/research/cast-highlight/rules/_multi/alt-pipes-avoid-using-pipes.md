---
title: Pipes are an inefficient way of dealing with commands
url: https://doc.casthighlight.com/alt_pipes-avoid-using-pipes/
slug: alt_pipes-avoid-using-pipes
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

Pipes take the output of one command and put it on the input of another command. They can also be strung together. This way, one can find matches in a particular pattern in their name AND have a particular IP address range.  
However the disadvantage is that it can be wasteful in nature and the code tends to be more efficient with a single awk command.

# **Business Impacts**

Using pipes in a program can be a risky decision as it tends to be wasteful in both time and productivity.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<http://www.bolthole.com/solaris/ksh-redirection.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts one violation each time a command is piped into another.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
