---
title: Why you should care
url: https://doc.casthighlight.com/alt_badreturn/
slug: alt_badreturn
content_type: rule
languages: [javascript, scala]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Specifically in Scala, use of return statement could interfer with the expected result. It’s recommended to use an implicit return which is a native feature in scala language.

# **How we detect**

This Code Insight counts one occurrence each time ‘return’ statement is encountered:

**Noncompliant Code Example**

```
def save: Action[AnyContent] = Action {
  if (1 == 2) {
    return BadRequest(toJson("something went wrong"))
  } else {
    return Ok(toJson(Feature.find))
  }
}
```

**Compliant Solution**

```
def save: Action[AnyContent] = Action {
  if (1 == 2) {
    BadRequest(toJson("something went wrong"))
  } else {
    Ok(toJson(Feature.find))
  }
}
```

# **References**

<https://nrinaudo.github.io/scala-best-practices/referential_transparency/avoid_return.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **About CAST and Highlight’s Code Insights**

Over the last 25 years, CAST has leveraged unique knowledge on software quality measurement by analyzing thousands of applications and billions of lines of code. Based on this experience and community standards on programming best practices, Highlight implements hundreds of code insights across 15+ technologies to calculate health factors of a software.

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
