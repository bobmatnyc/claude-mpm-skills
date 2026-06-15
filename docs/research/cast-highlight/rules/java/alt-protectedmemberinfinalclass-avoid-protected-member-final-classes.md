---
title: Avoid protected member in final classes
url: https://doc.casthighlight.com/alt_protectedmemberinfinalclass-avoid-protected-member-final-classes/
slug: alt_protectedmemberinfinalclass-avoid-protected-member-final-classes
content_type: rule
languages: [java]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The difference between private and protected visibility is that child classes can see and use protected members, but they cannot see private ones. Since a final class will have no children, marking the members of a final class protected is confusingly pointless.

Note that the protected members of a class can also be seen and used by other classes that are placed within the same package, this could lead to accidental, unintended access to otherwise private members.

# **How we detect**

CAST Highlight counts one occurrence each time a final class has a protected member.

**Bad Code**

```
public final class MyFinalClass {
protected String name = "Fred";
protected void setName(String name) {
// ...
}
```

# **References**

<https://rules.sonarsource.com/java/tag/confusing/RSPEC-2156>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
