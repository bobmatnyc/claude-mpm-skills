---
title: The code contains one or more “with” instructions
url: https://doc.casthighlight.com/alt_scope-code-contains-one-instructions/
slug: alt_scope-code-contains-one-instructions
content_type: rule
languages: [java, javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The with statement in javascript inserts an object at the front scope chain, so any property/variable references will first try to be resolved against the object. This is often used as a shortcut to avoid multiple long references.

```
with (document.forms["mainForm"].elements) {
   input1.value = "junk";
   input2.value = "junk";
}
```

The problem is that the programmer has no way to verify that input1 or input2 are actually being resolved as properties of the form elements array. It is checked first for properties with these names, but if they aren’t found then it continues to search up the scope chain. Eventually, it reaches the global object where it tries to treat “input1” and “input2” as global variables and tries to set their “value” properties, which result in an error.

Instead, create a reference to the reused object and use it to resolve references.

# **How we detect**

CAST Highlight counts one occurrence each time a *with* keyword is found.

**Bad Code**

```
with (document.forms["mainForm"].elements) {
   input1.value = "junk";
   input2.value = "junk";
}
```

Good Code

```
var elements = document.forms["mainForm"].elements;
elements.input1.value = "junk";
elements.input2.value = "junk";
```

# **References**

https://www.barryvan.com.au/2009/05/avoid-javascripts-with-keyword/

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
