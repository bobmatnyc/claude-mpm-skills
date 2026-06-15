---
title: Avoid self-assigned variables
url: https://doc.casthighlight.com/alt_selfassigned-avoid-self-assigned-variables/
slug: alt_selfassigned-avoid-self-assigned-variables
content_type: rule
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

There is no reason to re-assign a variable to itself. Either this statement is redundant and should be removed, or the re-assignment is a mistake and some other value or variable was intended for the assignment instead.

# **How we detect**

This Code Insight counts one occurrence each time a variable is re-assigned to itself.

**Bad Code**

```
func (user *User) rename(name string) {
name = name // Noncompliant
}
```

**Good Code**

```
func (user *User) rename(name string) {
user.name = name
}
```

# **References**

<https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>  
<https://rules.sonarsource.com/go/RSPEC-1656>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
