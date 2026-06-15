---
title: Avoid collapsible nested ‘if’
url: https://doc.casthighlight.com/alt_collapsibleif-avoid-collapsible-nested/
slug: alt_collapsibleif-avoid-collapsible-nested
content_type: rule
languages: [java]
category: Changeability
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Merging collapsible *if* statements increases the code’s readability.

# **How we detect**

CAST Highlight counts one occurrence each time several nested ‘if’, having each one no ‘else’ and each nested one beeing the only instruction of the encompassing.

**Bad Code**

```
def dummy() {
if (file != null) { // +1 VIOLATION
if (file.isFile() || file.isDirectory()) {
/* ... */
}
}
//Compliant Solution
if (file != null && isFileOrDirectory(file)) {
/* ... */
}

if (toto) { // +0 because encompassing 'if' has a 'else'
if (tata) {
b=a
}
}
else {
a=b
}

if (toto) { // +0 because nested 'if' has a else
if (tata) {
b=a
}
else {
a=b
}
}

if (toto) { // +0 because nested 'if' is not the only instruction of the encompassing.
if (tata) {
b=a
}
print (b)
}
}
```

# **References**

<https://rules.sonarsource.com/java/RSPEC-1066>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
