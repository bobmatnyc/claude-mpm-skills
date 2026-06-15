# Go Idiomatic Quality Rules

Small, high-frequency Go idioms that keep handler and service code readable and
idiomatic. These are the kind of thing a reviewer flags repeatedly; encode them in
`gofmt`/`go vet`/`staticcheck`/`golangci-lint` so review effort goes to design instead.

> **Source note:** These idioms are derived from CAST Highlight's language-agnostic
> (`_multi`, Go-tagged) code-quality indicators (https://doc.casthighlight.com/), which
> reference the canonical Go style sources. Those sources — **Effective Go** and the
> **Go Code Review Comments** wiki — are authoritative; cite them, not CAST, for the
> underlying rules. Examples are original.

---

## 1. Use short variable declarations (`:=`) for locals with an initial value

**Why:** For a local variable that is set to a value immediately, `:=` is the idiomatic,
least-noisy form. `var x = v` for a local reads as ceremony. Reserve `var` for
zero-value declarations (`var buf bytes.Buffer`) and package-level variables (where `:=`
is not allowed).

**Non-idiomatic:**
```go
func handler(w http.ResponseWriter, r *http.Request) {
    var name = r.URL.Query().Get("name")   // use :=
    var count = 0                           // zero value: just `var count int`
    _ = name
    _ = count
}
```

**Idiomatic:**
```go
func handler(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")   // explicit value -> :=
    var count int                       // zero value -> var, no redundant `= 0`
    _ = name
    _ = count
}
```

**How to test:** Lint-enforced, not unit-tested. `gofmt -s` and `golangci-lint`
(`gosimple` S1021/related) catch the redundant forms; gate them in CI.

---

## 2. Don't name an unused method receiver

**Why:** If a method never uses its receiver, leaving it unnamed (`func (*Server) Foo()`)
makes it immediately clear the receiver is irrelevant. A named-but-unused receiver invites
the reader to look for a use that isn't there.

**Non-idiomatic:**
```go
func (s *Server) DefaultPort() int {   // s is never used
    return 8080
}
```

**Idiomatic:**
```go
func (*Server) DefaultPort() int {     // receiver unnamed: clearly unused
    return 8080
}
```

**How to test:** Lint concern (`revive`/`staticcheck` unused-receiver style). Keep it in
CI rather than unit tests.

---

## 3. Initialize struct pointers with `&T{}`, not `new(T)`

**Why:** `&T{...}` is consistent with composite-literal struct initialization, lets you
set fields inline, and reads the same whether or not fields are provided. `new(T)` returns
a zeroed `*T` you must then mutate field-by-field, and mixing both styles in a codebase is
needless inconsistency.

**Non-idiomatic:**
```go
srv := new(Server)
srv.Addr = ":8080"
srv.Handler = mux
```

**Idiomatic:**
```go
srv := &Server{
    Addr:    ":8080",
    Handler: mux,
}
```

**How to test:** Behavior is identical, so this is a readability/lint rule
(`staticcheck` flags `new(T)` where a literal is clearer). Gate via `golangci-lint`.

---

## 4. Handle (don't discard) returned errors

**Why:** Although not in the original four CAST idioms, the most consequential Go quality
signal in handler code is a silently dropped `error`. An ignored error from
`w.Write`, `json.NewDecoder(...).Decode`, or a repository call turns a failure into a
silent 200. Check every returned error or explicitly document why it's ignored.

**Non-idiomatic:**
```go
func create(w http.ResponseWriter, r *http.Request) {
    var in CreateReq
    json.NewDecoder(r.Body).Decode(&in)   // error dropped: malformed body -> garbage
    repo.Save(in)                          // error dropped: failure looks like success
    w.WriteHeader(http.StatusCreated)
}
```

**Idiomatic:**
```go
func create(w http.ResponseWriter, r *http.Request) {
    var in CreateReq
    if err := json.NewDecoder(r.Body).Decode(&in); err != nil {
        http.Error(w, "invalid body", http.StatusBadRequest)
        return
    }
    if err := repo.Save(r.Context(), in); err != nil {
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    w.WriteHeader(http.StatusCreated)
}
```

**How to test:** `errcheck` (via `golangci-lint`) flags unchecked errors statically. Add a
handler test asserting that a malformed body yields 400 and a repo failure yields 500 —
proving the errors are actually handled, not dropped.

---

## Where this fits

These are review/lint checks complementary to the framework patterns in the main skill.
Most are enforced by `gofmt -s`, `go vet`, `staticcheck`, `errcheck`, and `revive` under
`golangci-lint` — wire them into CI. For concurrency-specific quality (race-free
goroutines, context cancellation), see the `golang-concurrency-patterns` skill.
