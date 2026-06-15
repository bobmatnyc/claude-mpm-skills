---
title: Variables should be declared with ‘let’ or ‘const’
url: https://doc.casthighlight.com/alt_variabledeclaration-variables-declared-let-const/
slug: alt_variabledeclaration-variables-declared-let-const
content_type: rule
languages: [java, javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

The distinction between the variable types created by *var* and by *let* is significant, and a *switch* to let will help alleviate many of the variable scope issues which have caused confusion in the past.

This code insight will trigger when *var* is used instead of *const* or *let*.

# **How we detect**

CAST Highlight counts one occurrence each time a variable is declared using the *var* statement.

**Bad Code**

```
var color = "blue";
var size = 4;
```

**Good Code**

```
const color = "blue";
let size = 4;
```

# **References**

<https://evertpot.com/javascript-let-const/>  
<https://pandeysoni.medium.com/when-should-use-const-and-let-instead-of-var-in-javascript-ec2c3d7e5ca6>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
