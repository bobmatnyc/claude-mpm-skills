---
title: Avoid naming unused receivers
url: https://doc.casthighlight.com/alt_badreceiver-avoid-naming-unused-receivers/
slug: alt_badreceiver-avoid-naming-unused-receivers
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

If the receiver of a method is unused, do not give it a name. It’s more readable because it’s clear that the receiver is not used in method.

# **How we detect**

CAST Highlight counts one occurrence each time a receiver is named and is not used in the method.

```
// Don't do this:
func (f foo) method() {
...
}

// Do this : 
func (foo) method() {
...
}
```

# **References**

<https://dmitri.shuralyov.com/idiomatic-go#avoid-unused-method-receiver-names>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
