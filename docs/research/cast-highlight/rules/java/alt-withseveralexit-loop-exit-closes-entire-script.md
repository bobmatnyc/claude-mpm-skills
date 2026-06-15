---
title: EXIT closes the entire script
url: https://doc.casthighlight.com/alt_withseveralexit_loop_exit-closes-entire-script/
slug: alt_withseveralexit_loop_exit-closes-entire-script
content_type: rule
languages: [java]
category: Transferability
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

EXIT instruction is designed to exit the entire script hence the purpose of having only one instruction at a time. EXIT instruction has the capability of causing some of the script to be unread if placed incorrectly. As a result, the script will have compilation errors.

# **Business Impacts**

EXIT is an instruction that can add complexity if not used properly which results in a loss of time that could be used towards innovating the script instead.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://www.geeksforgeeks.org/system-exit-in-java/

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This Code insight suggests that only one EXIT instruction should be present, and if possible, it should be the last instruction of the script.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
