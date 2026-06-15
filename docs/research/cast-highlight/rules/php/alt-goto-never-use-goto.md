---
title: GoTo is primitive & outside one’s control
url: https://doc.casthighlight.com/alt_goto-never-use-goto/
slug: alt_goto-never-use-goto
content_type: rule
languages: [php]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

The GOTO statement branches unconditionally to a statement label or block label. The label must be uniqe within its scope and precede an executable statement. The issues with GoTo however is its repetitive and superflous nature. It also enlongates the conceptual phase between the static prgram and the dynamic process which is not ideal for a programmer. The GoTo statement results in clauses that can create values outside of the programmer’s control which makes it hard to find a meaningful set of coordinates rendering it primitive in nature.

# **Business Impacts**

GoTo is primitive making it risky to incorporate in current programs. It deliberately wastes time and creates uncontrollable variables on the technical side making it unproductive.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://www.techonthenet.com/oracle/loops/goto.php>  
<http://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight suggests to never use GoTo.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
