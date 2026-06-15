---
title: ‘switch’ statements should not be nested
url: https://doc.casthighlight.com/alt_nestedswitches-switch-statements-should-not-be-nested/
slug: alt_nestedswitches-switch-statements-should-not-be-nested
content_type: rule
languages: [java, cpp]
category: Transferability
has_code_examples: true
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/software-elegance/)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

Nested *switch* structures are difficult to understand because you can easily confuse the cases of an inner switch as belonging to an outer statement. Therefore nested *switch* statements should be avoided.

Specifically, you should structure your code to avoid the need for nested *switch* statements, but if you cannot, then consider moving the inner *switch* to another function.

# **How we detect**

CAST Highlight counts one occurrence each time a nested switch is encountered.

**Bad Code**

```
switch (n) {
case 0:
switch (m) { // Noncompliant; nested switch
case 0:
// ...
case 1:
switch (o) { // Noncompliant; nested switch

case 0:
switch (p) { // Noncompliant; nested switch
//...
}

default:
// ...
}
}
case 1:
switch (o) { // Noncompliant; nested switch
default:
// ...
}
default:
// ...
}
```

Good Code

```
function foo(n: number, m: number) {
  switch (n) {
    case 0:
      bar(m);
    case 1:
      // ...
    default:
      // ...
  }
}
 
function bar(m: number) {
  switch(m) {
    // ...
  }
}
```

# **References**

<https://stackoverflow.com/questions/15931089/alternative-to-nested-switch-statements-in-java>  
<https://www.fluentcpp.com/2017/06/27/how-to-collapse-nested-switch-statements/>  
<https://stackoverflow.com/questions/14827914/is-there-any-design-pattern-to-avoid-a-nested-switch-case>  
<https://rules.sonarsource.com/java/RSPEC-1821>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
