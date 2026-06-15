---
title: "The code contains modifications of buildtins objects : Object, Array or Function"
url: https://doc.casthighlight.com/alt_behaviouralteration-the-code-contains-modifications-of-buildtins-objects-object-array-or-function/
slug: alt_behaviouralteration-the-code-contains-modifications-of-buildtins-objects-object-array-or-function
content_type: rule
languages: [java, javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Modifying builtins like Object.prototype and Array.prototype are strictly forbidden. Modifying other builtins like Function.prototype is less dangerous but still leads to hard to debug issues in production and should be avoided.

It is not seldom that you see people messing with Object.prototype.  
This is very bad because it breaks the object-as-hash-tables feature  
in javascript. Basically, the following is a very common scenario:

```
var obj = {a: "A", b: "B", c: "C", d: "D"};
for (var key in obj) {
doSomething(key, obj[key], obj);
}
if ("b" in obj) {
doSomethingElse();
}
```

If someone modified the Object.prototype the for in loop would include any fields you’ve added

# **How we detect**

CAST Highlight counts one occurrence each time one of the following patterns is found in the source code:

```
Object.prototype.<xxxx> = ....
Array.prototype.<xxxx> = ....
Function.prototype.<xxxx> = ....
```

# **References**

<https://flaviocopes.com/javascript-why-not-modify-object-prototype/>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
