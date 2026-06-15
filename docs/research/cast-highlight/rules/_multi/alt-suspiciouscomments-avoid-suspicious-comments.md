---
title: Suspicious Comments can increase costs due to their suspicious nature
url: https://doc.casthighlight.com/alt_suspiciouscomments-avoid-suspicious-comments/
slug: alt_suspiciouscomments-avoid-suspicious-comments
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

# **Why you should care**

Avoid (in production code) comments that reveals that the code could not be finalized or not mature.

# **Business Impacts**

It is recommended to avoid these in order to ensure the code is more readable and cost effective.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

Count one violation each time one comment bloc (one or more contiguous lines of comment) contains at least one of the following patterns :

- two or more successive **!** and/or **?**.
- following expressions :  **[àa] (v[ée]rifier|faire|voir|revoir)**
- following keywords**: todo**, **fixme**, **tbc**, **tbd**, **attention**
- english expressions **: to be (verified|done)**
- english keywords **: warning**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
