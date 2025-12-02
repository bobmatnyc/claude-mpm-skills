---
name: graphql
description: GraphQL query language and runtime for APIs enabling clients to request exactly the data they need with strongly-typed schemas and single endpoint architecture.
progressive_disclosure:
  entry_point:
    - summary
    - when_to_use
    - quick_start
  full_content:
    - core_concepts
    - schema_definition
    - type_system
    - queries_mutations
    - resolvers_dataloaders
    - subscriptions
    - error_handling
    - schema_patterns
    - server_implementations
    - client_integrations
    - typescript_codegen
    - authentication
    - performance
    - file_uploads
    - testing
    - production_patterns
    - framework_integration
    - comparison
    - migration
    - best_practices
tokens:
  entry: 70
  full: 5500
---

# GraphQL Skill

## Summary
GraphQL is a query language and runtime for APIs that enables clients to request exactly the data they need. It provides a strongly-typed schema, single endpoint architecture, and eliminates over-fetching/under-fetching problems common in REST APIs.

## When to Use
- Building flexible APIs for multiple client types (web, mobile, IoT)
- Complex data requirements with nested relationships
- Mobile-first applications needing bandwidth efficiency
- Reducing API versioning complexity
- Real-time data with subscriptions
- Microservices aggregation and federation
- Developer experience with strong typing and introspection

## Quick Start

### 1. Define Schema (SDL)
```graphql
# schema.graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  publishedAt: DateTime
}

type Query {
  user(id: ID!): User
  users: [User!]!
  post(id: ID!): Post
}

type Mutation {
  createPost(title: String!, content: String!, authorId: ID!): Post!
  updatePost(id: ID!, title: String, content: String): Post!
  deletePost(id: ID!): Boolean!
}
```

### 2. Write Resolvers (TypeScript + Apollo Server)
```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { readFileSync } from 'fs';

// Load schema
const typeDefs = readFileSync('./schema.graphql', 'utf-8');

// Mock data
const users = [
  { id: '1', name: 'Alice', email: 'alice@example.com' },
  { id: '2', name: 'Bob', email: 'bob@example.com' },
];

const posts = [
  { id: '1', title: 'GraphQL Intro', content: 'Learning GraphQL...', authorId: '1' },
  { id: '2', title: 'Apollo Server', content: 'Building APIs...', authorId: '1' },
];

// Resolvers
const resolvers = {
  Query: {
    user: (_, { id }) => users.find(u => u.id === id),
    users: () => users,
    post: (_, { id }) => posts.find(p => p.id === id),
  },

  Mutation: {
    createPost: (_, { title, content, authorId }) => {
      const post = {
        id: String(posts.length + 1),
        title,
        content,
        authorId,
      };
      posts.push(post);
      return post;
    },

    updatePost: (_, { id, title, content }) => {
      const post = posts.find(p => p.id === id);
      if (!post) throw new Error('Post not found');
      if (title) post.title = title;
      if (content) post.content = content;
      return post;
    },

    deletePost: (_, { id }) => {
      const index = posts.findIndex(p => p.id === id);
      if (index === -1) return false;
      posts.splice(index, 1);
      return true;
    },
  },

  User: {
    posts: (user) => posts.filter(p => p.authorId === user.id),
  },

  Post: {
    author: (post) => users.find(u => u.id === post.authorId),
  },
};

// Create server
const server = new ApolloServer({ typeDefs, resolvers });

startStandaloneServer(server, {
  listen: { port: 4000 },
}).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
```

### 3. Query Data (Client)
```typescript
// Using Apollo Client
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:4000',
  cache: new InMemoryCache(),
});

// Query
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      posts {
        id
        title
        publishedAt
      }
    }
  }
`;

const { data } = await client.query({
  query: GET_USER,
  variables: { id: '1' },
});

// Mutation
const CREATE_POST = gql`
  mutation CreatePost($title: String!, $content: String!, $authorId: ID!) {
    createPost(title: $title, content: $content, authorId: $authorId) {
      id
      title
      content
    }
  }
`;

const { data: postData } = await client.mutate({
  mutation: CREATE_POST,
  variables: {
    title: 'New Post',
    content: 'Hello GraphQL!',
    authorId: '1',
  },
});
```

---

## Core Concepts

### GraphQL Fundamentals
- **Schema-First Design**: Define API contract with Schema Definition Language (SDL)
- **Type Safety**: Strongly-typed schema enforced at runtime and build-time
- **Single Endpoint**: All queries and mutations go through one URL (e.g., `/graphql`)
- **Client-Specified Queries**: Clients request exactly what they need
- **Hierarchical Data**: Queries mirror the shape of returned data
- **Introspection**: Schema is self-documenting and queryable

### Operations
```graphql
# Query - Read data (GET-like)
query GetUser {
  user(id: "1") {
    name
  }
}

# Mutation - Modify data (POST/PUT/DELETE-like)
mutation CreateUser {
  createUser(name: "Alice", email: "alice@example.com") {
    id
    name
  }
}

