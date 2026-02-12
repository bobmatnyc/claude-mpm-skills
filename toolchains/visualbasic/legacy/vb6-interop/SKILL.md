---
name: vb6-legacy
description: Classic VB6 patterns, COM interop, migration strategies
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
tags: [visualbasic, vb6, legacy, com, interop, migration]
---

# VB6 Legacy and COM Interop

Patterns for maintaining VB6 code and strategies for migrating to VB.NET with COM interop.

## VB6 to VB.NET Migration

### Key Differences

```vb
' VB6 - Variant types
Dim data As Variant
data = 123
data = "Hello"

' VB.NET - Strong typing with Option Strict On
Option Strict On
Dim data As Object  ' Still avoid when possible
Dim number As Integer = 123
Dim text As String = "Hello"

' VB6 - Default properties
Text1.Text = "Hello"
Text1 = "Hello"  ' Uses default Text property

' VB.NET - Explicit properties required
TextBox1.Text = "Hello"  ' Must be explicit

' VB6 - ByRef default
Sub ProcessData(data As String)  ' ByRef by default

' VB.NET - ByVal default
Sub ProcessData(data As String)  ' ByVal by default
Sub ProcessData(ByRef data As String)  ' Explicit ByRef

' VB6 - On Error
On Error Resume Next
On Error GoTo ErrorHandler

' VB.NET - Try-Catch
Try
    ' Code
Catch ex As Exception
    ' Handle error
End Try
```

### Common Migration Issues

```vb
' VB6 - Fixed-length strings
Dim name As String * 50

' VB.NET - Use regular string and PadRight
Dim name As String = "John".PadRight(50)

' VB6 - Currency type
Dim amount As Currency

' VB.NET - Use Decimal
Dim amount As Decimal

' VB6 - Control arrays
Dim TextBox(5) As TextBox

' VB.NET - Use collection
Dim textBoxes As New List(Of TextBox)()

' VB6 - Let/Set keywords
Let x = 5
Set obj = New MyClass

' VB.NET - Assignment without keywords
Dim x As Integer = 5
Dim obj As New MyClass()
```

## COM Interop from VB.NET

### Early Binding (Type Library Reference)

```vb
' Add COM reference in project
' Tools -> Add Reference -> COM -> Excel Object Library

Imports Excel = Microsoft.Office.Interop.Excel

Public Sub ExportToExcel(data As DataTable)
    Dim excelApp As Excel.Application = Nothing
    Dim workbook As Excel.Workbook = Nothing
    Dim worksheet As Excel.Worksheet = Nothing

    Try
        excelApp = New Excel.Application()
        workbook = excelApp.Workbooks.Add()
        worksheet = CType(workbook.Worksheets(1), Excel.Worksheet)

        ' Write headers
        For col = 0 To data.Columns.Count - 1
            worksheet.Cells(1, col + 1) = data.Columns(col).ColumnName
        Next

        ' Write data
        For row = 0 To data.Rows.Count - 1
            For col = 0 To data.Columns.Count - 1
                worksheet.Cells(row + 2, col + 1) = data.Rows(row)(col)
            Next
        Next

        excelApp.Visible = True

    Catch ex As Exception
        MessageBox.Show($"Excel export failed: {ex.Message}")
    Finally
        ' Release COM objects
        If worksheet IsNot Nothing Then
            System.Runtime.InteropServices.Marshal.ReleaseComObject(worksheet)
        End If
        If workbook IsNot Nothing Then
            System.Runtime.InteropServices.Marshal.ReleaseComObject(workbook)
        End If
        If excelApp IsNot Nothing Then
            System.Runtime.InteropServices.Marshal.ReleaseComObject(excelApp)
        End If
    End Try
End Sub
```

### Late Binding (No Type Library)

```vb
Imports System.Reflection

Public Sub CreateExcelLateBound()
    Dim excelType As Type = Type.GetTypeFromProgID("Excel.Application")
    If excelType Is Nothing Then
        MessageBox.Show("Excel not installed")
        Return
    End If

    Dim excelApp As Object = Nothing
    Try
        ' Create COM object
        excelApp = Activator.CreateInstance(excelType)

        ' Call methods via reflection
        excelType.InvokeMember("Visible",
            BindingFlags.SetProperty,
            Nothing,
            excelApp,
            New Object() {True})

        Dim workbooks As Object = excelType.InvokeMember("Workbooks",
            BindingFlags.GetProperty,
            Nothing,
            excelApp,
            Nothing)

        ' Add workbook
        workbooks.GetType().InvokeMember("Add",
            BindingFlags.InvokeMethod,
            Nothing,
            workbooks,
            Nothing)

    Finally
        If excelApp IsNot Nothing Then
            System.Runtime.InteropServices.Marshal.ReleaseComObject(excelApp)
        End If
    End Try
End Sub
```

### COM Object Release Pattern

