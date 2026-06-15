---
title: The first line activates the KSH interpreter
url: https://doc.casthighlight.com/alt_kshfirstline-avoid-missing-interpreter-invocation/
slug: alt_kshfirstline-avoid-missing-interpreter-invocation
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

The first line is useful as it tells the OS what interpreter to invoke in order to run the script. In this case, the interpreter is the KSH interpreter. Without this line, the KSH interpreter cannot used to run this script.

# **Business Impacts**

The first line in KSH is useful to consider as it allows the KSH code to be more resillient and run efficiently without the potential of having bugs and thus, leading to greater productivity.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://stackoverflow.com/questions/2673771/why-is-the-line-bin-ksh-is-the-first-line-in-a-shell-script>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that if the first line begins with #!, then the shell interpreter is specified by which the script is to be executed. If this indication is missing, the default interpreter is invoked. If the script is not compliant with the default interpreter, an error will occur.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
