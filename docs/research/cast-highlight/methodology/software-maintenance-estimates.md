---
title: Software Maintenance Estimates
url: https://doc.casthighlight.com/software-maintenance-estimates/
slug: software-maintenance-estimates
content_type: methodology
---

## Definition

Based on [COCOMO II](https://en.wikipedia.org/wiki/COCOMO) (Constructive Cost Model – Post Architecture), the Software Maintenance Effort calculated by Highlight estimates the ideal level of effort in order to maintain an application in good operational conditions, expressed in FTE (Full-Time Equivalent). This indicator is derived both from the Software Maintenance survey and the software quality analysis which are computed during the source code scan.

## Example

An application presents the following characteristics:

- A consumer lending application, developed in Java, made of 177K lines of code
- An average maintenance effort of 20% over the last 12 months (evolutive maintenance excluded)
- An estimated code base change of 10% (added/modified lines of code vs. total lines of code) over the last 12 months
- The average skill level of the development team on this type of application is 3 years
- The annual staff turnover within the team is approximately 5%
- The organization in charge of developing/maintaining the application is CMMi level 4

In addition, based on the application code scan, the different quality indicators are:

- Software Agility: 91.6 out of 100 (benchmarked as being in the 1st quartile, i.e. 25% of the most adaptable applications)
- Software Elegance: 84.3 out of 100 (benchmarked as being in the 1st quartile, i.e. 25% of the less complex applications)
- Other computation parameters of the Software Maintenance Effort use the nominal values of [cost drivers](http://www.softstarsystems.com/cdtable.htm) as defined in COCOMO II

Highlight’s output

| Recorded Software Maintenance | Recommended Software Maintenance |
| --- | --- |
| 2.0 FTE | 0.9 FTE |
| *Representing 8.1 lines of code being modified/added for maintenance purpose, in average per FTE per day* | *Representing 18.9 lines of code being modified/added for maintenance purpose, in average per FTE per day* |

## Result Interpretation

**Application Level**The recommended maintenance effort calculated by Highlight can be compared with the recorded maintenance effort (as indicated by the application owner through the survey). Depending on the positive or negative gap between recorded and recommended values, you may decide to extend the maintenance team size (probably because the application health and/or the organizational context require more people to support the software maintenance effort) or to reallocate resources to other applications when necessary.

**Portfolio Level**  
At a glance, you can see the opportunity of a resource rationalization or reallocation initiative by looking at the number of applications for which you should increase or decrease the maintenance effort

[![3764](https://doc.casthighlight.com/wp-content/uploads/2017/05/CAST-Highlight-SoftwareMaintenance-Application.png)](https://doc.casthighlight.com/wp-content/uploads/2017/05/CAST-Highlight-SoftwareMaintenance-Application.png)

[![3765](https://doc.casthighlight.com/wp-content/uploads/2017/05/CAST-Highlight-SoftwareMaintenance-Portfolio.png)](https://doc.casthighlight.com/wp-content/uploads/2017/05/CAST-Highlight-SoftwareMaintenance-Portfolio.png)
