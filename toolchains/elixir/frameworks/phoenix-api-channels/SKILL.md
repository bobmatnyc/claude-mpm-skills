---
name: phoenix-api-channels
description: Phoenix controllers, JSON APIs, Channels, and Presence on the BEAM. Covers routing, plugs, versioned APIs, Ecto-backed contexts, PubSub broadcasting, Presence tracking, authentication, testing, telemetry, and deployment considerations.
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Phoenix REST/JSON + Channels/Presence on the BEAM with contexts, plugs, auth, and PubSub."
    when_to_use:
      - "Building JSON APIs with Phoenix controllers and versioned routes"
      - "Adding WebSocket/Channels for chat, notifications, or collaborative features"
      - "Needing Presence tracking, fan-out broadcasts, and PubSub-backed updates"
      - "Integrating Ecto contexts for persistence and domain boundaries"
    quick_start:
      - "mix phx.new my_api --no-html --no-live && cd my_api"
      - "mix deps.get && mix ecto.create"
      - "Define contexts + schemas; add routes/controllers; wire `socket` + Channel modules"
      - "Start server: mix phx.server (REST + WebSocket on http://localhost:4000)"
  token_estimate:
    entry: 170
    full: 5200
---

# Phoenix APIs, Channels, and Presence (Elixir/BEAM)

Phoenix excels at REST/JSON APIs and WebSocket Channels with minimal boilerplate, leveraging the BEAM for fault tolerance, lightweight processes, and supervised PubSub/Presence.

**Core pillars**
- Controllers for JSON APIs with plugs, pipelines, and versioning.
- Contexts own data (Ecto schemas + queries) and expose a narrow API to controllers/channels.
- Channels + PubSub for fan-out real-time updates; Presence for tracking users/devices.
- Auth via plugs (session/cookie for browser, token/Bearer for APIs), with signed params.

---

## Project Setup

```bash
mix phx.new my_api --no-html --no-live
cd my_api
mix deps.get
mix ecto.create
mix phx.server
```

Key files:
- `lib/my_api_web/endpoint.ex` — plugs, sockets, instrumentation
- `lib/my_api_web/router.ex` — pipelines, scopes, versioning, sockets
- `lib/my_api_web/controllers/*` — REST/JSON controllers
- `lib/my_api/*` — contexts + Ecto schemas (ownership of data logic)
- `lib/my_api_web/channels/*` — Channel modules

---

## Routing and Pipelines

Separate browser vs API pipelines; version APIs with scopes.
```elixir
defmodule MyApiWeb.Router do
  use MyApiWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
    plug :fetch_session
    plug :protect_from_forgery
    plug MyApiWeb.Plugs.RequireAuth
  end

  scope "/api", MyApiWeb do
    pipe_through :api

    scope "/v1", V1, as: :v1 do
      resources "/users", UserController, except: [:new, :edit]
      post "/sessions", SessionController, :create
    end
  end

  socket "/socket", MyApiWeb.UserSocket,
    websocket: [connect_info: [:peer_data, :x_headers]],
    longpoll: false
end
```

**Tips**
- Keep pipelines short; push auth/guards into plugs.
- Expose `socket "/socket"` for Channels; restrict transports as needed.

---

## Controllers and Plugs

Controllers stay thin; contexts own the logic.
```elixir
defmodule MyApiWeb.V1.UserController do
  use MyApiWeb, :controller
  alias MyApi.Accounts

  action_fallback MyApiWeb.FallbackController

  def index(conn, _params) do
    users = Accounts.list_users()
    render(conn, :index, users: users)
  end

  def create(conn, params) do
    with {:ok, user} <- Accounts.register_user(params) do
      conn
      |> put_status(:created)
      |> put_resp_header("location", ~p\"/api/v1/users/#{user.id}\")
      |> render(:show, user: user)
    end
  end
end
```

**FallbackController** centralizes error translation (`{:error, :not_found}` → 404 JSON).

**Plugs**
- `RequireAuth` verifies bearer/session tokens, sets `current_user`.
- Use `plug :scrub_params`-style transforms in pipelines, not controllers.
- Avoid heavy work in plugs; they run per-request.

---

## Contexts and Data (Ecto)

