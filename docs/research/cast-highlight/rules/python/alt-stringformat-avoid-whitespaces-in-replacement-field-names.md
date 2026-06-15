---
title: Whitespaces are a Production Risk
url: https://doc.casthighlight.com/alt_stringformat-avoid-whitespaces-in-replacement-field-names/
slug: alt_stringformat-avoid-whitespaces-in-replacement-field-names
content_type: rule
languages: [python]
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# Whitespaces are a Production Risk

Count one violation each time a format replacement field contains a whitespace.

**bad**

```
print "{ what} is {how it is}".format({"what": "life", "how it is": "hard"})


print "{ what} is {how it is}".format({" what": "life", "how it is": "hard"})
```

**good**

```
print "{what} is {how_it_is}".format({"what": "life", "how_it_is": "so much easier if you use QuantifiedCode"})
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

If you use a replacement field like `{ var}` in your format string, which contains a whitespace in its name, the key of the corresponding entry in your dictionary must contain this whitespace, too. Since whitespaces are easy to miss and you should avoid them.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/correctness/Avoid%20whitespaces%20in%20your%20replacement%20field%20names/9n9zeiZc

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
