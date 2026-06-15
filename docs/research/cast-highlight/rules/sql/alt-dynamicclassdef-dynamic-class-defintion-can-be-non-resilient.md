---
title: Incorrect dynamic class definition can be non-resilient
url: https://doc.casthighlight.com/alt_dynamicclassdef_dynamic-class-defintion-can-be-non-resilient/
slug: alt_dynamicclassdef_dynamic-class-defintion-can-be-non-resilient
content_type: rule
languages: [sql]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Incorrect dynamic class definition can be non-resilient**

This count insight counts a violation in this non-compliant code example, the function A<int>::f2() is ill-formed because int is not a class and does not have a member named x. Clearly the designer of template A did not intend it to be applied to {{int}}.

However the compiler is not required to catch the error, as it does not need to instantiate A<int>::f2(). Consequently the program will compile, run, and most likely produce flawed results.

template <typename T>  
class A {  
public:  
void f1() { /\* … \*/ }  
void f2() {  
T t;  
t.x = 50;  
}  
};

int main() {  
A<int> a;  
a.f1();  
}

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

All templates place restrictions on their arguments; however these restrictions are often not validated by the compiler. Consequently, it is possible to build and run code that violates a template’s design principles, as long as it doesn’t actually instantiate the ill-formed instantiations. Furthermore implicit template instantiations can always be made explicit by an attacker, subverting the design.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
