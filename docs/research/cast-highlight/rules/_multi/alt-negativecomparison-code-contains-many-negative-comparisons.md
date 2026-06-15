---
title: The code contains too many negative comparisons
url: https://doc.casthighlight.com/alt_negativecomparison-code-contains-many-negative-comparisons/
slug: alt_negativecomparison-code-contains-many-negative-comparisons
content_type: rule
category: Robustness
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-resiliency/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

This pattern verifies the presence in source code of negative comparisons. Depending on the frequency, CAST Highlight will trigger this code insight.

It’s much easier to think in a positive way about a situation than to be presented with the negative alternative and having to transform it in your mind by yourself to positive. People tend to have a ‘logical’ or ‘the default behaviour’ feeling about true, which makes it easy to think about. On the contrary, false is mostly regarded is the ‘exception’, ‘the error situation’ or the ‘alternative way out’.

Expressing the logic in a positive way helps developers better and quicker understand the code and is less error-prone.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Turn the negative comparison into a positive comparison whenever possible in the source code.

# **References**

<https://medium.com/@Cuadraman/why-to-stop-writting-negavite-code-af5ffb17195>

# **How we detect**

CAST Highlight counts one occurrence each time a condition contains “false” keyword or “!” character.

Example:

```
if ( ! (foo == value) { // +1
   var = FALSE;
}
else if(foo == FALSE) { +2
   var = TRUE;
}
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://doc.casthighlight.com/outputs-analytics/)

[HOW IT WORKS](http://casthighlight.wpengine.com/how-it-works/)
