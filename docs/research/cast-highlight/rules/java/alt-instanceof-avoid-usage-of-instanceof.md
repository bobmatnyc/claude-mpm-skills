---
title: Using “instanceOf” causes Production Risk
url: https://doc.casthighlight.com/alt_instanceof_avoid-usage-of-instanceof/
slug: alt_instanceof_avoid-usage-of-instanceof
content_type: rule
languages: [java]
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **How we detect**

This code insight counts a violation each time an “instanceOf” is utilized

public final class BadInstanceOf {

public static void doSomething(Animal aAnimal){  
if (aAnimal instanceof Fish){  
Fish fish = (Fish)aAnimal;  
fish.swim();  
}  
else if (aAnimal instanceof Spider){  
Spider spider = (Spider)aAnimal;  
spider.crawl();  
}  
}

// PRIVATE //  
private static class Animal {}

private static final class Fish extends Animal {  
void swim(){}  
}  
private static final class Spider extends Animal {  
void crawl(){}  
}  
}

Remedy –

public final class BadInstanceOfFixed {

public static void doSomething(Animal aAnimal){  
//calls different versions of move, specific to  
//each Animal  
aAnimal.move();  
}

// PRIVATE //  
private static class Animal {  
void move(){  
//do nothing  
}  
}

private static final class Fish extends Animal {  
void move(){  
//move like a fish  
}  
}  
private static final class Spider extends Animal {  
void move(){  
//move like a spider  
}  
}  
}

This report lists all artifacts that reference instanceOf used with an internal class or interface as argument.  
It provides the following information:  
Artifact full name, the number of occurrences of this detected in the artifact

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

Usually instanceOf is synonym of a bad design when it is used with against classes that you are developping.  
instanceof operator should be used only as a last resort, and that an overridden method is usually (but not always) a better alternative.

## **Business Impacts**

*Having a series of “InstanceOf” in an application is considered to be bad design from a technical perspective and that can lead to a lack of productivity in one’s portfolio.*

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

<http://www.javapractices.com/topic/TopicAction.do?Id=31>  
<http://www.artima.com/objectsandjava/webuscript/PolymorphismInterfaces1.html>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
