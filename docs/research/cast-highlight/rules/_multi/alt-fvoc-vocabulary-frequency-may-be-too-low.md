---
title: The vocabulary frequency is too low
url: https://doc.casthighlight.com/alt_fvoc-vocabulary-frequency-may-be-too-low/
slug: alt_fvoc-vocabulary-frequency-may-be-too-low
content_type: rule
category: Transferability
has_code_examples: false
---

## **The code vocabulary frequency may be too low**

SOFTWARE ELEGANCE

CODE COMPLEXITY

This code insight – a derived metric from Halstead complexity measures – evaluates if a source file has a correct level of keyword variety (i.e. the ratio between the total number of operators/operand and the number of distinct operators/operands). If this ratio is high, it means your code could be semantically poor and globally harder to understand. Depending on Halstead recommendations and thresholds defined by CAST and based on an experience of 25 years in software measurement, Highlight counts penalty points for the scanned file if the vocabulary frequency is too low.

### **Why you should care**

Understanding what a piece of code is supposed to do relies on many aspects like documentation, good naming conventions, etc. The vocabulary frequency can also help developers to understand and maintain the code more easily.  Ensuring your software has a well-balanced number of different keywords that a programming language offers tends to reduce the time necessary for a developer to handle it efficiently – especially if he’s not the primary code author.

### **Searched Pattern**

This code insight is a metric that calculate the ratio between the number of distinct words and the total number of word.

Are considered as words :

- the identifiers
- the keywords
- the following operators : …, <<= >>=  != %= &= \*= = -= /= = |= && || + —  ->  <<  <=  ==  >=  >>  !  %  &  \*  +  ,  –  .  /  <  =  >  ?   ^  | {  ;
- : except in a case pattern
- ( and [ except when following an indentifier or a keyword

[SEE FEATURES & ANALYTICS](http://casthighlight.wpengine.com/outputs-analytics/)

[HOW IT WORKS](http://casthighlight.wpengine.com/how-it-works/)
