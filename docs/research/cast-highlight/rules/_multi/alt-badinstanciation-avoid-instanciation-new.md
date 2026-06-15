---
title: Avoid instantiation with new
url: https://doc.casthighlight.com/alt_badinstanciation-avoid-instanciation-new/
slug: alt_badinstanciation-avoid-instanciation-new
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Use *&T{}* instead of *new(T)* when initializing struct references so that it is consistent with the struct initialization.

# **How we detect**

CAST Highlight counts one occurrence each time the keyword “*new*” is used.

```
// Bad
sptr := new(T)
sptr.Name = "bar"

// Good
sptr := &T{Name: "bar"}
```

# **References**

<https://github.com/bahlo/go-styleguide#avoid-new-keyword>  
<https://github.com/uber-go/guide/blob/master/style.md#initializing-struct-references>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
