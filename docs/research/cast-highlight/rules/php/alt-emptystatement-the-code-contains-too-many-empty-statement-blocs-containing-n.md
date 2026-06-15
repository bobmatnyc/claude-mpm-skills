---
title: Having empty statements can be unproductive in PHP
url: https://doc.casthighlight.com/alt_emptystatement-the-code-contains-too-many-empty-statement-blocs-containing-no-instructions/
slug: alt_emptystatement-the-code-contains-too-many-empty-statement-blocs-containing-no-instructions
content_type: rule
languages: [php]
category: Transferability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Having empty statements can be unproductive in PHP**

This code insight counts a violation each time an empty statement is detected in PHP

<?php

statement1 {  
// comment //Violation  
}

statement2 (conditions) {  
// comment //Violation  
}  
}  
}

Remedy –

Modify the source code to reduce the number of artifacts containing empty statements.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

For maintainability reasons, empty statements should be avoided. Empty statements make the source code harder to read and to maintain.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://pear.php.net/package/PHP\_CodeSniffer/docs/1.5.2/PHP\_CodeSniffer/Squiz\_Sniffs\_CodeAnalysis\_EmptyStatementSniff.html

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
