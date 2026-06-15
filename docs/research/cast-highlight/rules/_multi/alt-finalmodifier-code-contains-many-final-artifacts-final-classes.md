---
title: The code contains too many final artifacts in final classes
url: https://doc.casthighlight.com/alt_finalmodifier-code-contains-many-final-artifacts-final-classes/
slug: alt_finalmodifier-code-contains-many-final-artifacts-final-classes
content_type: rule
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Unnecessary final modifiers inside final classes should be avoided. Final modifier prevents child classes from overriding a method by prefixing the definition with final. If the class itself is being defined final then it cannot be extended and the modifier is useless.

# **How we detect**

CAST Highlight counts one occurrence each time a “*final*” artifact is detected within a final class.

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
