---
title: Low commented code rates increase time and effort
url: https://doc.casthighlight.com/alt_weakcommentrate-avoid-weak-comment-rate/
slug: alt_weakcommentrate-avoid-weak-comment-rate
content_type: rule
category: Changeability
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Embedded Documentation](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/embedded-documentation/)

# **Why you should care**

Commented code lines rate is the percentage of lines of codes that are preceded with at least one line of comment. Comments are essential in every programming language for summarizing, communicating and clarifying sections of code – in order to assist others working on an application.

Low commented code lines can cause readability and collaboration issues among developers, which increases development time and effort.  When done properly, commenting can help maintain code expansions and help find bugs faster.

# **Business Impacts**

A low rate of commenting within an application increases the difficulty that different developers and different teams face when writing new code, since it takes more effort to interpret and modify existing code (this includes external clients who might need to interact directly with an API or otherwise). It also hurts development speed since comments also serve to guide the debugging process.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)Time / Effort

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends establishing an internal standard for code commenting. Ensuring that each application and their corresponding development team has a unified style guide, in order to standardize the type and commonality of comments.

Developers and project leaders should think about what portions of their codebase may require effort to understand and make appropriate, meaningful additions.  Nonetheless, they should avoid superfluous additions to sections that are self-explanatory. And finally there should be an emphasis on writing comments alongside the development process, rather than after the fact.

# **References**

<https://en.wikipedia.org/wiki/Comment_(computer_programming)>

<https://www.cs.utah.edu/~germain/PPS/Topics/commenting.html>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight computes the formula below after being uploaded on the portal:

**(Nbr\_CommentsBlocs / Nbr\_LinesOfCode) \* 100**

***Nbr\_LinesOfCode:***  
The total number of lines containing code items (syntax, string).  
Blank lines, comments and docstring are excluded

***Nbr\_CommentsBlocs:***   
Total number of comment blocs.  
A Comment bloc is a set of contiguous lines containing comment, or docstring, and no code items.  
Inlines comments count as a bloc.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
