---
title: "Use short variable declarations (:=) for variables with default values"
url: https://doc.casthighlight.com/alt_variabledeclaration-use-short-variable-declarations-variables-default-values/
slug: alt_variabledeclaration-use-short-variable-declarations-variables-default-values
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Short variable declarations (*:=*) should be used if a variable is being set to some value explicitly.

# **How we detect**

CAST Highlight counts one occurrence each time a local variable (*:=* operator is not allowed for global variables) is declared with var statement and is initialized with a default value.

**Note** : do not consider variables declared with *const*.

```
// bad
var s = "foo"
 
// good
s := "foo"
const (
	idIP0   = 4 // ip address start index
	idDmLen = 4 // domain address length index
)
 
const toto := 3
```

# **References**

<https://github.com/uber-go/guide/blob/master/style.md#local-variable-declarations>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
