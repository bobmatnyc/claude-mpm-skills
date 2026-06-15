---
title: Avoid literal numbers (i.e. Magic numbers are not so magic)
url: https://doc.casthighlight.com/alt_magicnumbers-avoid-literal-numbers-e-magic-numbers-not-magic/
slug: alt_magicnumbers-avoid-literal-numbers-e-magic-numbers-not-magic
content_type: rule
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/programming-best-practices/)

# **Why you should care**

A magic number is a direct usage of a number in the code (e.g. “if($foo > 65)”) which refers to a specific value that can’t be easily understood by just reading it. Using too many magic numbers can lead to these types of issues:

– Confusing: the developer (who is often not the same person as the initial software author) doesn’t quickly understand what this value means in the context of the application (why 65? why not 64 or 66?). Here, 65 refers to the legal age for work retirement in the United Kingdom.

– Counter-productive: if the value is used by other source files (across components, microservices, etc.) and needs to be changed (e.g. the legal age for retirement will change next year in the UK and will be 67), you’re development team will have to modify all places where this value is used.

# **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

From an software engineering perspective, it is recommended to manage this value globally, in a way that other files, components … can access it from a single place, as shown in the example below.

**Suspicious Code Pattern:**

public class Foo {  
public void setPassword(String password) {  
// don’t do this  
if (password.length() > 7) {  
throw new InvalidArgumentException(“password”);  
}  
}  
}

**Refactored Code:**

public class Foo {  
public static final int MAX\_PASSWORD\_SIZE = 7;

public void setPassword(String password) {  
if (password.length() > MAX\_PASSWORD\_SIZE) {  
throw new InvalidArgumentException(“password”);  
}  
}  
}

# **References**

<https://en.wikipedia.org/wiki/Magic_number_(programming)>  
<http://eslint.org/docs/rules/no-magic-numbers>  
<https://refactoring.guru/replace-magic-number-with-symbolic-constant>  
<https://stackoverflow.com/questions/47882/what-is-a-magic-number-and-why-is-it-bad>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts the number of cases where a literal number found in the code could be considered a magic number.  Depending on the usage frequency, and based on specific thresholds CAST has defined by analyzing billions lines of code over the last 25 years, Highlight counts penalty points to the scanned source file accordingly. Literal numbers are excluded from this code insight when:

– Used as an initialization when declaring a variable  
– Are one the following autorized numbers: 0.0, 1.0, 0., 1., or an integer from 0 to 9

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