# Subscription - Real-time updates (WebSocket)
subscription OnPostCreated {
  postCreated {
    id
    title
    author {
      name
    }
  }
}
```

### Fields and Arguments
```graphql
type Query {
  # Field with arguments
  user(id: ID!): User
  users(limit: Int = 10, offset: Int = 0): [User!]!

  # Search with multiple arguments
  searchPosts(
    query: String!
    category: String
    limit: Int = 20
  ): [Post!]!
}
```

---

## Schema Definition Language (SDL)

### Basic Type Definition
```graphql
type User {
  id: ID!              # Non-null ID scalar
  name: String!        # Non-null String
  email: String!
  age: Int             # Nullable Int
  isActive: Boolean!
  posts: [Post!]!      # Non-null list of non-null Posts
  profile: Profile     # Nullable object type
}

type Profile {
  bio: String
  avatarUrl: String
  website: String
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  tags: [String!]      # Non-null list, nullable elements
  publishedAt: DateTime
}
```

### Input Types (for mutations)
```graphql
input CreateUserInput {
  name: String!
  email: String!
  age: Int
}

input UpdateUserInput {
  name: String
  email: String
  age: Int
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}
```

### Interfaces
```graphql
interface Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type User implements Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  name: String!
  email: String!
}

type Post implements Node {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  title: String!
  content: String!
}

type Query {
  node(id: ID!): Node  # Can return User or Post
}
```

### Unions
```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}

# Client query with fragments
query Search {
  search(query: "graphql") {
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
    ... on Comment {
      text
      author { name }
    }
  }
}
```

### Enums
```graphql
enum Role {
  ADMIN
  MODERATOR
  USER
  GUEST
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type User {
  id: ID!
  name: String!
  role: Role!
}

type Post {
  id: ID!
  title: String!
  status: PostStatus!
}
```

---

## Type System

### Scalar Types
```graphql
# Built-in scalars
scalar Int       # Signed 32-bit integer
scalar Float     # Signed double-precision floating-point
scalar String    # UTF-8 character sequence
scalar Boolean   # true or false
scalar ID        # Unique identifier (serialized as String)

# Custom scalars
scalar DateTime  # ISO 8601 timestamp
scalar Email     # Email address
scalar URL       # Valid URL
scalar JSON      # Arbitrary JSON
scalar Upload    # File upload
```

### Custom Scalar Implementation
```typescript
// DateTime scalar (TypeScript)
import { GraphQLScalarType, Kind } from 'graphql';

const DateTimeScalar = new GraphQLScalarType({
  name: 'DateTime',
  description: 'ISO 8601 DateTime',

  // Serialize to client (output)
  serialize(value: Date) {
    return value.toISOString();
  },

  // Parse from client (input)
  parseValue(value: string) {
    return new Date(value);
  },

  // Parse from query literal
  parseLiteral(ast) {
    if (ast.kind === Kind.STRING) {
      return new Date(ast.value);
    }
    return null;
  },
});

// Add to resolvers
const resolvers = {
  DateTime: DateTimeScalar,
  // ... other resolvers
};
```

### Non-Null and Lists
```graphql
type User {
  name: String!           # Non-null String
  email: String           # Nullable String

  tags: [String!]!        # Non-null list of non-null Strings
  friends: [User!]        # Nullable list of non-null Users
  posts: [Post]!          # Non-null list of nullable Posts
  comments: [Comment]     # Nullable list of nullable Comments
}
```

---

## Queries and Mutations

### Query Variables
```typescript
// Define query with variables
const GET_USER = gql`
  query GetUser($id: ID!, $includePosts: Boolean = false) {
    user(id: $id) {
      id
      name
      email
      posts @include(if: $includePosts) {
        id
        title
      }
    }
  }
`;

// Execute with variables
const { data } = await client.query({
  query: GET_USER,
  variables: {
    id: '1',
    includePosts: true,
  },
});
```

### Aliases
```graphql
query {
  # Fetch same field with different arguments
  user1: user(id: "1") {
    name
  }
  user2: user(id: "2") {
    name
  }

  # Alias for clarity
  currentUser: me {
    id
    name
  }
}
```

### Fragments
```graphql
# Define reusable fragment
fragment UserFields on User {
  id
  name
  email
  createdAt
}

fragment PostSummary on Post {
  id
  title
  publishedAt
  author {
    ...UserFields
  }
}

# Use fragments in query
query {
  user(id: "1") {
    ...UserFields
    posts {
      ...PostSummary
    }
  }
}
```

### Directives
```graphql
# Built-in directives
query GetUser($id: ID!, $withPosts: Boolean!, $skipEmail: Boolean!) {
  user(id: $id) {
    name
    email @skip(if: $skipEmail)
    posts @include(if: $withPosts) {
      title
    }
  }
}

# Custom directive definition
directive @auth(requires: Role = USER) on FIELD_DEFINITION

type Query {
  users: [User!]! @auth(requires: ADMIN)
  me: User! @auth
}
```

### Mutations Best Practices
```graphql
# Single mutation with input type
type Mutation {
  createPost(input: CreatePostInput!): CreatePostPayload!
  updatePost(id: ID!, input: UpdatePostInput!): UpdatePostPayload!
  deletePost(id: ID!): DeletePostPayload!
}

input CreatePostInput {
  title: String!
  content: String!
  categoryId: ID!
  tags: [String!]
}

# Payload pattern for mutations
type CreatePostPayload {
  post: Post          # Created resource
  userErrors: [UserError!]!  # Client errors
  success: Boolean!
}

type UserError {
  field: String!      # Which field caused error
  message: String!    # Human-readable message
}
```

---

## Resolvers and DataLoaders

### Resolver Signature
```typescript
type Resolver<TParent, TArgs, TContext, TResult> = (
  parent: TParent,      // Parent object
  args: TArgs,          // Field arguments
  context: TContext,    // Shared context (auth, db, etc.)
  info: GraphQLResolveInfo  // Query metadata
) => TResult | Promise<TResult>;
```

### Basic Resolvers
```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, { db }) => {
      return db.users.findById(id);
    },

    users: async (_, { limit = 10, offset = 0 }, { db }) => {
      return db.users.findMany({ limit, offset });
    },
  },

  Mutation: {
    createUser: async (_, { input }, { db, userId }) => {
      if (!userId) {
        throw new Error('Authentication required');
      }

      const user = await db.users.create(input);
      return { user, userErrors: [], success: true };
    },
  },

  User: {
    // Field resolver - only called if client requests 'posts'
    posts: async (user, _, { db }) => {
      return db.posts.findByAuthorId(user.id);
    },

    // Computed field
    fullName: (user) => {
      return `${user.firstName} ${user.lastName}`;
    },
  },
};
```

### The N+1 Problem
```typescript
// ❌ BAD - N+1 queries
const resolvers = {
  Query: {
    users: () => db.users.findMany(), // 1 query
  },
  User: {
    // Called for EACH user - N queries!
    posts: (user) => db.posts.findByAuthorId(user.id),
  },
};

