---
title: Too many functions with default value parameters are unproductive
url: https://doc.casthighlight.com/alt_parameters-the-code-contains-too-many-functions-whose-parameters-having-a-default-value-dont-come-at-the-end-of-the-function-signature/
slug: alt_parameters-the-code-contains-too-many-functions-whose-parameters-having-a-default-value-dont-come-at-the-end-of-the-function-signature
content_type: rule
languages: [php]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Too many functions with default value parameters are unproductive**

This code insight counts a violation each time parameter has a default value

“class CastTest  
{  
public function addData( $param0, $param1, $param2, $param3, $param4, $param5, $param5, $param6, $param7, $param8, $param9, $param10)  
{  
}  
}”

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Long parameter lists can indicate that a new object should be created to wrap the numerous parameters. In other words, always try to group the parameters together.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://phpmd.org/rules/codesize.html#excessiveparameterlist

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
