---
title: Single quote strings keeps code consistent and productive
url: https://doc.casthighlight.com/alt_string-prefer-simple-quotes-strings/
slug: alt_string-prefer-simple-quotes-strings
content_type: rule
languages: [java, javascript]
category: Robustness
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Single quote strings keeps code consistent and productive**

This code insight counts a violation each time a string is enclosed with double quotes, except if the string contains single quotes within double quotes.

**bad**:

“it is a bad string”  
“it is a \”bad\” string”

**good**:

“it ‘ s a good string”

var JSONObject=’ {  
“name”:”John Johnson”,  
“street”:”Oslo West 555″,  
“age”:33,  
“phone”:”555 1234567″}’;

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

It is helpful to keep consistent during development so that bugs and miscommunication can be prevented.  Single-quotes (‘) are preferred to double-quotes (“) because it is more consistent.  It is important to avoid mixing the types of quotes because that would result in the code from functioning properly and inefficiently.

An exception should be noted that double-quotes (“) are used to writing JSON as it’s libraries do not support single-quotes (‘).  This is helpful when creating strings that include HTML or to generate JSON.

## **Business Impacts**

Keeping consistent during development is important because preventing possible bugs and miscommunication between the team helps the code in being resilient which maximizes its’ productivity.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

CAST recommends keeping your code consistent because that engenders healthy programming and more collaborative development which is reflective of how programming has changed in the more recent years as its taken a more Agile-based approach.  Inconsistent code has the opposite effect and ill-advised, hence keeping single quotes can be one of the many steps towards ensuring your code is productive.

### References

https://stackoverflow.com/questions/242813/when-to-use-double-or-single-quotes-in-javascript

http://www.agile-process.org/

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
