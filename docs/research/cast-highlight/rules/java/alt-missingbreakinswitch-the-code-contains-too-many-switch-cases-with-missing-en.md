---
title: The code contains too many switch cases with missing ending breaks
url: https://doc.casthighlight.com/alt_missingbreakinswitch-the-code-contains-too-many-switch-cases-with-missing-ending-breaks/
slug: alt_missingbreakinswitch-the-code-contains-too-many-switch-cases-with-missing-ending-breaks
content_type: rule
languages: [java]
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Ending switch branches with ‘breaks’ helps the code be more consistent, functional, and easier to debug. This allows developers in different teams navigate the code easier and be more productive in the development process. Lack of breaks makes the code difficult for other developers to understand.

# **How we detect**

CAST Highlight counts one occurrence each time a non empty case/default statement is not ending with a break, continue, return, or throw statement.

```
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
```

# **References**

<https://softwareengineering.stackexchange.com/questions/201777/break-on-default-case-in-switch>  
<https://www.tutorialspoint.com/java/java_break_statement.htm>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