// Querying 100 users = 1 + 100 = 101 database queries!
```

### DataLoader Solution
```typescript
import DataLoader from 'dataloader';

// Batch function - receives array of keys
async function batchLoadPosts(authorIds: string[]) {
  const posts = await db.posts.findByAuthorIds(authorIds);

  // Group by author ID
  const postsByAuthor = authorIds.map(authorId =>
    posts.filter(post => post.authorId === authorId)
  );

  return postsByAuthor;
}

// Create context with loaders
function createContext({ req }) {
  return {
    db,
    userId: req.userId,
    loaders: {
      posts: new DataLoader(batchLoadPosts),
    },
  };
}

// ✅ GOOD - Batched queries
const resolvers = {
  Query: {
    users: () => db.users.findMany(), // 1 query
  },
  User: {
    // Uses DataLoader - batches all requests into 1 query!
    posts: (user, _, { loaders }) => {
      return loaders.posts.load(user.id);
    },
  },
};

// Querying 100 users = 1 + 1 = 2 database queries!
```

### Advanced DataLoader Patterns
```typescript
// DataLoader with caching
const userLoader = new DataLoader(
  async (ids) => {
    const users = await db.users.findByIds(ids);
    return ids.map(id => users.find(u => u.id === id));
  },
  {
    cache: true,           // Enable caching (default)
    maxBatchSize: 100,     // Limit batch size
    batchScheduleFn: (cb) => setTimeout(cb, 10), // Debounce batching
  }
);

// Cache manipulation
userLoader.clear(id);              // Clear single key
userLoader.clearAll();             // Clear entire cache
userLoader.prime(id, user);        // Prime cache with value
```

---

## Subscriptions

### WebSocket Setup (Apollo Server)
```typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { makeExecutableSchema } from '@graphql-tools/schema';
import express from 'express';

const app = express();
const httpServer = createServer(app);

const schema = makeExecutableSchema({ typeDefs, resolvers });

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});

await server.start();
app.use('/graphql', express.json(), expressMiddleware(server));

httpServer.listen(4000);
```

### Subscription Schema
```graphql
type Subscription {
  postCreated: Post!
  postUpdated(id: ID!): Post!
  messageAdded(channelId: ID!): Message!
  userStatusChanged(userId: ID!): UserStatus!
}

type Message {
  id: ID!
  text: String!
  author: User!
  channelId: ID!
  createdAt: DateTime!
}

enum UserStatus {
  ONLINE
  OFFLINE
  AWAY
}
```

### Subscription Resolvers (PubSub)
```typescript
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    createPost: async (_, { input }, { db }) => {
      const post = await db.posts.create(input);

      // Publish to subscribers
      pubsub.publish('POST_CREATED', { postCreated: post });

      return { post, success: true, userErrors: [] };
    },

    sendMessage: async (_, { channelId, text }, { db, userId }) => {
      const message = await db.messages.create({
        channelId,
        text,
        authorId: userId,
      });

      pubsub.publish(`MESSAGE_${channelId}`, {
        messageAdded: message,
      });

      return message;
    },
  },

  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator(['POST_CREATED']),
    },

    postUpdated: {
      subscribe: (_, { id }) => pubsub.asyncIterator([`POST_UPDATED_${id}`]),
    },

    messageAdded: {
      subscribe: (_, { channelId }) => {
        return pubsub.asyncIterator([`MESSAGE_${channelId}`]);
      },
    },
  },
};
```

### Client Subscriptions (Apollo Client)
```typescript
import { ApolloClient, InMemoryCache, split, HttpLink } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

// HTTP link for queries and mutations
const httpLink = new HttpLink({
  uri: 'http://localhost:4000/graphql',
});

