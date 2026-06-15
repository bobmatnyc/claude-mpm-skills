---
title: Avoid ‘if/else if’ & cases statements having the same condition
url: https://doc.casthighlight.com/alt_duplicatedcondition-avoid-else-cases-statements-condition/
slug: alt_duplicatedcondition-avoid-else-cases-statements-condition
content_type: rule
category: Changeability
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

A chain of if/else if statements is evaluated from top to bottom. At most, only one branch will be executed: the first one with a condition that evaluates to true.

Therefore, duplicating a condition automatically leads to dead code. Usually, this is due to a copy/paste error. At best, it’s simply dead code and at worst, it’s a bug that is likely to induce further bugs as the code is maintained, and obviously it could lead to unexpected behavior.

# **How we detect**

CAST Highlight counts one occurrence each time:

- PATTERN 1 : a whole condition is the same than a previous one in the sequence,
- PATTERN 2 : a simple condition is combined with “||” operator in a previous one in the sequence
- PATTERN 3 : a compound condition is combining with “||” operator a previous condition of the sequence

**Bad Code**

```
func example(condition1, condition2 bool) {
if condition1 {
} else if condition1 { // +1 VIOLATION (PATTERN 1)
}

if z || y{
} else if y { // +1 VIOLATION (PATTERN 2)
}


if a {
} else if a || b { // +1 VIOLATION (PATTERN 3)
}

if (a) {
} else if a || b { // +1 VIOLATION (PATTERN 3)
}

if foo && bar {
} else if (bar && foo) { // +1 VIOLATION (PATTERN 1) /!\ difficult to detect because simple conditions are not in the same order
}
}
```

# **References**

<https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>  
<https://rules.sonarsource.com/go/RSPEC-1862>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
