---
title: phpinfo() should not be used in production
url: https://doc.casthighlight.com/alt_debug-phpinfo-not-used-production/
slug: alt_debug-phpinfo-not-used-production
content_type: rule
languages: [javascript, php]
category: Security
has_code_examples: false
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

For security purpose, developers should not leave *phpinfo()* in production code, as it displays information which can be used to compromise the server that your site is running on.

# **How we detect**

CAST Highlight counts one occurrence each time phpinfo() is found into the source code.

# **References**

<https://www.drupal.org/node/243993>  
<https://serverfault.com/questions/194440/security-risks-of-having-public-phpinfo-page>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **About CAST and Highlight’s Code Insights**

Over the last 25 years, CAST has leveraged unique knowledge on software quality measurement by analyzing thousands of applications and billions of lines of code. Based on this experience and community standards on programming best practices, Highlight implements hundreds of code insights across 15+ technologies to calculate health factors of a software.

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
