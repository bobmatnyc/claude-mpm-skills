---
title: Optional property declarations should use ‘?’ syntax
url: https://doc.casthighlight.com/alt_optionalproperties-optional-property-declarations-use-syntax/
slug: alt_optionalproperties-optional-property-declarations-use-syntax
content_type: rule
languages: [kotlin, javascript]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

In TypeScript there are several ways to declare an optional property, i.e. a property which might be missing from an object: adding “| undefined” in the property type or adding “?” after its name. The latter is preferred as it brings more clarity and readability to a code.

# **How we detect**

CAST Highlight counts one occurrence each time a property is declared optional with ‘| undefined’. This code insight is only for interfaces, because optional property is not allowed for classes.

**Bad Code**

```
interface Person {
  name: string;
  nickname: string | undefined; // Noncompliant
  pet?: Animal | undefined; // Noncompliant, "undefined" is redundant
  age: number;
}
```

**Good Code**

```
interface Person {
  name: string;
  nickname?: string;
  pet?: Animal;
  age: number;
}
```

# **References**

<https://developer.android.com/kotlin/style-guide>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
