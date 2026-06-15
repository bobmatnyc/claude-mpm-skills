---
title: Avoid variable assignments in conditional expressions
url: https://doc.casthighlight.com/alt_assignmentsinconditionalexpr-avoid-many-variable-assignments-conditional-expressions/
slug: alt_assignmentsinconditionalexpr-avoid-many-variable-assignments-conditional-expressions
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-resiliency/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

This pattern verifies the presence of variable assignments in conditional (IF) expressions. It is generally not recommended to use the assignment operator in this case as it is close to the comparison operator (==) and could lead to misreading the code logic.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Assign variables outside conditional expressions.

# **References**

<https://stackoverflow.com/questions/16148580/assign-variable-value-inside-if-statement>  
<https://stackoverflow.com/questions/17681535/variable-assignment-in-if-condition>

# **How we detect**

CAST Highlight counts one occurrence each time the assignment operator (=) is detected within a conditional expression, whether it is IF, EACH or WHILE.

```
if(foo = "1234") { ... // +1
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://doc.casthighlight.com/outputs-analytics/)

[HOW IT WORKS](http://casthighlight.wpengine.com/how-it-works/)
