---
title: Javascript in HTML can be unreadable and cause reliability issues
url: https://doc.casthighlight.com/alt_include-avoid-include-javascript-files/
slug: alt_include-avoid-include-javascript-files
content_type: rule
languages: [java, javascript]
category: Efficiency
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Including JavaScript files in HTML is not ideal as some browsers cannot read an external Javascript file and usually renders it completely blank. It usually requires importing a Jquery. Having Javascript files be unreadable in HTML can cause reliability issues.

# **Business Impacts**

It is recommended to avoid JavaScript in HTML as it cannot be accessed by browsers making the code unreadable, inaccessible and unproductive. It can also be a waste of resources if the code is designed to be accessed as a website.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

https://stackoverflow.com/questions/17505563/javascript-file-not-working-when-linked-from-html

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight shows that JavaScript includes are sent by the server each time the page that include it is loaded. If you use the HTML tag to refer to this file, the browser doesn’t have to query for the static content for every page request. Most popular browser like IE, FireFox, Safari, Opera first check their local cache for the static file/resource and only if they don’t find do they make a request to the web server for the same.  
For JSP: create a link (html tag) instead of an include. It will be stored in the client cache instead of being sent each time the page is loaded

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
