---
name: vb-winforms
description: Windows Forms development patterns, UI threading, data binding
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
tags: [visualbasic, winforms, ui, desktop, data-binding]
---

# Visual Basic Windows Forms Patterns

Modern Windows Forms development with VB.NET focusing on proper UI threading, data binding, and event handling.

## Quick Start

```vb
' Form definition
Public Class CustomerForm
    Inherits Form

    Private customerService As ICustomerService
    Private bindingSource As New BindingSource()

    Public Sub New()
        InitializeComponent()
        customerService = New CustomerService()
    End Sub

    ' Async load
    Private Async Sub CustomerForm_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Await LoadCustomersAsync()
    End Sub

    Private Async Function LoadCustomersAsync() As Task
        Try
            Cursor = Cursors.WaitCursor
            Dim customers = Await customerService.GetAllAsync()
            bindingSource.DataSource = customers
            dataGridView.DataSource = bindingSource
        Catch ex As Exception
            MessageBox.Show($"Error loading customers: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
        Finally
            Cursor = Cursors.Default
        End Try
    End Function
End Class
```

## UI Threading Patterns

### Invoke vs BeginInvoke

```vb
' Update UI from background thread
Private Sub BackgroundWorker_ProgressChanged(sender As Object, e As ProgressChangedEventArgs)
    ' Already on UI thread with BackgroundWorker
    progressBar.Value = e.ProgressPercentage
    lblStatus.Text = $"Processing: {e.ProgressPercentage}%"
End Sub

' Manual invoke when needed
Private Sub UpdateUIFromThread(text As String)
    If lblStatus.InvokeRequired Then
        lblStatus.Invoke(Sub() lblStatus.Text = text)
    Else
        lblStatus.Text = text
    End If
End Sub

' Async pattern
Private Async Sub btnProcess_Click(sender As Object, e As EventArgs) Handles btnProcess.Click
    btnProcess.Enabled = False
    Try
        Dim result = Await Task.Run(Function() LongRunningOperation())
        lblResult.Text = result  ' Safe - back on UI thread
    Finally
        btnProcess.Enabled = True
    End Try
End Sub
```

### BackgroundWorker Pattern

```vb
Private WithEvents bgWorker As New BackgroundWorker With {
    .WorkerReportsProgress = True,
    .WorkerSupportsCancellation = True
}

Private Sub btnStart_Click(sender As Object, e As EventArgs) Handles btnStart.Click
    If Not bgWorker.IsBusy Then
        bgWorker.RunWorkerAsync()
    End If
End Sub

Private Sub bgWorker_DoWork(sender As Object, e As DoWorkEventArgs) Handles bgWorker.DoWork
    For i = 0 To 100
        If bgWorker.CancellationPending Then
            e.Cancel = True
            Exit For
        End If

        ' Simulate work
        Threading.Thread.Sleep(50)
        bgWorker.ReportProgress(i)
    Next
End Sub

Private Sub bgWorker_ProgressChanged(sender As Object, e As ProgressChangedEventArgs) Handles bgWorker.ProgressChanged
    progressBar.Value = e.ProgressPercentage
End Sub

Private Sub bgWorker_RunWorkerCompleted(sender As Object, e As RunWorkerCompletedEventArgs) Handles bgWorker.RunWorkerCompleted
    If e.Cancelled Then
        MessageBox.Show("Operation cancelled")
    ElseIf e.Error IsNot Nothing Then
        MessageBox.Show($"Error: {e.Error.Message}")
    Else
        MessageBox.Show("Operation completed")
    End If
End Sub
```

## Data Binding

### BindingSource Pattern

```vb
Public Class CustomerForm
    Private bindingSource As New BindingSource()
    Private customers As List(Of Customer)

    Private Async Sub Form_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        customers = Await customerService.GetAllAsync()

        ' Setup binding source
        bindingSource.DataSource = customers

        ' Bind controls
        dataGridView.DataSource = bindingSource
        txtName.DataBindings.Add("Text", bindingSource, "Name")
        txtEmail.DataBindings.Add("Text", bindingSource, "Email")

        ' Navigation
        bindingNavigator.BindingSource = bindingSource
    End Sub

    ' Filter
    Private Sub txtSearch_TextChanged(sender As Object, e As EventArgs) Handles txtSearch.TextChanged
        If String.IsNullOrEmpty(txtSearch.Text) Then
            bindingSource.RemoveFilter()
        Else
            bindingSource.Filter = $"Name LIKE '%{txtSearch.Text}%'"
        End If
    End Sub
End Class
```

### Object Data Binding

