---
title: Avoid small switch/Case
url: https://doc.casthighlight.com/alt_smallswitchcase/
slug: alt_smallswitchcase
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

SWITCH statements are useful when there are many different cases depending on the value of the same expression. However, code will me more readable with IF statements for one or two cases.

# **How we detect**

CAST Highlight counts one occurrence each time a SWITCH structure has less than 3 cases statements.

**Bad Code**

```
switch (variable) {
case 0:
doSomething();
break;
default:
doSomethingElse();
break;
}
```

**Good Code**

```
switch (variable) {
case 0:
doSomething();
break;
case 1 : 
doSomething();
break;
default:
doSomethingElse();
break;
}
```

# **References**

MISRA C:2012, 16.6  
<https://rules.sonarsource.com/c/RSPEC-1301>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