// WebSocket link for subscriptions
const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
  })
);

// Split based on operation type
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache(),
});

// Use subscription
const MESSAGES_SUBSCRIPTION = gql`
  subscription OnMessageAdded($channelId: ID!) {
    messageAdded(channelId: $channelId) {
      id
      text
      author {
        name
      }
      createdAt
    }
  }
`;

function ChatComponent({ channelId }) {
  const { data, loading } = useSubscription(MESSAGES_SUBSCRIPTION, {
    variables: { channelId },
  });

  if (loading) return <p>Loading...</p>;

  return <div>New message: {data.messageAdded.text}</div>;
}
```

### Redis PubSub (Production)
```typescript
import { RedisPubSub } from 'graphql-redis-subscriptions';
import Redis from 'ioredis';

const options = {
  host: 'localhost',
  port: 6379,
  retryStrategy: (times) => Math.min(times * 50, 2000),
};

const pubsub = new RedisPubSub({
  publisher: new Redis(options),
  subscriber: new Redis(options),
});

// Use same as in-memory PubSub
pubsub.publish('POST_CREATED', { postCreated: post });
pubsub.asyncIterator(['POST_CREATED']);
```

---

## Error Handling

### Error Types
```typescript
import { GraphQLError } from 'graphql';

// Custom error classes
class AuthenticationError extends GraphQLError {
  constructor(message: string) {
    super(message, {
      extensions: {
        code: 'UNAUTHENTICATED',
        http: { status: 401 },
      },
    });
  }
}

class ForbiddenError extends GraphQLError {
  constructor(message: string) {
    super(message, {
      extensions: {
        code: 'FORBIDDEN',
        http: { status: 403 },
      },
    });
  }
}

class ValidationError extends GraphQLError {
  constructor(message: string, invalidFields: Record<string, string>) {
    super(message, {
      extensions: {
        code: 'BAD_USER_INPUT',
        invalidFields,
      },
    });
  }
}
```

### Throwing Errors in Resolvers
```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, { db, userId }) => {
      if (!userId) {
        throw new AuthenticationError('Must be logged in');
      }

      const user = await db.users.findById(id);
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: { code: 'NOT_FOUND' },
        });
      }

      return user;
    },
  },

  Mutation: {
    createPost: async (_, { input }, { db, userId }) => {
      const errors: Record<string, string> = {};

      if (!input.title || input.title.length < 3) {
        errors.title = 'Title must be at least 3 characters';
      }

      if (!input.content) {
        errors.content = 'Content is required';
      }

      if (Object.keys(errors).length > 0) {
        throw new ValidationError('Invalid input', errors);
      }

      const post = await db.posts.create({ ...input, authorId: userId });
      return { post, success: true, userErrors: [] };
    },
  },
};
```

### Error Response Format
```json
{
  "errors": [
    {
      "message": "User not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND"
      }
    }
  ],
  "data": {
    "user": null
  }
}
```

### Field-Level Error Handling
```typescript
// Nullable fields allow partial results
type Query {
  user(id: ID!): User        # null on error
  users: [User!]!            # throws on error
  post(id: ID!): Post        # null on error
}

// Resolver can return null instead of throwing
const resolvers = {
  Query: {
    user: async (_, { id }, { db }) => {
      try {
        return await db.users.findById(id);
      } catch (error) {
        console.error('Failed to fetch user:', error);
        return null;  // Returns null instead of error
      }
    },
  },
};
```

---

## Schema Design Patterns

### Relay Cursor Connections
```graphql
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type Query {
  posts(
    first: Int
    after: String
    last: Int
    before: String
  ): PostConnection!
}
```

### Relay Connection Resolver
```typescript
import { fromGlobalId, toGlobalId } from 'graphql-relay';

function encodeCursor(id: string): string {
  return Buffer.from(`cursor:${id}`).toString('base64');
}

function decodeCursor(cursor: string): string {
  return Buffer.from(cursor, 'base64').toString('utf-8').replace('cursor:', '');
}

const resolvers = {
  Query: {
    posts: async (_, { first = 10, after }, { db }) => {
      const startId = after ? decodeCursor(after) : null;

      // Fetch first + 1 to determine hasNextPage
      const posts = await db.posts.findMany({
        where: startId ? { id: { gt: startId } } : {},
        take: first + 1,
        orderBy: { createdAt: 'desc' },
      });

      const hasNextPage = posts.length > first;
      const nodes = hasNextPage ? posts.slice(0, -1) : posts;

      const edges = nodes.map(node => ({
        node,
        cursor: encodeCursor(node.id),
      }));

      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor,
        },
        totalCount: await db.posts.count(),
      };
    },
  },
};
```

### Offset Pagination (Simpler)
```graphql
type PostsResponse {
  posts: [Post!]!
  total: Int!
  hasMore: Boolean!
}

type Query {
  posts(limit: Int = 10, offset: Int = 0): PostsResponse!
}
```

### Global Object Identification (Relay)
```graphql
interface Node {
  id: ID!  # Global unique ID
}

type User implements Node {
  id: ID!
  name: String!
}

type Post implements Node {
  id: ID!
  title: String!
}

