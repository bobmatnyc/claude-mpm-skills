---
title: Extraneous whitespaces increase costs
url: https://doc.casthighlight.com/alt_badspacing-avoid-extraneous-whitespaces/
slug: alt_badspacing-avoid-extraneous-whitespaces
content_type: rule
languages: [java, javascript]
category: Efficiency
has_code_examples: true
---

[Software Agility](http://casthighlight.wpengine.com/software-agility/)[Code Readability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-agility/code-readability/)

# **Why you should care**

Avoid extraneous whitespace in the following situations:

- Immediately inside parentheses, brackets or braces.

  ```
  Yes: spam(ham[1], {eggs: 2})
  No:  spam( ham[ 1 ], { eggs: 2 } )
  ```
- Immediately before a:

  - comma
  - semicolon
  - colon (except when using as slice operator)

    ```
    Yes: if x == 4: print x, y; x, y = y, x
    No:  if x == 4 : print x , y ; x , y = y , x
    ```
- Immediately before the open parenthesis that starts the argument list of a function call:

  ```
  Yes: spam(1)
  No:  spam (1)
  ```
- Immediately before the open parenthesis that starts an indexing or slicing:

  ```
  Yes: dct['key'] = lst[index]
  No:  dct ['key'] = lst [index]
  ```
- More than one space around an assignment (or other) operator to align it with another.

  Yes:

  ```
  x = 1
  y = 2
  long_variable = 3
  ```

  No:

  ```
  x             = 1
  y             = 2
  long_variable = 3
  ```
- Don’t use spaces around the = sign when used to indicate a keyword argument or a default parameter value.

  Yes:

  ```
  def complex(real, imag=0.0):
      return magic(r=real, i=imag)
  ```

  No:

  ```
  def complex(real, imag = 0.0):
      return magic(r = real, i = imag)
  ```

# **Business Impacts**

It is recommended to avoid these in order to ensure the code is more readable and cost effective.

[Cost](http://casthighlight.wpengine.com/category/product/indicators-methodology/cost/)Time / Effort

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends having no space between function name and parenthesis.  The JavaScript style guidelines by Douglas Crockford establish very consistent rules that help the code work well and perform with cost efficiency.

# **References**

<https://stackoverflow.com/questions/9765942/space-after-function-name-is-wrong>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight count one violation each time a whitespace is encountered :just before :

- **openning parenthesis** following an identifier (except language keywords like : or, and, if, import, in,…)
- **closing parents** (when preceded by number or identifier)
- **openning brackets** following an identifier
- **closing** **bracket** (when preceded by number or identifier)
- **closing braces** (when preceded by number or identifier)
- **coma**
- **semicolon**
- **colon** (except when using as slice operator)

just after :

- **openning parenthese** (when followed by number or identifier)
- **openning bracket** (when followed by number or identifier)
- **openning braces** (when followed by number or identifier)

around:

- **assignment operator** when used to indicate a keyword argument or a default parameter value

more than one around

- **assignment operator**

**Notes**:

1 – whitespaces are not counted if they are considered as indentations, i.e. they are at line beginning.

2 – only one violation per operator : if there is one violation before and one violation after, only one is counted.

3 – if an openning item (parenthesis, bracket or braces) is followed by an unexpected blank space, then no violation will be counted if the corresponding closing is preceded too by an unexpected blank space.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
