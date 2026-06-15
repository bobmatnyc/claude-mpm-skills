---
title: Crossing the Parameter limit can cause bugs
url: https://doc.casthighlight.com/alt_numberofparameters-crossing-parameter-limit-can-cause-bugs/
slug: alt_numberofparameters-crossing-parameter-limit-can-cause-bugs
content_type: rule
languages: [sql]
category: Transferability
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

Parameters are used to pass data between a stored procedure and the batch or script. It results in executing the stored procedure. Each Parameter has a limit, known as a Parameter limit, which is hard-coded per stored procedure. The Parameter limit, in an SQL server, is 2,100. This limit ensures avoiding bugs or improper use of procedures in the code.

# **Business Impacts**

It is advised that Parameters should be approached carefully as misuse can cause bugs which can slow the innovative potential of the code. These factors can make the code unsuitable for clients.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Reduce the total number of parameters by subdividing your functions into more specialized and granular artifacts.

# **References**

<http://www.sommarskog.se/share_data.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight establishes that functions, procedures and triggers should not have too many parameters. Depending on thresholds observed in the benchmark of thousands of applications and billions lines of code, Highlight accounts penalty points to the given scanned files.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
