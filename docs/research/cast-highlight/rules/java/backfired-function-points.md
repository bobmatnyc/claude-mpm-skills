---
title: Backfired Function Points
url: https://doc.casthighlight.com/backfired-function-points/
slug: backfired-function-points
content_type: rule
languages: [java, javascript, sql]
has_code_examples: false
---

## Definition

Back-Fired Function Points (BFP) estimate the number of function points of an application. This code-derived metric is based on the lines of code, weighted by a gearing factor for a given technology. The gearing factors are taken from [QSM](http://www.qsm.com/resources/function-point-languages-table) (Quantitative Software Management).

## Example

An application is composed of 3 different technologies:

- Java (100K lines of code)
- PL/SQL (20K lines of code)
- Javascript (10K lines of code)

The abacus table indicates how many source lines of code is observed in average to constitute one function points, for each technology:

- Java: 53 lines of code for 1 BFP
- PL/SQL: 37 lines of code for 1 BFP
- Javascript: 47 lines of code for 1 BFP

Back to our application example:

- Java represents ~1,886 BFPs
- PL/SQL represents ~540 BFPs
- Javascript represents ~212 BFPs
- Total application represents ~2,638 BFPs

This metric is captured each time an application is scanned with CAST Highlight and is presented over time in the TRENDS dashboard as shown below.

[![CAST-Highlight-Trends-BFP](https://casthighlight.wpengine.com/wp-content/uploads/2017/05/CAST-Highlight-Trends-BFP-1024x576.png)](http://casthighlight.wpengine.com/wp-content/uploads/2017/05/CAST-Highlight-Trends-BFP.png)