```vb
' Customer class with INotifyPropertyChanged
Public Class Customer
    Implements INotifyPropertyChanged

    Private _name As String
    Public Property Name As String
        Get
            Return _name
        End Get
        Set(value As String)
            If _name <> value Then
                _name = value
                OnPropertyChanged(NameOf(Name))
            End If
        End Set
    End Property

    Public Event PropertyChanged As PropertyChangedEventHandler _
        Implements INotifyPropertyChanged.PropertyChanged

    Protected Sub OnPropertyChanged(propertyName As String)
        RaiseEvent PropertyChanged(Me, New PropertyChangedEventArgs(propertyName))
    End Sub
End Class
```

## Event Handling

### Standard Event Pattern

```vb
' Button click
Private Sub btnSave_Click(sender As Object, e As EventArgs) Handles btnSave.Click
    If ValidateForm() Then
        SaveCustomer()
    End If
End Sub

' Multiple controls, same handler
Private Sub TextBox_TextChanged(sender As Object, e As EventArgs) _
    Handles txtName.TextChanged, txtEmail.TextChanged

    ValidateForm()
End Sub

' Custom event arguments
Public Class CustomerEventArgs
    Inherits EventArgs

    Public Property Customer As Customer

    Public Sub New(customer As Customer)
        Me.Customer = customer
    End Sub
End Class

Public Event CustomerSaved As EventHandler(Of CustomerEventArgs)

Protected Sub OnCustomerSaved(customer As Customer)
    RaiseEvent CustomerSaved(Me, New CustomerEventArgs(customer))
End Sub
```

## Form Validation

```vb
Private Function ValidateForm() As Boolean
    errorProvider.Clear()
    Dim isValid = True

    ' Validate name
    If String.IsNullOrWhiteSpace(txtName.Text) Then
        errorProvider.SetError(txtName, "Name is required")
        isValid = False
    End If

    ' Validate email
    If String.IsNullOrWhiteSpace(txtEmail.Text) OrElse Not txtEmail.Text.Contains("@") Then
        errorProvider.SetError(txtEmail, "Valid email is required")
        isValid = False
    End If

    ' Enable/disable save button
    btnSave.Enabled = isValid

    Return isValid
End Function

' Real-time validation
Private Sub txtEmail_Validating(sender As Object, e As System.ComponentModel.CancelEventArgs) _
    Handles txtEmail.Validating

    If Not txtEmail.Text.Contains("@") Then
        errorProvider.SetError(txtEmail, "Invalid email format")
        e.Cancel = True
    Else
        errorProvider.SetError(txtEmail, "")
    End If
End Sub
```

## Dialog Patterns

### Custom Dialog Result

```vb
Public Class CustomerDialog
    Inherits Form

    Public Property Customer As Customer

    Private Sub btnOK_Click(sender As Object, e As EventArgs) Handles btnOK.Click
        If ValidateForm() Then
            Customer = New Customer With {
                .Name = txtName.Text,
                .Email = txtEmail.Text
            }
            DialogResult = DialogResult.OK
            Close()
        End If
    End Sub

    Private Sub btnCancel_Click(sender As Object, e As EventArgs) Handles btnCancel.Click
        DialogResult = DialogResult.Cancel
        Close()
    End Sub
End Class

' Usage
Private Sub ShowCustomerDialog()
    Using dialog = New CustomerDialog()
        If dialog.ShowDialog() = DialogResult.OK Then
            ' Use dialog.Customer
            customers.Add(dialog.Customer)
            RefreshGrid()
        End If
    End Using
End Sub
```

## Best Practices

### ✅ DO

```vb
' Use async for I/O operations
Private Async Sub btnLoad_Click(sender As Object, e As EventArgs) Handles btnLoad.Click
    Dim data = Await LoadDataAsync()
End Sub

' Dispose resources properly
Private Sub Form_FormClosing(sender As Object, e As FormClosingEventArgs) Handles MyBase.FormClosing
    connection?.Dispose()
    timer?.Dispose()
End Sub

' Use BindingSource for data binding
bindingSource.DataSource = customers
dataGridView.DataSource = bindingSource

' Validate on events
Private Sub txtName_Validating(sender As Object, e As CancelEventArgs) Handles txtName.Validating

' Use ErrorProvider for validation feedback
errorProvider.SetError(txtName, "Name is required")
```

### ❌ DON'T

```vb
' Don't block UI thread
Private Sub btnLoad_Click(sender As Object, e As EventArgs) Handles btnLoad.Click
    Dim data = LoadDataAsync().Result  ' Blocks UI!
End Sub

' Don't update UI from background thread directly
Task.Run(Sub()
    lblStatus.Text = "Done"  ' WRONG - cross-thread operation
End Sub)

' Don't forget to dispose forms
Dim form = New CustomerForm()
form.Show()  ' Memory leak - use Using or handle FormClosed

' Don't use Application.DoEvents
While processing
    Application.DoEvents()  ' Bad practice - use async instead
End While
```

## Related Skills

- **vb-core**: Core VB.NET patterns and type safety
- **vb-database**: Database integration with Windows Forms
- **test-driven-development**: Testing Windows Forms applications
