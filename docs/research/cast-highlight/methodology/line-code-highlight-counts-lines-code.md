---
title: What is a line of code and how Highlight counts them
url: https://doc.casthighlight.com/line-code-highlight-counts-lines-code/
slug: line-code-highlight-counts-lines-code
content_type: methodology
category: Changeability
---

Sometimes, this question is raised by new users: how CAST Highlight counts lines of code compared to classic static code analysis tools and how to explain possible differences. While there is no truer or better methodology than another for counting lines of code, the most important in order to get consistent results is to use the same approach to compare metrics over time and across applications, projects, etc.

In Highlight, the analyzers count physical lines of code where non-commented instructions can be found. Below are the different possible cases.

- var foo = 42; => 1 line of code
- var foo = 42; foo += 12; => 1 line of code
- var foo = 42; // some comment => 1 line of code
- { => 1 line of code
- } => 1 line of code
- { var foo = 42; } => 1 line of code
- // some comment => 0 line of code
- // var foo = 42 => 0 line of code
- BLANK/EMPTY LINE => 0 line of code

#### Some basic examples

7 lines of JS code

// this is some JS code  
var foo = 42; // my favorite number  
var misc = 4;

while(misc > 0) {  
   // foo = foo – misc;  
   foo -= misc;  
   misc -= 1;  
}

/\*\*  
The result should be something like 32  
\*\*/

alert(foo);

10 lines of PHP code

<?php // account for 1 line of code

include(‘functions.php’);

/\*\*  
THIS IS A PHP SCRIPT  
\*\*/

$foo = 42; $i = 10;

while($i > 0)  
{  
   $foo = $foo – $i;  
   $i = $i – 1;  
}  
?>  
<div>  
   <strong><?=$foo?></strong>  
</div>

#### Q&As

**Is generated code taken into account in lines of code?**  
If the generated code is part of the [scan scope](https://doc.casthighlight.com/good-practices-defining-scope-code-scan/) and written in one of [the technologies supported by CAST Highlight](https://doc.casthighlight.com/#technologycoverage), it will be taken into account.

**Are project or configuration files taken into account in lines of code?**  
Project and configuration files such as pom.xml, .json, .vcsproj … are not counted as lines of code.

**Are binary files taken into account in lines of code?**  
Binary files such as JARs, DLLs, EXEs … are not counted as lines of code.

**Are third-party component lines of code taken into account?**  
Yes, if third-party component files are readable source code (i.e., not binary files) and not excluded from the scan (e.g., minified files in JavaScript are automatically excluded from the analysis).

**Are annotations taken into account?**  
No, annotations (e.g., @Override) are not considered in the count of code lines.

**Are lines of code of unsupported technologies taken into account?**  
No, the count of lines of code takes only supported technologies into account. [Please refer to the list of supported technologies](https://doc.casthighlight.com/#technologycoverage).
