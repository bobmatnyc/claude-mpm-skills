---
title: Classes with missing destructor declarations can be unproductive
url: https://doc.casthighlight.com/alt_missingclassdestructor2_the-code-contains-too-many-classes-with-missing-destructor/
slug: alt_missingclassdestructor2_the-code-contains-too-many-classes-with-missing-destructor
content_type: rule
languages: [sql]
has_code_examples: false
---

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Classes with missing destructor declarations can be unproductive**

This code insight highlights a violation when a class has missing destructor declarations

class Vehicle  
{  
public:  
Vehicle();  
virtual ~Vehicle();  
void start();  
void stop();  
virtual void run();  
protected:  
Engine\* theEngine;  
};

class Car : public Vehicle  
{  
public:  
Car();  
~Car(); // VIOLATION  
protected:  
int numberOfWheels;  
};

Remedy

class Car : public Vehicle  
{  
public:  
Car();  
virtual ~Car(); // FIXED  
protected:  
int numberOfWheels;  
};

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

A missing virtual keyword in front of a destructor “overriding” a virtual destructor will hide the polymorphic nature of the destructor from developers using the class. They may not know that at execution time other destructors in the inheritance tree will be executed. A missing virtual keyword may also be an indication that the author of the destructor ignored the fact that it needed to be virtual and thus was not aware that the destructor requires specific attention and specific coding.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

https://www.tutorialspoint.com/sql/sql-transactions.htm

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
