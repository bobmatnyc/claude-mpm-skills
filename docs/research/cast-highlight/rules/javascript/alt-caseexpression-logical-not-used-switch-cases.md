---
title: Logical OR should not be used in switch cases
url: https://doc.casthighlight.com/alt_caseexpression-logical-not-used-switch-cases/
slug: alt_caseexpression-logical-not-used-switch-cases
content_type: rule
languages: [javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The logical OR operator (||) will not work in a switch case as one might think, only the first argument will be considered at execution time.

# **How we detect**

CAST Highlight counts one occurrence each time a case argument is implementing unexpected logical ||.

**Bad Code**

```
switch (x) {
case 1 || 2: // Noncompliant; only '1' is handled
doSomething(x);
break;
case 3:
doAnotherThing(x);
break;
default:
console.log("Boom!"); // this happens when x is 2
}
```

**Good Code**

```
switch (x) {
case 1:
case 2:
doSomething(x);
break;
case 3:
doAnotherThing(x);
break;
default:
console.log("Boom!");
}
```

# **References**

<https://rules.sonarsource.com/typescript/RSPEC-3616>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
