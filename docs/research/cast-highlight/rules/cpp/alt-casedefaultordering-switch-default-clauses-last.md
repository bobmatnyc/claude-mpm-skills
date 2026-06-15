---
title: In switch ‘default’ clauses should be last
url: https://doc.casthighlight.com/alt_casedefaultordering-switch-default-clauses-last/
slug: alt_casedefaultordering-switch-default-clauses-last
content_type: rule
languages: [cpp]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Switch can contain a default clause for various reasons: to handle unexpected values, to show that all the cases were properly considered.

For code readability purpose, to help a developer to quickly find the default behavior of a switch statement, it is recommended to put the default clause at the end of the switch statement. This rule raises an issue if the default clause is not the last one of the switch’s cases.

# **How we detect**

CAST Highlight counts one occurrence each time the default clause of a switch in not in last position.

**Bad Code**

```
switch (param) {
default: // default clause should be the last one
error();
break;
case 0:
doSomething();
break;
case 1:
doSomethingElse();
break;
}
```

**Good Code**

```
switch (param) {
case 0:
doSomething();
break;
case 1:
doSomethingElse();
break;
default:
error();
break;
}
```

# **References**

MISRA C++:2008, 6-4-6 – The final clause of a switch statement shall be the default-clause  
MISRA C:2012, 16.5 – A default label shall appear as either the first or the last switch label of a switch statement

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
