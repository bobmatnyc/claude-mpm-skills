---
title: % operator to format string can cause production risk
url: https://doc.casthighlight.com/alt_stringformat-avoid-operator-to-format-string/
slug: alt_stringformat-avoid-operator-to-format-string
content_type: rule
languages: [python]
category: Transferability
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# % operator to format string can cause production risk

Count one violation each time a string use the % operator.

**bad**

```
print("%s is %s" % ("`$`", "fine"))
```

**good**

```
print("{0} is {1}, much {1}".format("format", "better"))
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Future python version will promote usage of format().

[If possible, prefer using the `format()` function to perform string-formatting instead of the % operator. The former provides more advanced options, allows you to reuse arguments in your string and removes ambiguity.](https://www.quantifiedcode.com/knowledge-base/maintainability/Prefer%20%60format%28%29%60%20over%20string%20interpolation%20operator/4ACGxFj1)

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/maintainability/Prefer%20%60format%28%29%60%20over%20string%20interpolation%20operator/4ACGxFj1

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
