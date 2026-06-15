---
title: Memory leaks in C++ is a huge production risk
url: https://doc.casthighlight.com/alt_mallocfreeuses_count-one-violation-each-time-malloc-or-free-keyword-is-encountered/
slug: alt_mallocfreeuses_count-one-violation-each-time-malloc-or-free-keyword-is-encountered
content_type: rule
languages: [cpp]
category: Robustness
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Memory leaks in C++ is a huge production risk**

This code insight counts a violation each time a Call free or delete to free the memory.  List all locations where a memory allocation is created (malloc/calloc/realloc, new, and std::auto\_ptr.release()) that is not freed (using free or delete).

void f()  
{  
int \*array = calloc(1024, sizeof(int));  
/\* Do some work with array here \*/  
// VIOLATION: Memory not freed  
}

Remedy

void f()  
{  
int \*array = calloc(1024, sizeof(int));  
/\* Do some work with array here \*/  
free(array); // REMEDIATION  
}

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Memory leaks ultimately mean available memory is gradually reduced leading to various problems ranging from poor responsiveness to a system/application crash

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

http://en.wikipedia.org/wiki/Memory\_leak

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
