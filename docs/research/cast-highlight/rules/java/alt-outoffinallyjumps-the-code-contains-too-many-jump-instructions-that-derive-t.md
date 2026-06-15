---
title: The code contains too many jump instructions that derive the control flow out of a finally structure
url: https://doc.casthighlight.com/alt_outoffinallyjumps-the-code-contains-too-many-jump-instructions-that-derive-the-control-flow-out-of-a-finally-structure/
slug: alt_outoffinallyjumps-the-code-contains-too-many-jump-instructions-that-derive-the-control-flow-out-of-a-finally-structure
content_type: rule
languages: [java]
category: Security
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Using return, break, throw, and continue from a finally block overwrites similar statements from the suspended try and catch blocks.

# **How we detect**

CAST Highlight counts one occurrence each time a jump statement (break, continue, return and throw) would force control flow to leave a finally block.

**Bad Code**

```
try {
console.log('test')
}
catch(e) {
console.log(e);
}
finally{
throw new Error('Something bad happened'); // Noncompliant
}
```

**Good Code**

```
function foo() {
try {
return 1; // We expect 1 to be returned
} catch(err) {
return 2; // Or 2 in cases of error
}
}
```

# **References**

<https://wiki.sei.cmu.edu/confluence/display/java/ERR04-J.+Do+not+complete+abruptly+from+a+finally+block>  
<https://owasp.org/www-community/vulnerabilities/Return_Inside_Finally_Block>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
