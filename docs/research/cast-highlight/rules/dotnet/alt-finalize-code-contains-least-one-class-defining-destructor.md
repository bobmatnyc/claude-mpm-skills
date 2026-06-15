---
title: The code contains at least one class defining a destructor
url: https://doc.casthighlight.com/alt_finalize-code-contains-least-one-class-defining-destructor/
slug: alt_finalize-code-contains-least-one-class-defining-destructor
content_type: rule
languages: [dotnet]
category: Efficiency
has_code_examples: true
---

[SOFTWARE RESILIENCY](https://doc.casthighlight.com/software-resiliency/)

[CODE RELIABILITY](https://doc.casthighlight.com/category/product/indicators-methodology/code-insights/software-resiliency/code-reliability/)

# **Why you should care**

For several reasons detailed in references, using finalizers is not recommended:

- The finalization is not determined. You don’t know when the finalizer will be called
- Due to the fact that an object with the finalizer does not get removed by the garbage collector immediately, the object, and the entire graph of dependent objects, go through the garbage collection and promote to the next generation. They will be removed only when the garbage collector decides to collect objects of this generation, which can take quite a while
- Since the finalizers run in a separate thread in parallel with other threads of the application, a programmer may have a situation when the new objects, requiring finalization, will be created faster than the finalizers of old objects will complete the execution. This will lead to increased memory consumption, decreased performance, and perhaps eventually to the crash of the application with OutOfMemoryException
- A finalizer may be not executed at all. Upon the abortion of the application, for example, if there is an exception thrown in somebody’s finalizer due to any of the reasons described above, no other finalizers will be executed. If you free unmanaged objects of the operating system, there will be nothing wrong in the way that the operating system returns its resources when the application terminates. But if you put unwritten bytes to the file, you will lose your data

# **How we detect**

CAST Highlight counts one occurrence each time a finalizer is detected. A finalizer is detected by the presence of “~” preceding a method name that is also the name of a class.

```
class Nested
{
public void DoSomeWork()
{
Console.WriteLine(String.Format(
"Thread {0} enters DoSomeWork",
Thread.CurrentThread.ManagedThreadId));
Thread.Sleep(2000);
Console.WriteLine(String.Format(
"Thread {0} leaves DoSomeWork",
Thread.CurrentThread.ManagedThreadId));
}
~Nested()
{
Console.WriteLine("Finalization of Nested");
DoSomeWork();
}
}
```

# **References**

<https://pvs-studio.com/en/blog/posts/csharp/0437/>

![5362](https://doc.casthighlight.com/wp-content/uploads/2018/02/map-shadow.png)

[SEE FEATURES](https://www.castsoftware.com/products/highlight/outputs-analytics)

[HOW IT WORKS](https://www.castsoftware.com/products/highlight/how-it-works)
