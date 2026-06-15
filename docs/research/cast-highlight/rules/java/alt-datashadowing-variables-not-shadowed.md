---
title: Variables should not be shadowed
url: https://doc.casthighlight.com/alt_datashadowing-variables-not-shadowed/
slug: alt_datashadowing-variables-not-shadowed
content_type: rule
languages: [java, javascript]
category: Security
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Overriding a variable declared in an outer scope can strongly impact the readability, and therefore the maintainability, of a piece of code. Further, it could lead maintainers to introduce bugs because they think they’re using one variable but are really using another.

# **How we detect**

CAST Highlight counts one occurrence each time a variable declaration (with var, let or const) is hidding another upper level declaration (variable or parameter).

```
function foo() {
if (x > 0) {
let y = bar(2); // no shadowing
} else {
let y = bar(3); // no shadowing
}
}
function foo() {
if (x > 0) {
let y = bar(2); // the let declaration is shadowing the var declaration.
} else {
var y = bar(3);
}
}
function foo() {
let y = bar(2); // do not compile because "let y" and "var y" are both in the full function scope.
if (x > 0) {
var y = bar(3);
}
}
function foo() {
if (x > 0) {
let y = 0; // y is not conflicting with "var y" because "var y" is in the full scope of the function, while "let y" is in the scope of the "if" statement". So "let y" is shadowing "var y".
while (more) {
var y = bar(3);
}
}
}
```

# **References**

<https://www.appmarq.com/public/security,1021072,Avoid-shadowing-class-variables>  
<https://javascript.plainenglish.io/javascript-best-practices-shadowing-variables-and-spacing-950c0ee2259f>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
