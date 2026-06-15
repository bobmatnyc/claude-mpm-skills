---
title: The code contains too many var statements declaring several variables in it
url: https://doc.casthighlight.com/alt_multdecl-code-contains-many-var-statements-declaring-several-variables/
slug: alt_multdecl-code-contains-many-var-statements-declaring-several-variables
content_type: rule
languages: [java, javascript]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Although JavaScript allows to declare multiple variables in a single chain, it is recommended to declare each variable separately as it is easier to read and reduce the risk of unexpected behaviors in some cases.

# **How we detect**

CAST Highlight counts one occurrence when multiple variable declarations are detected.

Bad Code

```
var header,
topnav,
content;
```

Good Code

```
var firstVar;
var secondVar;
var thirdVar;
```

# **References**

<https://eslint.org/docs/rules/one-var>  
<https://bluepnume.medium.com/theres-no-need-to-define-all-javascript-vars-once-at-the-top-of-a-function-and-there-hasn-t-been-a66b31f21822>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
