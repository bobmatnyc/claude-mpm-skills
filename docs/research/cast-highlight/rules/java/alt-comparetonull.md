---
title: Why you should care
url: https://doc.casthighlight.com/alt_comparetonull/
slug: alt_comparetonull
content_type: rule
languages: [java, javascript, scala]
category: Robustness
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Whenever null seems like a good idea, use Option instead.

As far as types are concerned, `null` is a bit of a lie:

```
val s: String = null
```

The compiler believes `s` to be a [`String`](https://docs.oracle.com/javase/8/docs/api/java/lang/String.html) and will accept it wherever one is required. The compiler is, obviously, wrong:

```
s.toLowerCase
// java.lang.NullPointerException
// 	at repl.Session$App$$anonfun$2.apply(avoid_null.md:15)
// 	at repl.Session$App$$anonfun$2.apply(avoid_null.md:15)
```

Whenever you’re using `null`, you’re hindering the compiler’s ability to prove your code incorrect.

# **How we detect**

This Code Insight counts one occurrence each time null is used (strings are not concerned):

**Non-compliant Code Example**

```
object HelloWorld {
	def concat(a: String, b: String): String = {
		if(a == null)      b     		else if(b == null) a    		else               s"$a$b"
	}
}
```

**Compliant Solution**

```
object HelloWorld {
	def concat(a: Option[String], b: Option[String]): String =
		s"${a.getOrElse("")}${b.getOrElse("")}"
}
```

–

# **References**

<https://nrinaudo.github.io/scala-best-practices/unsafe/avoid_null.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **About CAST and Highlight’s Code Insights**

Over the last 25 years, CAST has leveraged unique knowledge on software quality measurement by analyzing thousands of applications and billions of lines of code. Based on this experience and community standards on programming best practices, Highlight implements hundreds of code insights across 15+ technologies to calculate health factors of a software.

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