type Query {
  node(id: ID!): Node
}
```

```typescript
const resolvers = {
  Query: {
    node: async (_, { id }, { db }) => {
      const { type, id: rawId } = fromGlobalId(id);

      switch (type) {
        case 'User':
          return db.users.findById(rawId);
        case 'Post':
          return db.posts.findById(rawId);
        default:
          return null;
      }
    },
  },

  User: {
    id: (user) => toGlobalId('User', user.id),
  },

  Post: {
    id: (post) => toGlobalId('Post', post.id),
  },
};
```

---

## Server Implementations

### Apollo Server (TypeScript)
```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production',
  plugins: [
    // Custom plugin
    {
      async requestDidStart() {
        return {
          async willSendResponse({ response }) {
            console.log('Response:', response);
          },
        };
      },
    },
  ],
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => ({
    token: req.headers.authorization,
    db: database,
  }),
});
```

### GraphQL Yoga (Modern Alternative)
```typescript
import { createYoga, createSchema } from 'graphql-yoga';
import { createServer } from 'node:http';

const yoga = createYoga({
  schema: createSchema({
    typeDefs,
    resolvers,
  }),
  graphiql: true,
  context: ({ request }) => ({
    userId: request.headers.get('x-user-id'),
  }),
});

const server = createServer(yoga);
server.listen(4000, () => {
  console.log('Server on http://localhost:4000/graphql');
});
```

### Graphene (Python/Django)
```python
import graphene
from graphene_django import DjangoObjectType
from .models import User, Post

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'

