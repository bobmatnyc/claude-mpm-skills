---
title: String concatenation in loop causes production risks
url: https://doc.casthighlight.com/alt_concatinloop-avoid-string-concatenation-in-loops/
slug: alt_concatinloop-avoid-string-concatenation-in-loops
content_type: rule
category: Efficiency
has_code_examples: true
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# String concatenation in loop causes production risks

This code insight counts one violation each time an operator + or += is used with a string parameter inside a loop.

Note : the rule is restricted to expression with litteral string. Variable string need semantic to be detected.

**bad**

```
employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
        employee_table += '</table>'
```

**good**

```
items = ['<table>']
    for last_name, first_name in employee_list:
        items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
        items.append('</table>')
    employee_table = ''.join(items)
```

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Avoid using the + and += operators to accumulate a string within a loop. Since strings are immutable, this creates unnecessary temporary objects and results in quadratic rather than linear running time. Instead, add each substring to a list and ”.join the list after the loop terminates (or, write each substring to a io.BytesIO buffer).

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.quantifiedcode.com/knowledge-base/performance/Use%20%60extend%28%29%60%20for%20list%20concatenation/3kr7yXet

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
