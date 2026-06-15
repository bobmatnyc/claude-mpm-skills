---
title: Multiline string literals should not be used
url: https://doc.casthighlight.com/alt_badlinecontinuation-multiline-string-literals-not-used/
slug: alt_badlinecontinuation-multiline-string-literals-not-used
content_type: rule
languages: [javascript]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Continuing a string across a linebreak is supported in most script engines, but it is not a part of ECMAScript. Additionally, the whitespace at the beginning of each line can’t be safely stripped at compile time, and any whitespace after the slash will result in tricky errors.

# **How we detect**

CAST Highlight counts one occurrence each time a multiline string is encountered, that is a string containing newline preceded by “\”.

**Bad Code**

```
var myString = 'A rather long string of English text, an error message \
actually that just keeps going and going -- an error \
message to make the Energizer bunny blush (right through \
those Schwarzenegger shades)! Where was I? Oh yes, \
you\'ve got an error and all the extraneous whitespace is \
just gravy. Have a nice day.'; // Noncompliant
```

**Good Code**

```
var myString = 'A rather long string of English text, an error message ' +
'actually that just keeps going and going -- an error ' +
'message to make the Energizer bunny blush (right through ' +
'those Schwarzenegger shades)! Where was I? Oh yes, ' +
'you\'ve got an error and all the extraneous whitespace is ' +
'just gravy. Have a nice day.';
```

# **References**

<https://rules.sonarsource.com/typescript/RSPEC-3616>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
