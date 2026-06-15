---
title: Avoid binary operators with identical members
url: https://doc.casthighlight.com/alt_badvaluesoperator-avoid-binary-operators-identical-members/
slug: alt_badvaluesoperator-avoid-binary-operators-identical-members
content_type: rule
category: Robustness
has_code_examples: true
---

[SOFTWARE AGILITY](https://doc.casthighlight.com/software-agility/)

[CODE READABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Using the same value on either side of a binary operator is almost always a mistake. In the case of logical operators, it is either a copy/paste error and therefore a bug, or it is simply wasted code, and should be simplified. In the case of bitwise operators and most binary mathematical operators, having the same value on both sides of an operator yields predictable results, and should be simplified.

# **How we detect**

CAST Highlight counts one occurrence each time same values are detected before and after a logical operator as: ‘&&’ or ‘||’

Exceptions**:** This code insight ignores \*, +, << and =.

**Bad Code**

```
func main() {
  v1 := (true && false) && (true && false) // Noncompliant
}
```

**Good Code**

```
func main() {
  v1 := (true && false) // Compliant
}
```

# **References**

<https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>  
<https://rules.sonarsource.com/go/RSPEC-1764>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
