---
title: Avoid caching selector for long time
url: https://doc.casthighlight.com/alt_greedydataaccess-avoid-caching-selector-long-time/
slug: alt_greedydataaccess-avoid-caching-selector-long-time
content_type: rule
languages: [java, javascript]
category: Efficiency
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[BEST PRACTICES](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/best-practices/)

# **Why you should care**

Since object members may contain other members, it’s not uncommon to see patterns such as window.location.href in JavaScript code. These nested members cause the JavaScript engine to go through the object member resolution process each time a dot is encountered.

Reducing the dotation usage can win 50% of the time consumed by this function.

Generally speaking, if you’re going to read an object property more than one time in a function, it’s best to store that property value in a local variable. The local variable can then be used in place of the property to avoid the performance overhead of another property lookup. This is especially important when dealing with nested object members that have a more dramatic effect on execution speed.

JavaScript namespacing, such as the technique used in YUI, is a source of frequently accessed nested properties.

# **How we detect**

CAST Highlight counts one occurrence each time an object member is accessed with more than one dot whereas its dereference path has allready been used in the same scope.

**Note**: the scope for tracking derefereces reuses is limited to the content of a function, excluding inner functions contents.

**Bad Code**

```
function toggle(element){
  if (YAHOO.util.Dom.hasClass(
              element, "selected")){
      YAHOO.util.Dom.removeClass(
              element, "selected");
      return false;
  } else {
      YAHOO.util.Dom.addClass(
              element, "selected");
      return true; 
  }
}
```

**Good Code**

```
function toggle(element) {
  var Dom = YAHOO.util.Dom;
  if (Dom.hasClass(element, "selected")){
      Dom.removeClass(element, "selected");
      return false;
  } else {
      Dom.addClass(element, "selected");
      return true;
  }
}
```

# **References**

Coming soon…

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
