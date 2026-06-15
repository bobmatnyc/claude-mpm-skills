---
title: Avoid dead code
url: https://doc.casthighlight.com/alt_deadcode-avoid-dead-code/
slug: alt_deadcode-avoid-dead-code
content_type: rule
languages: [swift]
category: Changeability
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Dead code are instructions that can never be reached. Obvious dead code are instructions that follow unconditional jumps in the same statement block.

Dead code could just be deactivated functionalities, but in this case, it should not be present in production.

# **How we detect**

CAST Highlight counts one occurrence each time a statement is detected after a jump statement (i.e. return, break, continue, and fallthrough) in the same current block.

**Bad Code**

```
func fun(a:Int)->Int{
var i = 10;
return i + a;
i++; // this is never executed
}
```

Good Code

```
func fun(a:Int)->Int{
  var i = 10;
  return i + a;
}
```

# **References**

<http://cwe.mitre.org/data/definitions/561.html>  
<https://rules.sonarsource.com/swift/RSPEC-1763>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