class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    posts = graphene.List(PostType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_posts(self, info):
        return Post.objects.all()

class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()

    def mutate(self, info, name, email):
        user = User.objects.create(name=name, email=email)
        return CreateUser(user=user, success=True)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
```

### Strawberry (Python, Modern)
```python
import strawberry
from typing import List, Optional
from datetime import datetime

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    created_at: datetime

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    author_id: strawberry.ID

@strawberry.input
class CreateUserInput:
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return User.objects.all()

    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        return User.objects.get(pk=id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> User:
        return User.objects.create(**input.__dict__)

schema = strawberry.Schema(query=Query, mutation=Mutation)

# FastAPI integration
from strawberry.fastapi import GraphQLRouter

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

---

## Client Integrations

### Apollo Client (React)
```typescript
import { ApolloClient, InMemoryCache, ApolloProvider, useQuery, useMutation } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:4000/graphql',
  cache: new InMemoryCache(),
});

function App() {
  return (
    <ApolloProvider client={client}>
      <UserList />
    </ApolloProvider>
  );
}

function UserList() {
  const { loading, error, data, refetch } = useQuery(GET_USERS);
  const [createUser] = useMutation(CREATE_USER, {
    refetchQueries: [{ query: GET_USERS }],
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {data.users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
      <button onClick={() => createUser({ variables: { name: 'New User' } })}>
        Add User
      </button>
    </div>
  );
}
```

### urql (Lightweight Alternative)
```typescript
import { createClient, Provider, useQuery, useMutation } from 'urql';

const client = createClient({
  url: 'http://localhost:4000/graphql',
});

function App() {
  return (
    <Provider value={client}>
      <UserList />
    </Provider>
  );
}

function UserList() {
  const [result, reexecuteQuery] = useQuery({ query: GET_USERS });
  const [, createUser] = useMutation(CREATE_USER);

  const { data, fetching, error } = result;

  if (fetching) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {data.users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### graphql-request (Minimal)
```typescript
import { GraphQLClient, gql } from 'graphql-request';

const client = new GraphQLClient('http://localhost:4000/graphql');

async function fetchUsers() {
  const query = gql`
    query {
      users {
        id
        name
      }
    }
  `;

  const data = await client.request(query);
  return data.users;
}

async function createUser(name: string) {
  const mutation = gql`
    mutation CreateUser($name: String!) {
      createUser(name: $name) {
        id
        name
      }
    }
  `;

  const data = await client.request(mutation, { name });
  return data.createUser;
}
```

### TanStack Query + GraphQL
```typescript
import { useQuery, useMutation, QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { GraphQLClient } from 'graphql-request';

const graphQLClient = new GraphQLClient('http://localhost:4000/graphql');

function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { users } = await graphQLClient.request(GET_USERS);
      return users;
    },
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (name: string) => {
      const { createUser } = await graphQLClient.request(CREATE_USER, { name });
      return createUser;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

---

## TypeScript Code Generation

### GraphQL Code Generator Setup
```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations @graphql-codegen/typescript-react-apollo
```

### codegen.yml
```yaml
schema: http://localhost:4000/graphql
documents: 'src/**/*.graphql'
generates:
  src/generated/graphql.ts:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
    config:
      withHooks: true
      withComponent: false
      skipTypename: false
      enumsAsTypes: true
```

### Generated Types
```typescript
// src/queries/users.graphql
// query GetUsers {
//   users {
//     id
//     name
//     email
//   }
// }

// Generated types
export type GetUsersQuery = {
  __typename?: 'Query';
  users: Array<{
    __typename?: 'User';
    id: string;
    name: string;
    email: string;
  }>;
};

export function useGetUsersQuery(
  baseOptions?: Apollo.QueryHookOptions<GetUsersQuery, GetUsersQueryVariables>
) {
  return Apollo.useQuery<GetUsersQuery, GetUsersQueryVariables>(
    GetUsersDocument,
    baseOptions
  );
}
```

### Usage with Generated Types
```typescript
import { useGetUsersQuery, useCreateUserMutation } from './generated/graphql';

function UserList() {
  const { data, loading, error } = useGetUsersQuery();
  const [createUser] = useCreateUserMutation();

  // Fully typed!
  const users = data?.users; // Type: User[] | undefined
}
```

---

## Authentication and Authorization

### Context-Based Auth
```typescript
import jwt from 'jsonwebtoken';

async function createContext({ req }) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return { userId: null, db };
  }

  try {
    const { userId } = jwt.verify(token, process.env.JWT_SECRET);
    return { userId, db };
  } catch (error) {
    return { userId: null, db };
  }
}

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

await startStandaloneServer(server, {
  context: createContext,
});
```

### Resolver-Level Auth
```typescript
const resolvers = {
  Query: {
    me: (_, __, { userId }) => {
      if (!userId) {
        throw new AuthenticationError('Not authenticated');
      }
      return db.users.findById(userId);
    },

    users: (_, __, { userId, db }) => {
      if (!userId) {
        throw new AuthenticationError('Not authenticated');
      }

      const user = db.users.findById(userId);
      if (user.role !== 'ADMIN') {
        throw new ForbiddenError('Admin access required');
      }

      return db.users.findMany();
    },
  },
};
```

### Directive-Based Auth
```typescript
import { mapSchema, getDirective, MapperKind } from '@graphql-tools/utils';

// Schema with directive
const typeDefs = gql`
  directive @auth(requires: Role = USER) on FIELD_DEFINITION

  enum Role {
    ADMIN
    USER
  }

  type Query {
    users: [User!]! @auth(requires: ADMIN)
    me: User! @auth
  }
`;

// Directive transformer
function authDirectiveTransformer(schema, directiveName = 'auth') {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, directiveName)?.[0];

      if (authDirective) {
        const { requires } = authDirective;
        const { resolve = defaultFieldResolver } = fieldConfig;

        fieldConfig.resolve = async (source, args, context, info) => {
          if (!context.userId) {
            throw new AuthenticationError('Not authenticated');
          }

          if (requires) {
            const user = await context.db.users.findById(context.userId);
            if (user.role !== requires) {
              throw new ForbiddenError(`${requires} role required`);
            }
          }

          return resolve(source, args, context, info);
        };
      }

      return fieldConfig;
    },
  });
}

let schema = makeExecutableSchema({ typeDefs, resolvers });
schema = authDirectiveTransformer(schema);
```

---

## Performance Optimization

### Query Complexity Analysis
```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10,
    }),
  ],
});
```

### Persistent Queries (APQ)
```typescript
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginInlineTraceDisabled } from '@apollo/server/plugin/disabled';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    cache: new Map(), // Or Redis
  },
});

// Client sends hash instead of full query
// Reduces payload size by ~80%
```

### Response Caching
```typescript
import responseCachePlugin from '@apollo/server-plugin-response-cache';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    responseCachePlugin({
      sessionId: (context) => context.userId || null,
      shouldReadFromCache: (context) => !context.userId, // Cache only public queries
    }),
  ],
});

// Schema directive for cache control
const typeDefs = gql`
  type Query {
    posts: [Post!]! @cacheControl(maxAge: 60)
    user(id: ID!): User @cacheControl(maxAge: 30)
  }
`;
```

### Field-Level Caching
```typescript
import { InMemoryLRUCache } from '@apollo/utils.keyvaluecache';

const cache = new InMemoryLRUCache({
  maxSize: Math.pow(2, 20) * 100, // 100 MB
  ttl: 300, // 5 minutes
});

const resolvers = {
  Query: {
    user: async (_, { id }, { cache, db }) => {
      const cacheKey = `user:${id}`;
      const cached = await cache.get(cacheKey);

      if (cached) {
        return JSON.parse(cached);
      }

      const user = await db.users.findById(id);
      await cache.set(cacheKey, JSON.stringify(user), { ttl: 60 });

      return user;
    },
  },
};
```

---

## File Uploads

### Schema
```graphql
scalar Upload

type Mutation {
  uploadFile(file: Upload!): File!
  uploadMultiple(files: [Upload!]!): [File!]!
}

type File {
  filename: String!
  mimetype: String!
  encoding: String!
  url: String!
}
```

### Server (graphql-upload)
```typescript
import graphqlUploadExpress from 'graphql-upload/graphqlUploadExpress.mjs';
import { GraphQLUpload } from 'graphql-upload/GraphQLUpload.mjs';
import fs from 'fs';
import path from 'path';

app.use('/graphql', graphqlUploadExpress({ maxFileSize: 10000000, maxFiles: 10 }));

const resolvers = {
  Upload: GraphQLUpload,

  Mutation: {
    uploadFile: async (_, { file }) => {
      const { createReadStream, filename, mimetype, encoding } = await file;

      const stream = createReadStream();
      const uploadPath = path.join(__dirname, 'uploads', filename);

      await new Promise((resolve, reject) => {
        stream
          .pipe(fs.createWriteStream(uploadPath))
          .on('finish', resolve)
          .on('error', reject);
      });

      return {
        filename,
        mimetype,
        encoding,
        url: `/uploads/${filename}`,
      };
    },
  },
};
```

### Client (Apollo Client)
```typescript
import { useMutation } from '@apollo/client';

const UPLOAD_FILE = gql`
  mutation UploadFile($file: Upload!) {
    uploadFile(file: $file) {
      filename
      url
    }
  }
`;

function FileUpload() {
  const [uploadFile] = useMutation(UPLOAD_FILE);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    uploadFile({ variables: { file } });
  };

  return <input type="file" onChange={handleFileChange} />;
}
```

---

## Testing

### Unit Testing Resolvers
```typescript
import { describe, it, expect, vi } from 'vitest';

describe('User Resolvers', () => {
  it('should fetch user by ID', async () => {
    const mockDb = {
      users: {
        findById: vi.fn().mockResolvedValue({
          id: '1',
          name: 'Alice',
          email: 'alice@example.com',
        }),
      },
    };

    const result = await resolvers.Query.user(
      null,
      { id: '1' },
      { db: mockDb, userId: '1' },
      {} as any
    );

    expect(result.name).toBe('Alice');
    expect(mockDb.users.findById).toHaveBeenCalledWith('1');
  });

  it('should throw error when not authenticated', async () => {
    await expect(
      resolvers.Query.me(null, {}, { userId: null }, {} as any)
    ).rejects.toThrow('Not authenticated');
  });
});
```

### Integration Testing (Apollo Server)
```typescript
import { ApolloServer } from '@apollo/server';
import assert from 'assert';

it('fetches users', async () => {
  const server = new ApolloServer({ typeDefs, resolvers });

  const response = await server.executeOperation({
    query: 'query { users { id name } }',
  });

  assert(response.body.kind === 'single');
  expect(response.body.singleResult.errors).toBeUndefined();
  expect(response.body.singleResult.data?.users).toHaveLength(2);
});

it('creates user', async () => {
  const response = await server.executeOperation({
    query: `
      mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
          user { id name }
          success
        }
      }
    `,
    variables: {
      input: { name: 'Charlie', email: 'charlie@example.com' },
    },
  });

  assert(response.body.kind === 'single');
  expect(response.body.singleResult.data?.createUser.success).toBe(true);
});
```

### E2E Testing (Supertest)
```typescript
import request from 'supertest';
import { app } from './server';

describe('GraphQL API', () => {
  it('should query users', async () => {
    const response = await request(app)
      .post('/graphql')
      .send({
        query: '{ users { id name } }',
      })
      .expect(200);

    expect(response.body.data.users).toBeDefined();
  });

  it('should require authentication', async () => {
    const response = await request(app)
      .post('/graphql')
      .send({
        query: '{ me { id } }',
      })
      .expect(200);

    expect(response.body.errors[0].extensions.code).toBe('UNAUTHENTICATED');
  });
});
```

---

## Production Patterns

### Schema Stitching
```typescript
import { stitchSchemas } from '@graphql-tools/stitch';

const userSchema = makeExecutableSchema({ typeDefs: userTypeDefs, resolvers: userResolvers });
const postSchema = makeExecutableSchema({ typeDefs: postTypeDefs, resolvers: postResolvers });

const schema = stitchSchemas({
  subschemas: [
    { schema: userSchema },
    { schema: postSchema },
  ],
});
```

### Apollo Federation
```typescript
// User service
import { buildSubgraphSchema } from '@apollo/subgraph';

const typeDefs = gql`
  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
  }
