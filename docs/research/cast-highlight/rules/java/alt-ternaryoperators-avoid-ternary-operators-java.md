---
title: Ternary operators in Java can make code unreadable
url: https://doc.casthighlight.com/alt_ternaryoperators-avoid-ternary-operators-java/
slug: alt_ternaryoperators-avoid-ternary-operators-java
content_type: rule
languages: [java]
category: Changeability
has_code_examples: true
---

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)[Software Agility](http://casthighlight.wpengine.com/software-resiliency/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Ternary operators in Java can make code unreadable

This code insight counts one violation each time a ternary operator is encountered.

**Note** : Do not confuse with question mark used as wildcard for unknow generic type.

**bad**

```
String data = (str.contains("A") ? "Str contains 'A'" : "Str doesn't contains 'A'");
```

**good**

```
if (str.contains("A")) {
    data = "Str contains 'A'";
}
else {
     data = "Str doesn't contains 'A'";
}
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

While the ternary operator is pleasingly compact, its use can make code more difficult to read. It should therefore be avoided in favor of the more verbose if/elsestructure.

## **Business Impacts**

*It is recommended to avoid these in order to ensure the code is more readable and cost effective.*

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)

c
