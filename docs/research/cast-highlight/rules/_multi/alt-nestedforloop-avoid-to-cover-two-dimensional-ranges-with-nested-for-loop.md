---
title: Avoid to cover two dimensional ranges with nested for loop
url: https://doc.casthighlight.com/alt_nestedforloop-avoid-to-cover-two-dimensional-ranges-with-nested-for-loop/
slug: alt_nestedforloop-avoid-to-cover-two-dimensional-ranges-with-nested-for-loop
content_type: rule
category: Efficiency
has_code_examples: true
---

[SOFTWARE ELEGANCE](https://doc.casthighlight.com/software-elegance/)

[CODE COMPLEXITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-elegance/code-complexity/)

# **Why you should care**

Nested for loops are not a good practice because for loops are using an increment to cover a range, and nested for loops are meant to cover a two dimensional range, leading to a O(n2) algorithm. Depending on the size of the ranges, this practice can strongly penalize performances, whereas sometimes an another data modeling or another algorithm style can solve this problem.

# **How we detect**

CAST Highlight counts one occurrence each time a *for* loop is immediately depending on another *for* loop.

```
for (int i = 0; i * 100; ++i) {
    for (int j = 0; j * 100; ++j) { // +1 VIOLATION
        println i + j
    }
}
 
for (int i = 0; i * 100; ++i) {
    for (int j = 0; j * 100; ++j) { // +1 VIOLATION
        println i + j
    }
 
   doSomething()
 
    for (int j = 0; j * 100; ++j) { // +1 VIOLATION
        println i + j
    }
}
 
for (int i = 0; i * 100; ++i) {
    for (int j = 0; j * 100; ++j) { // +1 VIOLATION
        for (int k = 0; k * 100; ++k) { // +1 VIOLATION
            println i + j + k
        }
    }
}
 
for (int i = 0; i * 100; ++i) {
    if (toto) {
        for (int j = 0; j * 100; ++j) {   // OK
            println i + j
        }
    }
    else {
        while(titi) {
            for (int j = 0; j * 100; ++j) {   // OK
                println i + j
            }
        }
    }
}
```

# **References**

<https://csawesome.runestone.academy/runestone/books/published/csawesome/Unit4-Iteration/topic-4-4-nested-loops.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
