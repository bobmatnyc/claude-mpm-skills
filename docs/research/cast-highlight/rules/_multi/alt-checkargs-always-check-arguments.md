---
title: Leaving arguments unchecked hinders progress
url: https://doc.casthighlight.com/alt_checkargs-always-check-arguments/
slug: alt_checkargs-always-check-arguments
content_type: rule
category: Transferability
has_code_examples: true
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Code Reliability](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

Checking arguments is a critical component of Shell script.

The $# variable indicates the number of arguments.  If this variable is improperly implemented, then the arguments are left unchecked which can lead to improper execution and bugs in the code.

# **Business Impacts**

Leaving arguments unchecked on multiple shell scripts can be a blow to the overall portfolio.  This can cause productivity issues in an agile-based environment where some developers are trying to debug their code but end up over-complicating the process and leaving other developers without any progress to work towards.

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)[Complexity](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

# **CAST Recommendations**

CAST recommends checking arguments by adding spaces between its arguments like the following example below –

Incorrect –

```
if [$# -ne 1]; 
    then echo "illegal number of parameters"
fi
```

Correct –

```
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
fi
```

Instead of leaving arguments unchecked, they can be removed by adding shift like the following example below –

```
if (( $# < 3 )); then
  echo "$0 old_string new_string file [file...]"
  exit 0
else
  ostr="$1"; shift
  nstr="$1"; shift  
fi
```

These errors usually occur because the style-guide in the company is not followed by development teams or has not been updated for future projects.  For more help on checking arguments, refer to “Scripting Guide for Bash”

# **References**

https://stackoverflow.com/questions/18568706/check-number-of-arguments-passed-to-a-bash-script?rq=1

https://unix.stackexchange.com/questions/174566/what-is-the-purpose-of-using-shift-in-shell-scripts

[Shell Script Guide](http://tldp.org/LDP/abs/html/)

# **How we detect**

This code insight counts one violation each time the following patterns are encountered :

- **<indentifier> = $#**
- **$#  <op>** where <op> is  **-eq**, **-ne, -lt, -gt, -le, -ge, =, !=**
- **case $#**

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