`;

const resolvers = {
  User: {
    __resolveReference(user, { db }) {
      return db.users.findById(user.id);
    },
  },
};

const schema = buildSubgraphSchema({ typeDefs, resolvers });

// Post service
const typeDefs = gql`
  extend type User @key(fields: "id") {
    id: ID! @external
    posts: [Post!]!
  }

  type Post @key(fields: "id") {
    id: ID!
    title: String!
    authorId: ID!
  }
`;

// Gateway
import { ApolloGateway } from '@apollo/gateway';

const gateway = new ApolloGateway({
  supergraphSdl: readFileSync('./supergraph.graphql', 'utf-8'),
});

const server = new ApolloServer({ gateway });
```

### Rate Limiting
```typescript
import { GraphQLRateLimitDirective } from 'graphql-rate-limit-directive';

const typeDefs = gql`
  directive @rateLimit(
    limit: Int = 10
    duration: Int = 60
  ) on FIELD_DEFINITION

  type Query {
    users: [User!]! @rateLimit(limit: 100, duration: 60)
    search(query: String!): [Result!]! @rateLimit(limit: 10, duration: 60)
  }
`;

let schema = makeExecutableSchema({ typeDefs, resolvers });
schema = GraphQLRateLimitDirective()(schema);
```

### Monitoring (Apollo Studio)
```typescript
import { ApolloServerPluginUsageReporting } from '@apollo/server/plugin/usageReporting';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    ApolloServerPluginUsageReporting({
      sendVariableValues: { all: true },
      sendHeaders: { all: true },
    }),
  ],
});
```

---

## Framework Integration

### Next.js App Router
```typescript
// app/api/graphql/route.ts
import { ApolloServer } from '@apollo/server';
import { startServerAndCreateNextHandler } from '@as-integrations/next';

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const handler = startServerAndCreateNextHandler(server);

export { handler as GET, handler as POST };
```

