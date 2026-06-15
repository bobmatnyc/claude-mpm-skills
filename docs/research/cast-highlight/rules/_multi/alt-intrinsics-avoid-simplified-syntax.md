---
title: Simplified Syntax can be unproductive in KSH
url: https://doc.casthighlight.com/alt_intrinsics-avoid-simplified-syntax/
slug: alt_intrinsics-avoid-simplified-syntax
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/category/product/indicators-methodology/software-resiliency)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Using the simplified, but deprecated/discouraged commands in shell scripts can lead to minor unpredictability and less feature flexibility. It is better practice to stick to the established alternatives to these two commands, for readability, consistency and expansion.

# **Why you should care**

Using certain syntax in shell, like these simplified commands can have issues with behavioral consistency and flexibility. Avoiding modern syntax can potentially lead to unexpected application behavior and increased development time debugging.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

Encouraging developers to read up on the latest syntax/suggested style for shell – in order to reduce their use of outdated/partially deprecated commands, even if their use might simplify the appearance of the code.

# **References**

https://stackoverflow.com/questions/669452/is-double-square-brackets-preferable-over-single-square-brackets-in-ba

https://stackoverflow.com/questions/22709371/backticks-vs-braces-in-bash

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts one violation each time following pattern for command execution and conditions are encountered :

- **` *<command>* `**
- **[ *<condition>* ]**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
