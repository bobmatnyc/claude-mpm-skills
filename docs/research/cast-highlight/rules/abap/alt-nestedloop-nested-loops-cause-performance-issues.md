---
title: Nested Loops cause performance issues
url: https://doc.casthighlight.com/alt_nestedloop-nested-loops-cause-performance-issues/
slug: alt_nestedloop-nested-loops-cause-performance-issues
content_type: rule
languages: [abap]
category: Efficiency
has_code_examples: false
---

[Software Elegance](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance)[Code Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-elegance/code-complexity/)

# **Why you should care**

If the amount of data is large, nested loops are fully avoided due to performance issues. If the program is extracting small amount of data, then focus on SELECT statements than nested loops.  
The indexed loop and READ statement using binary search are the best methods to avoid performance issues.

# **Business Impacts**

Nested Loops can greatly reduce the innovative potential of the code because it negatively impacts performance.

[Acceleration](http://casthighlight.wpengine.com/category/product/indicators-methodology/acceleration/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Reduce the total number of parameters by subdividing your functions into more specialized and granular artifacts.

# **References**

<http://www.sommarskog.se/share_data.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight checks all Abap artifacts containing nested loops. These are:  
– LOOP … ENDLOOP  
– DO … ENDDO  
– WHILE … ENDWHILE  
– PROVIDE … ENDPROVIDE

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
