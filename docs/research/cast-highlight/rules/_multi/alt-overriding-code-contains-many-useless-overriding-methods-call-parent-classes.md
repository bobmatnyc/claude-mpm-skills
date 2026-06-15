---
title: Avoid useless overriding method
url: https://doc.casthighlight.com/alt_overriding-code-contains-many-useless-overriding-methods-call-parent-classess-method-name-arguments/
slug: alt_overriding-code-contains-many-useless-overriding-methods-call-parent-classess-method-name-arguments
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Overring methods is a very powerfull way of factoring the code and produce complete fonctionnalities. However useless overriding methods can be a problem for the simplicity of the source code.

# **How we detect**

CAST Highlight counts one occurrence each time a method only call its parent classes’s method with the same name and arguments.

```
class FooBar {
    public function __construct($a, $b) {
        parent::__construct($a, $b);
    }
}
```

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
