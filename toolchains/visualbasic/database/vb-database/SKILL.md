---
name: vb-database
description: ADO.NET patterns, Entity Framework, database best practices
user-invocable: false
disable-model-invocation: true
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
tags: [visualbasic, adonet, database, entity-framework, sql]
---

# Visual Basic Database Patterns

ADO.NET and Entity Framework patterns for VB.NET with focus on connection management, parameterized queries, and async operations.

## ADO.NET Patterns

### Connection Management

```vb
' ✅ Good: Using statement ensures disposal
Public Async Function GetCustomersAsync() As Task(Of List(Of Customer))
    Dim customers = New List(Of Customer)()

    Using connection = New SqlConnection(connectionString)
        Await connection.OpenAsync()

        Using command = New SqlCommand("SELECT * FROM Customers WHERE IsActive = @isActive", connection)
            command.Parameters.AddWithValue("@isActive", True)

            Using reader = Await command.ExecuteReaderAsync()
                While Await reader.ReadAsync()
                    customers.Add(New Customer With {
                        .Id = reader.GetInt32(0),
                        .Name = reader.GetString(1),
                        .Email = reader.GetString(2)
                    })
                End While
            End Using
        End Using
    End Using

    Return customers
End Function
```

### Parameterized Queries (Critical for SQL Injection Prevention)

```vb
' ✅ Good: Parameterized query
Public Async Function FindCustomerAsync(email As String) As Task(Of Customer)
    Using connection = New SqlConnection(connectionString)
        Await connection.OpenAsync()

        Dim sql = "SELECT * FROM Customers WHERE Email = @email"
        Using command = New SqlCommand(sql, connection)
            command.Parameters.Add("@email", SqlDbType.NVarChar, 255).Value = email

            Using reader = Await command.ExecuteReaderAsync()
                If Await reader.ReadAsync() Then
                    Return MapCustomer(reader)
                End If
            End Using
        End Using
    End Using

    Return Nothing
End Function

' ❌ BAD: String concatenation (SQL injection risk!)
Dim sql = $"SELECT * FROM Customers WHERE Email = '{email}'"  ' NEVER DO THIS!
```

### Transaction Management

```vb
Public Async Function TransferFundsAsync(fromAccountId As Integer, toAccountId As Integer, amount As Decimal) As Task
    Using connection = New SqlConnection(connectionString)
        Await connection.OpenAsync()

        Using transaction = connection.BeginTransaction()
            Try
                ' Debit from account
                Using command = New SqlCommand("UPDATE Accounts SET Balance = Balance - @amount WHERE Id = @id", connection, transaction)
                    command.Parameters.AddWithValue("@amount", amount)
                    command.Parameters.AddWithValue("@id", fromAccountId)
                    Await command.ExecuteNonQueryAsync()
                End Using

                ' Credit to account
                Using command = New SqlCommand("UPDATE Accounts SET Balance = Balance + @amount WHERE Id = @id", connection, transaction)
                    command.Parameters.AddWithValue("@amount", amount)
                    command.Parameters.AddWithValue("@id", toAccountId)
                    Await command.ExecuteNonQueryAsync()
                End Using

                transaction.Commit()
            Catch ex As Exception
                transaction.Rollback()
                Throw
            End Try
        End Using
    End Using
End Function
```

### Bulk Operations

```vb
Public Async Function BulkInsertCustomersAsync(customers As List(Of Customer)) As Task
    Using connection = New SqlConnection(connectionString)
        Await connection.OpenAsync()

        ' Create DataTable
        Dim table = New DataTable()
        table.Columns.Add("Name", GetType(String))
        table.Columns.Add("Email", GetType(String))
        table.Columns.Add("CreatedAt", GetType(DateTime))

        For Each customer In customers
            table.Rows.Add(customer.Name, customer.Email, DateTime.Now)
        Next

        ' Bulk copy
        Using bulkCopy = New SqlBulkCopy(connection)
            bulkCopy.DestinationTableName = "Customers"
            bulkCopy.BatchSize = 1000
            Await bulkCopy.WriteToServerAsync(table)
        End Using
    End Using
End Function
```

## Entity Framework Core Patterns

### DbContext Setup

```vb
Public Class AppDbContext
    Inherits DbContext

    Public Property Customers As DbSet(Of Customer)
    Public Property Orders As DbSet(Of Order)

    Public Sub New(options As DbContextOptions(Of AppDbContext))
        MyBase.New(options)
    End Sub

    Protected Overrides Sub OnModelCreating(builder As ModelBuilder)
        ' Configure entity
        builder.Entity(Of Customer)(Sub(entity)
            entity.HasKey(Function(c) c.Id)
            entity.Property(Function(c) c.Name).IsRequired().HasMaxLength(200)
            entity.Property(Function(c) c.Email).IsRequired().HasMaxLength(255)
            entity.HasIndex(Function(c) c.Email).IsUnique()
        End Sub)

        ' Configure relationship
        builder.Entity(Of Order)(Sub(entity)
            entity.HasOne(Function(o) o.Customer) _
                  .WithMany(Function(c) c.Orders) _
                  .HasForeignKey(Function(o) o.CustomerId)
        End Sub)
    End Sub
End Class
```

### CRUD Operations

