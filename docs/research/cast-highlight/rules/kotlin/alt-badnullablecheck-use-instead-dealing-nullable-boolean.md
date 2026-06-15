---
title: "Use == instead of ?: when dealing with nullable boolean"
url: https://doc.casthighlight.com/alt_badnullablecheck-use-instead-dealing-nullable-boolean/
slug: alt_badnullablecheck-use-instead-dealing-nullable-boolean
content_type: rule
languages: [kotlin]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Nullable boolean can be null, or having a value “true” or “false”.

```
var a: Boolean?  // a is a nullable boolean
```

Before accessing the value, we should verify if the variable is null or not. This can be done with the classical check : if … else … For exemple, to check against true:

```
if ((a != null) && (a == true)) { ... } else { ... }
```

In Kotlin it is possible to use a compact syntax using the elvis operator. *(a ?: b)* is equivalent to *(if (a !=null) a else b)*. So checking a nullable Boolean to true can be shortly done with the elvis operator like that:

```
if ( a ?: false ) { ... } else { .... }
```

Unfortunately, even this is shortest it is nevertheless worse and indigest for many persons because of the boolean inversion. So, prefer using the direct check to the value, without checking the nullity:

```
if ( a == true ) { ... } else { .... }
```

# **How we detect**

CAST Highlight counts one occurrence each time the pattern ?:true or ?:false is encountered.

# **References**

<https://kotlinlang.org/docs/coding-conventions.html>  
[https://riptutorial.com/kotlin/example/30735/elvis-operator—–](https://riptutorial.com/kotlin/example/30735/elvis-operator-----)  
<https://github.com/Kotlin/kotlin-style-guide/issues/18>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
