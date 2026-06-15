---
title: File Records with no COPY Clause can be risky
url: https://doc.casthighlight.com/alt_nocopyclause_avoid-file-records-not-in-in-copy-clause/
slug: alt_nocopyclause_avoid-file-records-not-in-in-copy-clause
content_type: rule
has_code_examples: false
---

[Software Resiliency](http://casthighlight.wpengine.com/software-resiliency/)[Programming Best Practices](http://casthighlight.wpengine.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# File Records with no COPY Clause can be risky

This code insight count a violation each time a file record has more than one data and is not in a copy clause.

**Bad**:

000130 DATA DIVISION.  
000140 FILE SECTION.  
000150 **FD** SALES-FILE  
000160       RECORDING MODE IS F.  
000170  
000180 01 SALES-RECORD.  
000190       05 BROKER-REGION PIC 9.  
000200       05 BROKER-CITY PIC X(19).  
000210       05 BROKER-NAME PIC X(20).  
000220  
000230 WORKING-STORAGE SECTION.

**Good** :

000130 DATA DIVISION.  
000140 FILE SECTION.  
000150 **FD** STUDENT-FILE  
000160 RECORD CONTAINS 43 CHARACTERS  
000170 DATA RECORD IS STUDENT-IN.  
000180 01 STUDENT-IN PIC X(43).  
000190  
000200 **FD** PRINT-FILE  
000210       RECORD CONTAINS 80 CHARACTERS  
000220       DATA RECORD IS PRINT-LINE.  
000230  COPY CopyPrintFileRecord  
000240  
000250 WORKING-STORAGE SECTION.

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

## **Why you should care**

File records should be described in a copy clause.

## **Business Impacts**

[Production Risk](http://casthighlight.wpengine.com/category/product/indicators-methodology/innovation/)

### CAST recommendations

### References

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)[See features](http://casthighlight.wpengine.com/outputs-analytics/)[How it works](http://casthighlight.wpengine.com/how-it-works/)