```vb
Public Class CustomerRepository
    Private ReadOnly context As AppDbContext

    Public Sub New(context As AppDbContext)
        Me.context = context
    End Sub

    ' Create
    Public Async Function AddAsync(customer As Customer) As Task(Of Customer)
        context.Customers.Add(customer)
        Await context.SaveChangesAsync()
        Return customer
    End Function

    ' Read
    Public Async Function GetByIdAsync(id As Integer) As Task(Of Customer)
        Return Await context.Customers _
            .Include(Function(c) c.Orders) _
            .FirstOrDefaultAsync(Function(c) c.Id = id)
    End Function

    ' Update
    Public Async Function UpdateAsync(customer As Customer) As Task
        context.Customers.Update(customer)
        Await context.SaveChangesAsync()
    End Function

    ' Delete
    Public Async Function DeleteAsync(id As Integer) As Task
        Dim customer = Await context.Customers.FindAsync(id)
        If customer IsNot Nothing Then
            context.Customers.Remove(customer)
            Await context.SaveChangesAsync()
        End If
    End Function

    ' Query with filtering
    Public Async Function GetActiveCustomersAsync() As Task(Of List(Of Customer))
        Return Await context.Customers _
            .Where(Function(c) c.IsActive) _
            .OrderBy(Function(c) c.Name) _
            .ToListAsync()
    End Function
End Class
```

### Async Queries

```vb
' Single result
Dim customer = Await context.Customers _
    .FirstOrDefaultAsync(Function(c) c.Email = email)

' List results
Dim customers = Await context.Customers _
    .Where(Function(c) c.IsActive) _
    .ToListAsync()

' Count
Dim count = Await context.Customers.CountAsync()

' Any
Dim exists = Await context.Customers _
    .AnyAsync(Function(c) c.Email = email)

' Aggregate
Dim totalOrders = Await context.Orders.SumAsync(Function(o) o.Amount)
```

### Change Tracking

```vb
' Detach entity
context.Entry(customer).State = EntityState.Detached

' Track changes
Dim customer = Await context.Customers.FindAsync(id)
customer.Name = "Updated Name"

' See what changed
Dim entry = context.Entry(customer)
For Each prop In entry.Properties
    If prop.IsModified Then
        Console.WriteLine($"{prop.Metadata.Name}: {prop.OriginalValue} -> {prop.CurrentValue}")
    End If
Next

Await context.SaveChangesAsync()
```

## Database Migrations

### Code-First Migrations

```bash
# Add migration
dotnet ef migrations add InitialCreate

# Update database
dotnet ef database update

# Rollback
dotnet ef database update PreviousMigration

# Generate SQL script
dotnet ef migrations script
```

### Migration Class

```vb
Public Class CreateCustomersTable
    Inherits Migration

    Protected Overrides Sub Up(migrationBuilder As MigrationBuilder)
        migrationBuilder.CreateTable(
            name:="Customers",
            columns:=Function(table) New With {
                .Id = table.Column(Of Integer)(nullable:=False).Annotation("SqlServer:Identity", "1, 1"),
                .Name = table.Column(Of String)(maxLength:=200, nullable:=False),
                .Email = table.Column(Of String)(maxLength:=255, nullable:=False),
                .CreatedAt = table.Column(Of DateTime)(nullable:=False)
            },
            constraints:=Sub(table)
                table.PrimaryKey("PK_Customers", Function(x) x.Id)
                table.UniqueConstraint("UK_Customers_Email", Function(x) x.Email)
            End Sub
        )

        migrationBuilder.CreateIndex(
            name:="IX_Customers_Email",
            table:="Customers",
            column:="Email",
            unique:=True
        )
    End Sub

    Protected Overrides Sub Down(migrationBuilder As MigrationBuilder)
        migrationBuilder.DropTable(name:="Customers")
    End Sub
End Class
```

## Connection String Management

```vb
' appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyApp;Trusted_Connection=True;"
  }
}

' Startup configuration
Public Class Startup
    Public Sub ConfigureServices(services As IServiceCollection)
        services.AddDbContext(Of AppDbContext)(Sub(options)
            options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection"))
        End Sub)
    End Sub
End Class
```

## Best Practices

### ✅ DO

```vb
' Use async methods
Dim customers = Await context.Customers.ToListAsync()

' Use parameterized queries
command.Parameters.AddWithValue("@email", email)

' Dispose connections
Using connection = New SqlConnection(connectionString)
End Using

' Use transactions for multiple operations
Using transaction = connection.BeginTransaction()

' Use IQueryable for deferred execution
Dim query As IQueryable(Of Customer) = context.Customers.Where(Function(c) c.IsActive)
```

### ❌ DON'T

```vb
' Don't concatenate SQL (SQL injection!)
Dim sql = $"SELECT * FROM Users WHERE Email = '{email}'"

' Don't forget to dispose
Dim connection = New SqlConnection(connectionString)  ' No Using - leak!

' Don't block on async
Dim result = GetDataAsync().Result  ' Deadlock risk

' Don't load entire table when filtering
Dim customers = context.Customers.ToList().Where(Function(c) c.IsActive)  ' Loads all first!
' Better: context.Customers.Where(Function(c) c.IsActive).ToList()
```

## Related Skills

- **vb-core**: Core VB.NET patterns
- **vb-winforms**: Windows Forms with database binding
- **test-driven-development**: Testing database operations
