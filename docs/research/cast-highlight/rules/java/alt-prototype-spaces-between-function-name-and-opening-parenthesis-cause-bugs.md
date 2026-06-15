---
title: Spaces between function name and opening parenthesis cause bugs
url: https://doc.casthighlight.com/alt_prototype-spaces-between-function-name-and-opening-parenthesis-cause-bugs/
slug: alt_prototype-spaces-between-function-name-and-opening-parenthesis-cause-bugs
content_type: rule
languages: [java, javascript]
category: Efficiency
has_code_examples: false
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

There should be no space between the name of a function and the ( (left parenthesis) of its parameter list, unless case of an anonymous literal function.  
If a function literal is anonymous, there should be one space between the word function and the ( (left parenthesis). If the space is omitted, then it can appear that the function’s name is function, which is an incorrect reading.

# **Business Impacts**

It is recommended to allow no spaces between the name of a function and the opening parenthesis of the list because more bugs in the portfolio and it prevents the code from being cost-effective.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)Time / Effort

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends having no space between function name and parenthesis.  The JavaScript style guidelines by Douglas Crockford establish very consistent rules that help the code work well and perform with cost efficiency.

# **References**

<https://stackoverflow.com/questions/9765942/space-after-function-name-is-wrong>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight counts one violation each time a function declaration has no space between its name and the opening parenthesis and each time an anonymous function declaration has one or more spaces between the ‘function’ keyword and the opening parenthesis.

function MyFunction (param) { // bad !!!

// good (it’s a literal anonymous function:  
div.onclick = function (e) {  
return false;  
};

that = {  
// bad (it’s a literal function)  
method: function literal\_fct (e) {  
return this.datum;  
},  
datum: 0  
};  
}

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
