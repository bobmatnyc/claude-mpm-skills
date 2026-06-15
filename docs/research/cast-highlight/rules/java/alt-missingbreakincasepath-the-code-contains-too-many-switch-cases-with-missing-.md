---
title: Switch cases without ending breaks are hard to understand
url: https://doc.casthighlight.com/alt_missingbreakincasepath-the-code-contains-too-many-switch-cases-with-missing-ending-breaks/
slug: alt_missingbreakincasepath-the-code-contains-too-many-switch-cases-with-missing-ending-breaks
content_type: rule
languages: [java]
category: Transferability
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

## **Why you should care**

Although Switch cases do not require ending breaks after the default statement, It is recommended to end every branch with a return, or break statement, for the following reasons –

**Refactorability** – Branches ending with break or end can be easily reordered without having their changing their functionality.

**Consistency** – Similar branches should have a consistent ending as it makes the code easier to read and understand.

**Protection** – Ending all switch branches with a break is a fantastic habit as it helps in detecting missing break statements which is crucial for debugging and troubleshooting

## **Business Impacts**

Ending switch branches with ‘breaks’ helps the code be more consistent, functional, and easier to debug.  This allows developers in different teams navigate the code easier and be more productive in the development process.  Lack of breaks makes the code difficult for other developers to understand.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)[Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

### CAST recommendations

CAST recommends developers to build habits on making switch cases more readable by adding ending breaks where needed. This habit can be fostered by following a standardized guide internally set by the company which follows specific guidelines on writing code.  Not all switch cases need ending breaks so long as the code is understandable without compromising its’ functionality.

The key points to follow regarding switch cases is that the best programs are built from consistent code that focuses on functionality first.  Since many companies are shifting towards an agile-based environment, it is easy for development teams to get lost in the shuffle, especially with developers with their unique programming habits.  While having a style guide helps, it is also important to have developers undergo training and be constantly updated on new technologies that are to be implemented in future projects.

### References

https://softwareengineering.stackexchange.com/questions/201777/break-on-default-case-in-switch

https://www.tutorialspoint.com/java/java\_break\_statement.htm

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts a violation each time the code misses a break which fails to end ‘case’ clauses

int main()  
{  
int i = 2;  
switch(i)  
{  
case 0:  
cout << “0” << endl;  
// Violation  
case 1:  
// No violation: Empty clause  
case 2:  
cout << “1 or 2” << endl;  
break; // No violation: A break  
default:  
cout << “Other” << endl;  
// No violation: Last clause is default  
}  
}

It checks for a ‘switch’-clause that does not end with a ‘break’, ‘return’ or ‘throw’. This construct should be at the top level in the ‘switch’-clause.  However, the rule is also triggered if the last ‘switch’-clause of a ‘switch’ statement is ‘default’, and does not explicitly end with ‘break’, ‘return’ or ‘throw’.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
