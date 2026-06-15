---
title: Builtin instructions are inadvisable because of their risky nature
url: https://doc.casthighlight.com/alt_riskyfunctioncalls-avoid-using-risky-builtins/
slug: alt_riskyfunctioncalls-avoid-using-risky-builtins
content_type: rule
languages: [php, dotnet]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Certain built-in commands in VB/VB.net bring about unnecessary reliability risk to applications.

This unexpected application or machine behavior occurs a result of awkward/unreliable methods of handling errors and interacting with memory – that includes using pointers, forcing garbage collection, unstructured exception handling etc.

# **Business Impacts**

The use of certain (unrecommended) built-in commands can increase the likelihood for applications to malfunction and fail in a production environment. Debugging and working with these commands can increase development time significantly.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)[Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST recommendations**

Identifying the built-in functions that can potentially cause reliability issues from the patterns above and encourage developers to seek alternatives to these risky commands. Documentation of most of these identified issues can be easily found online and in the references below.

### References

<https://stackoverflow.com/questions/118633/whats-so-wrong-about-using-gc-collect>

<http://www.vbforums.com/showthread.php?759361-RESOLVED-Need-Full-Understanding-of-VarPtr-StrPtr-ObjPtr>

<https://docs.microsoft.com/en-us/dotnet/visual-basic/language-reference/statements/resume-statement>

<https://stackoverflow.com/questions/29418248/what-does-the-vb-net-ubound-function-actually-do-and-why-does-the-msdn-document>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight follows code which contains “**system**” and “**gc**“, count one violation each time “**collect (**” is encountered.

Count one violation each time following patterns are encountered :

- **objptr**
- **strptr**
- **varptr**
- **ismissing**
- **as new**
- **resume**
- **for … lbound**
- **to … ubound**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
