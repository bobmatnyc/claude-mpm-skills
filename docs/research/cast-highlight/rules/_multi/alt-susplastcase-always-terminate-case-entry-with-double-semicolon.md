---
title: Double semicolon is required for a bash syntax to correctly parse the command
url: https://doc.casthighlight.com/alt_susplastcase-always-terminate-case-entry-with-double-semicolon/
slug: alt_susplastcase-always-terminate-case-entry-with-double-semicolon
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

A simple semicolon is used to end the items of structures, signatures and objects as these semicolons are considered mandatory. The double semicolon is also useful as it leaves no ambiguity in the code. It is required as it is used at the end of each clause as required by the bash syntax in order to parse the command correctly. It is only used in case constructs to indicate that the end of an alternative.

# **Business Impacts**

It is recommended to add a double semi-colon as it prevents the code from having risks and lets the code be more productive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://caml.inria.fr/pub/docs/tutorial-camlp4/tutorial005.html  
https://stackoverflow.com/questions/16905183/dash-double-semicolon-syntax  
http://www.linuxquestions.org/questions/linux-newbie-8/bash-scripting-options-double-semicolon-4175600617/

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that an inconsistency is found around esac keyword due to the absence of double semi-colon after the last case entry.  
 Explanation : the analyzer expect the esac instruction to be in the same level than its associated case. Each case entry introduces a new statement, while each double semicolon leave this “entry” statement. If the ;; is forgotten, the esac is not in the same imbrication level than the associated case, and that is the most ofen the cause of this alert…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