Contexts expose only what controllers/channels need.
```elixir
defmodule MyApi.Accounts do
  import Ecto.Query, warn: false
  alias MyApi.{Repo, Accounts.User}

  def list_users, do: Repo.all(User)
  def get_user!(id), do: Repo.get!(User, id)

  def register_user(attrs) do
    %User{}
    |> User.registration_changeset(attrs)
    |> Repo.insert()
  end
end
```

**Guidelines**
- Keep schema modules free of controller knowledge.
- Validate at the changeset; use `Ecto.Multi` for multi-step operations.
- Prefer pagination helpers (`Scrivener`, `Flop`) for large lists.

---

## Channels, PubSub, and Presence

Channel module example:
```elixir
defmodule MyApiWeb.RoomChannel do
  use Phoenix.Channel
  alias Phoenix.Presence

  def join("room:" <> room_id, _payload, socket) do
    send(self(), :after_join)
    {:ok, assign(socket, :room_id, room_id)}
  end

  def handle_info(:after_join, socket) do
    Presence.track(socket, socket.assigns.user_id, %{online_at: System.system_time(:second)})
    push(socket, "presence_state", Presence.list(socket))
    {:noreply, socket}
  end

  def handle_in("message:new", %{"body" => body}, socket) do
    broadcast!(socket, "message:new", %{user_id: socket.assigns.user_id, body: body})
    {:noreply, socket}
  end
end
```

**PubSub from contexts**
```elixir
def create_order(attrs) do
  with {:ok, order} <- %Order{} |> Order.changeset(attrs) |> Repo.insert() do
    Phoenix.PubSub.broadcast(MyApi.PubSub, "orders", {:order_created, order})
    {:ok, order}
  end
end
```

**Best practices**
- Authorize in `UserSocket.connect/3` before joining topics.
- Limit payload sizes; validate incoming events.
- Use topic partitioning for tenancy (`"tenant:" <> tenant_id <> ":room:" <> room_id`).

---

## Authentication Patterns

- **API tokens**: Accept `authorization: Bearer <token>`; verify in plug, assign `current_user`.
- **Signed params**: `Phoenix.Token.sign/verify` for short-lived join params.
- **Rate limiting**: Use plugs + ETS/Cachex or reverse proxy (NGINX/Cloudflare).
- **CORS**: Configure in `Endpoint` with `cors_plug`.

---

## Testing

Use generated helpers:
```elixir
defmodule MyApiWeb.UserControllerTest do
  use MyApiWeb.ConnCase, async: true

  test "lists users", %{conn: conn} do
    conn = get(conn, ~p\"/api/v1/users\")
    assert json_response(conn, 200)["data"] == []
  end
end
```

Channel tests:
```elixir
defmodule MyApiWeb.RoomChannelTest do
  use MyApiWeb.ChannelCase, async: true

  test "broadcasts messages" do
    {:ok, _, socket} = connect(MyApiWeb.UserSocket, %{"token" => "abc"})
    {:ok, _, socket} = subscribe_and_join(socket, "room:123", %{})
    ref = push(socket, "message:new", %{"body" => "hi"})
    assert_reply ref, :ok
    assert_broadcast "message:new", %{body: "hi"}
  end
end
```

**DataCase**: isolates DB per test; use fixtures/factories for setup.

---

## Telemetry, Observability, and Ops

- `:telemetry` events from endpoint, controller, channel, and Ecto queries; export via `OpentelemetryPhoenix` and `OpentelemetryEcto`.
- Use `Plug.Telemetry` for request metrics; add logging metadata (request_id, user_id).
- Releases: `MIX_ENV=prod mix release`; configure runtime in `config/runtime.exs`.
- Clustering: `libcluster` + distributed PubSub for multi-node Presence.
- Assetless APIs: disable unused watchers (esbuild/tailwind) for API-only apps.

---

## Common Pitfalls

- Controllers doing queries directly instead of delegating to contexts.
- Not authorizing in `UserSocket.connect/3`, leading to topic exposure.
- Missing `action_fallback` → inconsistent error shapes.
- Forgetting to limit event payloads; large messages can overwhelm channels.
- Leaving longpoll enabled when unused; disable to reduce surface area.

Phoenix API + Channels shine when contexts own data, controllers stay thin, and Channels use PubSub/Presence with strict authorization and telemetry. The BEAM handles concurrency and fault tolerance so you can focus on clear boundaries and real-time experiences.
