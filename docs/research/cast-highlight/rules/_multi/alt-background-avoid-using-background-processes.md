---
title: Background processes are created by KSH
url: https://doc.casthighlight.com/alt_background-avoid-using-background-processes/
slug: alt_background-avoid-using-background-processes
content_type: rule
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Background processes occur behind the scenes without user intervention. They can be considered unwanted and slow down the software that is running and is of main priority to the user.  
Background processes occur as KSH is capable of providing a facility to control and run job in the background.

# **Business Impacts**

Background processes are risky because it has a tendency of greatly slowing down the code; rendering it unproductive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://www.cyberciti.biz/howto/unix-linux-job-control-command-examples-for-bash-ksh-shell/>  
<https://en.wikipedia.org/wiki/Background_process>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that background processes introduces asynchronous processes execution. They can potentially create resource conflicts. Execution in background is useful for command line but should be avoided in scripts.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