### Next.js with Apollo Client (SSR)
```typescript
// lib/apollo-client.ts
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';
import { registerApolloClient } from '@apollo/experimental-nextjs-app-support/rsc';

export const { getClient } = registerApolloClient(() => {
  return new ApolloClient({
    cache: new InMemoryCache(),
    link: new HttpLink({
      uri: 'http://localhost:4000/graphql',
    }),
  });
});

// app/users/page.tsx
import { getClient } from '@/lib/apollo-client';
import { gql } from '@apollo/client';

export default async function UsersPage() {
  const { data } = await getClient().query({
    query: gql`
      query GetUsers {
        users {
          id
          name
        }
      }
    `,
  });

  return (
    <div>
      {data.users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### FastAPI + Strawberry
```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Comparison with REST and tRPC

### GraphQL vs REST
| Feature | GraphQL | REST |
|---------|---------|------|
| Endpoints | Single endpoint | Multiple endpoints |
| Data Fetching | Client specifies fields | Server determines response |
| Over-fetching | No | Yes (extra fields) |
| Under-fetching | No | Yes (multiple requests) |
| Versioning | Not needed | Required (v1, v2) |
| Caching | Complex | Simple (HTTP caching) |
| Type System | Built-in | External (OpenAPI) |
| Real-time | Subscriptions | SSE/WebSocket |

### GraphQL vs tRPC
| Feature | GraphQL | tRPC |
|---------|---------|------|
| Type Safety | Codegen required | Native TypeScript |
| Language Support | Any | TypeScript only |
| Client-Server Coupling | Loose | Tight |
| Schema | SDL required | Inferred from code |
| Learning Curve | Steep | Gentle |
| Tooling | Extensive | Growing |
| Use Case | Public APIs, Mobile | Full-stack TypeScript |

---

## Migration Strategies

### REST to GraphQL (Gradual)
```typescript
// 1. Wrap existing REST endpoints
const resolvers = {
  Query: {
    user: async (_, { id }) => {
      const response = await fetch(`https://api.example.com/users/${id}`);
      return response.json();
    },
  },
};

// 2. Add GraphQL layer alongside REST
app.use('/api/rest', restRouter);
app.use('/graphql', graphqlMiddleware);

// 3. Migrate clients incrementally
// 4. Deprecate REST endpoints when ready
```

### Adding GraphQL to Existing App
```typescript
// Express + GraphQL
import express from 'express';
import { expressMiddleware } from '@apollo/server/express4';

const app = express();

// Existing routes
app.use('/api', existingApiRouter);

// Add GraphQL
app.use('/graphql', express.json(), expressMiddleware(server));
```

---

## Best Practices

### Schema Design
- Use semantic field names (`createdAt`, not `created_at`)
- Prefer specific types over generic JSON
- Use enums for fixed value sets
- Design for client use cases, not database structure
- Use input types for complex mutations
- Implement pagination for lists
- Follow Relay specification for connections

### Resolver Patterns
- Keep resolvers thin, delegate to service layer
- Use DataLoader for all database fetches
- Validate inputs in resolvers, not database layer
- Return errors in payload, not just exceptions
- Use context for shared dependencies (db, auth, loaders)

### Error Handling
- Use custom error types with error codes
- Return field-level errors for mutations
- Log errors server-side, sanitize for clients
- Use nullable fields to allow partial results
- Don't expose internal implementation details

### Performance
- Always use DataLoader to prevent N+1
- Implement query complexity limits
- Cache frequently accessed data
- Use persisted queries in production
- Monitor slow queries and optimize
- Batch mutations when possible

### Security
- Implement authentication and authorization
- Validate all inputs
- Use query depth limiting
- Implement rate limiting per user
- Disable introspection in production (optional)
- Sanitize error messages

### Testing
- Test resolvers in isolation
- Mock external dependencies
- Test error conditions
- Integration test critical flows
- E2E test with real client

### Documentation
- Write clear field descriptions
- Document deprecations with `@deprecated`
- Provide usage examples in schema comments
- Keep schema documentation up-to-date

---

## Summary

GraphQL provides a powerful, flexible API layer with strong typing, efficient data fetching, and excellent developer experience. Key advantages include:

- **Client Control**: Fetch exactly what you need
- **Type Safety**: Schema-first design with introspection
- **Single Endpoint**: Simplified API surface
- **Real-time**: Built-in subscription support
- **Tooling**: Excellent ecosystem (Apollo, Relay, codegen)

**Trade-offs to Consider**:
- More complex than REST for simple CRUD
- Caching requires more thought than HTTP caching
- Learning curve for teams new to GraphQL
- Query complexity can impact performance

**Best For**:
- Mobile apps needing bandwidth efficiency
- Complex frontends with varied data needs
- Microservices aggregation
- Real-time applications
- Multi-platform clients (web, mobile, IoT)

**Start Simple**:
1. Define schema for core entities
2. Write resolvers with DataLoader
3. Add authentication/authorization
4. Implement error handling
5. Optimize with caching
6. Add subscriptions if needed
7. Monitor and iterate

GraphQL shines when API flexibility and developer experience are priorities. Combined with TypeScript code generation, it provides end-to-end type safety from database to UI.
