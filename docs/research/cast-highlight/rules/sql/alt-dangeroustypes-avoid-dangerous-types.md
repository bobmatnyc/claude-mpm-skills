---
title: Avoid dangerous types
url: https://doc.casthighlight.com/alt_dangeroustypes-avoid-dangerous-types/
slug: alt_dangeroustypes-avoid-dangerous-types
content_type: rule
languages: [sql, cpp]
has_code_examples: false
---

- [C/C++ (MISRA)](#1583503416409-de9d93c4-839f)
- [PL/SQL](#1583503416435-a95fa63d-533a)

#### [C/C++ (MISRA)](#1583503416409-de9d93c4-839f)

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

The basic numerical types of char, int short, long, float, double, and long double should not be used directly to declare variable. This is because their storage size is machine dependent, and so for portability consideration, specific-lengths typedefs types should be used instead.

Example of usefull typedefs:

- typedef char char\_t;
- typedef signed char int8\_t;
- typedef unsigned char uint8\_t;
- typedef float float32\_t;
- typedef double float64\_t;

… and so on…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **References**

MISRA-Cpp-2008 3.9.2

# **How we detect**

Count one violation each time a variable is declared using directly one of the below basic type :

- char
- int
- short
- long
- float
- double

In addition, the Highlight implementation add the following:

- bool
- signed
- unsigned

Concerned variables are global variables, auto variable, class data members and struct fields.

Example of violations:

char c;  
unsigned int i;  
float f;

#### [PL/SQL](#1583503416435-a95fa63d-533a)

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

PLSQL include Datatypes such as LONG, CHAR, VARCHAR and VARCHAR2  
LONG datatype is used to store variable-length character strings with a maximum size of 32,760 bytes. They are only supported for backward compatibility with existing L79 applications while new applications use CLOB or NCLOB datatypes. CHAR datatype is used to hold fixed-length, blank padded strings with a max size of 32,767 bytes while VARCHAR datatypes is used to hold variable-length strings with the same size as CHAR. VARCHAR2 does not distniguish between a NULL or empty string unlike VARCHAR hence the possibility of VARCHAR causing more bugs.

# **Business Impacts**

It is useful to distinguish PLSQL Datatypes as proper implementation of datatypes result in greater productivity. Improper implementation of datatypes would cause a loss of time which would be unproductive in the long run.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/risk/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

# **References**

<https://docs.oracle.com/cd/B19306_01/appdev.102/b14261/datatypes.htm>  
<https://docs.oracle.com/cd/A97630_01/appdev.920/a96624/03_types.htm>  
<https://docs.oracle.com/cd/B28359_01/appdev.111/b28370/datatypes.htm#i43252>  
<https://stackoverflow.com/questions/1171196/what-is-the-difference-between-varchar-and-varchar2>

[Style Guide](https://github.com/Kristories/awesome-guidelines)

# **How we detect**

This code insight focuses on how the data represented internally depends on the database character set.  
CHAR[(maximum\_size [CHAR | BYTE] )]  
If you do not specify a maximum size, it defaults to 1. If you specify the maximum size in bytes rather than characters, a CHAR(n) variable might be too small to hold n multibyte characters. To avoid this possibility, use the notation CHAR(n CHAR) so that the variable can hold n characters in the database character set, even if some of those characters contain multiple bytes.  
CHAR is a fixed length data type which should only be used when appropriate. CHAR columns/variables are always filled to the specified length, this may lead to side-effects.  
VARCHAR : The VARCHAR data type is a subtype of VARCHAR2. There is a strong possibility, that the meaning of VARCHAR might change in future version of ANSI SQL Standard. ORACLE recommends that you avoid using VARCHAR and use VARCHAR2 instead.  
LONG : LONG and LONG RAW data type support will be discontinued in future  
ORACLE releases.

[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