```vb
' ✅ Good: Proper COM object cleanup
Public Sub UseComObject()
    Dim excelApp As Excel.Application = Nothing
    Dim workbook As Excel.Workbook = Nothing

    Try
        excelApp = New Excel.Application()
        workbook = excelApp.Workbooks.Add()
        ' Use objects
    Finally
        ' Release in reverse order of creation
        If workbook IsNot Nothing Then
            workbook.Close(False)
            Marshal.ReleaseComObject(workbook)
            workbook = Nothing
        End If

        If excelApp IsNot Nothing Then
            excelApp.Quit()
            Marshal.ReleaseComObject(excelApp)
            excelApp = Nothing
        End If

        GC.Collect()
        GC.WaitForPendingFinalizers()
    End Try
End Sub

' ❌ Bad: Not releasing COM objects (memory leak)
Dim excelApp = New Excel.Application()
excelApp.Workbooks.Add()
' No cleanup - Excel process remains in memory!
```

## Creating COM-Visible .NET Components

### COM-Visible Class

```vb
Imports System.Runtime.InteropServices

<ComVisible(True)>
<Guid("12345678-1234-1234-1234-123456789012")>
<ClassInterface(ClassInterfaceType.None)>
<ProgId("MyCompany.Calculator")>
Public Class Calculator
    Implements ICalculator

    Public Function Add(a As Integer, b As Integer) As Integer Implements ICalculator.Add
        Return a + b
    End Function

    Public Function Subtract(a As Integer, b As Integer) As Integer Implements ICalculator.Subtract
        Return a - b
    End Function
End Class

' Interface for COM
<ComVisible(True)>
<Guid("87654321-4321-4321-4321-210987654321")>
<InterfaceType(ComInterfaceType.InterfaceIsDual)>
Public Interface ICalculator
    Function Add(a As Integer, b As Integer) As Integer
    Function Subtract(a As Integer, b As Integer) As Integer
End Interface
```

### Register for COM

```bash
# Register assembly for COM
regasm MyAssembly.dll /tlb /codebase

# Unregister
regasm MyAssembly.dll /u

# Generate type library
tlbexp MyAssembly.dll
```

## Legacy VB6 Patterns to Modernize

### Error Handling

```vb
' VB6 style (avoid in new code)
Public Function GetCustomer(id As Integer) As Customer
    On Error GoTo ErrorHandler

    ' Code here
    Exit Function

ErrorHandler:
    MsgBox "Error: " & Err.Description
    Resume Next
End Function

' VB.NET modern style
Public Function GetCustomer(id As Integer) As Customer
    Try
        ' Code here
    Catch ex As ArgumentException
        MessageBox.Show($"Invalid argument: {ex.Message}")
        Return Nothing
    Catch ex As Exception
        MessageBox.Show($"Error: {ex.Message}")
        Throw
    End Try
End Function
```

### File I/O

```vb
' VB6 style (avoid)
Dim fileNum As Integer = FreeFile()
FileOpen(fileNum, "data.txt", OpenMode.Output)
PrintLine(fileNum, "Hello World")
FileClose(fileNum)

' VB.NET modern style
Using writer = New StreamWriter("data.txt")
    writer.WriteLine("Hello World")
End Using

' Or async
Await File.WriteAllTextAsync("data.txt", "Hello World")
```

### Collections

```vb
' VB6 Collection (avoid in new code)
Dim customers As New Collection()
customers.Add(customer, "key1")
Dim item = customers("key1")

' VB.NET generic collections
Dim customers = New Dictionary(Of String, Customer)()
customers.Add("key1", customer)
Dim item = customers("key1")

' Or List(Of T)
Dim customerList = New List(Of Customer)()
customerList.Add(customer)
```

## Migration Strategy

### Incremental Migration

```vb
' 1. Start with COM interop wrapper
' Wrap VB6 COM component in VB.NET

Public Class VB6Wrapper
    Private vb6Component As Object

    Public Sub New()
        vb6Component = CreateObject("VB6Project.Component")
    End Sub

    Public Function ProcessData(data As String) As String
        Return vb6Component.ProcessData(data).ToString()
    End Function
End Class

' 2. Gradually replace with native VB.NET
Public Class ModernComponent
    Public Function ProcessData(data As String) As String
        ' New VB.NET implementation
        Return data.ToUpper()
    End Function
End Class
```

## Best Practices

### ✅ DO

```vb
' Use modern VB.NET features in new code
Option Strict On
Option Explicit On

' Release COM objects explicitly
Marshal.ReleaseComObject(comObject)
GC.Collect()

' Use Try-Catch instead of On Error
Try
    ' Code
Catch ex As Exception
    ' Handle
End Try

' Use generics instead of Collections
Dim items = New List(Of Customer)()

' Use async for I/O
Await File.WriteAllTextAsync("file.txt", content)
```

### ❌ DON'T

```vb
' Don't use VB6 compatibility module
Imports Microsoft.VisualBasic.Compatibility.VB6  ' Legacy only!

' Don't use Option Strict Off
Option Strict Off  ' Avoid!

' Don't use On Error in new code
On Error Resume Next  ' VB6 style

' Don't forget to release COM objects
Dim excelApp = New Excel.Application()
' ... (no cleanup - memory leak!)

' Don't use late binding when early binding available
Dim obj = CreateObject("Excel.Application")  ' Use typed reference instead
```

## Related Skills

- **vb-core**: Modern VB.NET patterns
- **vb-winforms**: Windows Forms migration
- **vb-database**: Database migration strategies
