---
name: vue
description: Vue 3 - Progressive JavaScript framework with Composition API, reactivity system, single-file components, Vite integration, TypeScript support
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Progressive JavaScript framework: Composition API with setup(), reactive refs/computed, Vue Router, Pinia state, TypeScript, Vite"
    when_to_use: "Interactive UIs with gradual adoption, SPAs with Vue Router, progressive web apps, TypeScript projects with Vue DevTools"
    quick_start: "1. npm create vue@latest 2. Choose TypeScript + Router + Pinia 3. Use setup() with ref/reactive 4. npm run dev"
  context_limit: 80
tags:
  - vue
  - vue3
  - composition-api
  - reactivity
  - sfc
  - pinia
  - router
  - vite
  - typescript
  - frontend
requires_tools: []
---

# Vue 3 - Progressive JavaScript Framework

## Overview

Vue 3 is a **progressive framework** for building user interfaces with emphasis on approachability, performance, and flexibility. It features the **Composition API** for better logic reuse, a powerful **reactivity system**, and **single-file components** (.vue files).

**Key Features**:
- **Composition API**: setup() with ref, reactive, computed, watch
- **Reactivity System**: Fine-grained reactive data tracking
- **Single-File Components**: Template, script, style in one file
- **Vue Router**: Official routing for SPAs
- **Pinia**: Modern state management (Vuex successor)
- **TypeScript**: First-class TypeScript support
- **Vite**: Lightning-fast development with HMR

**Installation**:
```bash
# Create new Vue 3 project (recommended)
npm create vue@latest my-app
cd my-app
npm install
npm run dev

# Or with Vite template
npm create vite@latest my-app -- --template vue-ts
```

## Composition API Fundamentals

### setup() Function

```vue
<script setup lang="ts">
// Modern <script setup> syntax (recommended)
import { ref, computed, onMounted } from 'vue';

// Reactive state
const count = ref(0);
const message = ref('Hello Vue 3');

// Computed values
const doubled = computed(() => count.value * 2);

// Methods
function increment() {
  count.value++;
}

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted');
});
</script>

<template>
  <div>
    <p>Count: {{ count }} (Doubled: {{ doubled }})</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

### Reactive State with ref() and reactive()

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue';

// ref() - for primitives and objects (needs .value in script)
const count = ref(0);
const user = ref({ name: 'Alice', age: 30 });

console.log(count.value); // 0
console.log(user.value.name); // 'Alice'

// reactive() - for objects only (no .value needed)
const state = reactive({
  todos: [] as Todo[],
  filter: 'all',
  error: null as string | null
});

console.log(state.todos); // []
state.todos.push({ id: 1, text: 'Learn Vue', done: false });
</script>

<template>
  <!-- In template, .value is automatic for refs -->
  <p>Count: {{ count }}</p>
  <p>User: {{ user.name }}</p>
  <p>Todos: {{ state.todos.length }}</p>
</template>
```

### Computed Properties

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

// Read-only computed
const fullName = computed(() => `${firstName.value} ${lastName.value}`);

// Writable computed
const fullNameWritable = computed({
  get() {
    return `${firstName.value} ${lastName.value}`;
  },
  set(value: string) {
    const parts = value.split(' ');
    firstName.value = parts[0];
    lastName.value = parts[1];
  }
});

// Complex computations
interface Todo {
  id: number;
  text: string;
  done: boolean;
}

const todos = ref<Todo[]>([
  { id: 1, text: 'Learn Vue', done: true },
  { id: 2, text: 'Build app', done: false }
]);

const completedTodos = computed(() =>
  todos.value.filter(t => t.done)
);

const activeTodos = computed(() =>
  todos.value.filter(t => !t.done)
);

const progress = computed(() =>
  todos.value.length > 0
    ? (completedTodos.value.length / todos.value.length) * 100
    : 0
);
</script>

<template>
  <div>
    <p>Full Name: {{ fullName }}</p>
    <p>Progress: {{ progress.toFixed(1) }}%</p>
    <p>Active: {{ activeTodos.length }} | Done: {{ completedTodos.length }}</p>
  </div>
</template>
```

### Watchers and Side Effects

```vue
<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue';

const count = ref(0);
const user = ref({ name: 'Alice', age: 30 });

// watch() - explicit dependencies
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`);
});

// Watch multiple sources
watch([count, user], ([newCount, newUser], [oldCount, oldUser]) => {
  console.log('Count or user changed');
});

// Watch object property (needs getter)
watch(
  () => user.value.name,
  (newName, oldName) => {
    console.log(`Name changed from ${oldName} to ${newName}`);
  }
);

// Deep watch for nested objects
watch(
  user,
  (newUser) => {
    console.log('User object changed deeply');
  },
  { deep: true }
);

// watchEffect() - automatic dependency tracking
watchEffect(() => {
  // Automatically watches count and user
  console.log(`Count: ${count.value}, User: ${user.value.name}`);
});

// Cleanup function
watchEffect((onCleanup) => {
  const timer = setTimeout(() => {
    console.log('Delayed effect');
  }, 1000);

  onCleanup(() => {
    clearTimeout(timer);
  });
});
</script>
```

## Component Props and Events

### Defining Props (TypeScript)

```vue
<script setup lang="ts">
// Type-safe props with defineProps
interface Props {
  title: string;
  count?: number;
  tags?: string[];
  user: {
    name: string;
    email: string;
  };
  disabled?: boolean;
}

// With defaults
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  tags: () => [],
  disabled: false
});

// Access props
console.log(props.title);
console.log(props.count);
</script>

<template>
  <div>
    <h1>{{ title }}</h1>
    <p>Count: {{ count }}</p>
    <p>Tags: {{ tags.join(', ') }}</p>
  </div>
</template>
```

### Emitting Events

```vue
<script setup lang="ts">
// Define emitted events with types
const emit = defineEmits<{
  update: [value: number];
  submit: [data: { name: string; email: string }];
  delete: [id: number];
}>();

function handleClick() {
  emit('update', 42);
}

function handleSubmit() {
  emit('submit', { name: 'Alice', email: 'alice@example.com' });
}
</script>

<template>
  <button @click="handleClick">Update</button>
  <button @click="handleSubmit">Submit</button>
</template>
```

### v-model for Two-Way Binding

```vue
<!-- Child: CustomInput.vue -->
<script setup lang="ts">
// v-model creates 'modelValue' prop and 'update:modelValue' event
const props = defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string];
}>();

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
}
</script>

<template>
  <input
    :value="modelValue"
    @input="handleInput"
    :placeholder="placeholder"
  />
</template>

<!-- Parent.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import CustomInput from './CustomInput.vue';

const searchQuery = ref('');
</script>

<template>
  <CustomInput v-model="searchQuery" placeholder="Search..." />
  <p>Searching for: {{ searchQuery }}</p>
</template>
```

### Multiple v-model Bindings

```vue
<!-- Child: UserForm.vue -->
<script setup lang="ts">
defineProps<{
  firstName: string;
  lastName: string;
}>();

const emit = defineEmits<{
  'update:firstName': [value: string];
  'update:lastName': [value: string];
}>();
</script>

<template>
  <div>
    <input
      :value="firstName"
      @input="emit('update:firstName', ($event.target as HTMLInputElement).value)"
    />
    <input
      :value="lastName"
      @input="emit('update:lastName', ($event.target as HTMLInputElement).value)"
    />
  </div>
</template>

<!-- Parent.vue -->
<script setup lang="ts">
import { ref } from 'vue';
import UserForm from './UserForm.vue';

const first = ref('John');
const last = ref('Doe');
</script>

<template>
  <UserForm v-model:first-name="first" v-model:last-name="last" />
  <p>Full name: {{ first }} {{ last }}</p>
</template>
```

## Template Syntax

### Directives

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue';

const message = ref('Hello Vue');
const isActive = ref(true);
const hasError = ref(false);
const items = ref(['Apple', 'Banana', 'Cherry']);
const user = ref({ name: 'Alice', email: 'alice@example.com' });

const formData = reactive({
  username: '',
  agree: false,
  gender: 'male',
  interests: [] as string[]
});
</script>

<template>
  <!-- Text interpolation -->
  <p>{{ message }}</p>

  <!-- Raw HTML (careful with XSS!) -->
  <div v-html="'<strong>Bold</strong>'"></div>

  <!-- Attribute binding -->
  <div :id="'container-' + user.name"></div>
  <img :src="user.avatar" :alt="user.name" />

  <!-- Class binding -->
  <div :class="{ active: isActive, 'text-danger': hasError }"></div>
  <div :class="[isActive ? 'active' : '', hasError && 'error']"></div>

  <!-- Style binding -->
  <div :style="{ color: 'red', fontSize: '16px' }"></div>
  <div :style="{ color: isActive ? 'green' : 'gray' }"></div>

  <!-- Conditional rendering -->
  <p v-if="isActive">Active</p>
  <p v-else-if="hasError">Error</p>
  <p v-else>Inactive</p>

  <!-- v-show (toggles display CSS) -->
  <p v-show="isActive">Visible when active</p>

  <!-- List rendering -->
  <ul>
    <li v-for="(item, index) in items" :key="index">
      {{ index + 1 }}. {{ item }}
    </li>
  </ul>

  <!-- Object iteration -->
  <div v-for="(value, key) in user" :key="key">
    {{ key }}: {{ value }}
  </div>

  <!-- Event handling -->
  <button @click="isActive = !isActive">Toggle</button>
  <button @click.prevent="handleSubmit">Submit</button>
  <input @keyup.enter="handleSearch" />

  <!-- Form binding -->
  <input v-model="formData.username" />
  <input type="checkbox" v-model="formData.agree" />
  <input type="radio" v-model="formData.gender" value="male" />
  <input type="radio" v-model="formData.gender" value="female" />
  <select v-model="formData.interests" multiple>
    <option>Reading</option>
    <option>Gaming</option>
    <option>Coding</option>
  </select>
</template>
```

### Event Modifiers

```vue
<template>
  <!-- Prevent default -->
  <form @submit.prevent="handleSubmit">
    <button type="submit">Submit</button>
  </form>

  <!-- Stop propagation -->
  <div @click="handleOuter">
    <button @click.stop="handleInner">Click me</button>
  </div>

  <!-- Capture mode -->
  <div @click.capture="handleCapture">...</div>

  <!-- Self (only if event.target is the element itself) -->
  <div @click.self="handleSelf">...</div>

  <!-- Once (trigger at most once) -->
  <button @click.once="handleOnce">Click once</button>

  <!-- Key modifiers -->
  <input @keyup.enter="handleEnter" />
  <input @keyup.esc="handleEscape" />
  <input @keyup.ctrl.s="handleSave" />
  <input @keyup.shift.t="handleShiftT" />

  <!-- Mouse button modifiers -->
  <div @click.left="handleLeftClick"></div>
  <div @click.right="handleRightClick"></div>
  <div @click.middle="handleMiddleClick"></div>
</template>
```

## Lifecycle Hooks

```vue
<script setup lang="ts">
import {
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onErrorCaptured
} from 'vue';

// Before component is mounted
onBeforeMount(() => {
  console.log('Component about to mount');
});

// After component is mounted (DOM is ready)
onMounted(() => {
  console.log('Component mounted');
  // Good place for API calls, DOM manipulation
  fetchData();
});

// Before component updates due to reactive changes
onBeforeUpdate(() => {
  console.log('Component about to update');
});

// After component updates
onUpdated(() => {
  console.log('Component updated');
  // Careful: can cause infinite loops if you update state here
});

// Before component unmounts
onBeforeUnmount(() => {
  console.log('Component about to unmount');
  // Clean up subscriptions, timers, etc.
});

// After component unmounts
onUnmounted(() => {
  console.log('Component unmounted');
});

// Error handling
onErrorCaptured((err, instance, info) => {
  console.error('Error captured:', err, info);
  return false; // Prevent propagation
});

async function fetchData() {
  const response = await fetch('/api/data');
  const data = await response.json();
  console.log(data);
}
</script>
```

## Provide/Inject (Dependency Injection)

```vue
<!-- Parent.vue -->
<script setup lang="ts">
import { ref, provide } from 'vue';
import type { InjectionKey } from 'vue';

interface Theme {
  primary: string;
  secondary: string;
}

// Create typed injection key
export const ThemeKey: InjectionKey<Theme> = Symbol('theme');

const theme = ref<Theme>({
  primary: '#007bff',
  secondary: '#6c757d'
});

// Provide to all descendants
provide(ThemeKey, theme.value);
provide('userPermissions', ['read', 'write']);
</script>

<!-- Child.vue (any depth) -->
<script setup lang="ts">
import { inject } from 'vue';
import { ThemeKey } from './Parent.vue';

// Inject with type safety
const theme = inject(ThemeKey);
const permissions = inject<string[]>('userPermissions', []);

// With default value
const config = inject('config', { debug: false });
</script>

<template>
  <div :style="{ color: theme?.primary }">
    Themed content
  </div>
</template>
```

## Vue Router Integration

### Basic Setup

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Home from '@/views/Home.vue';
import About from '@/views/About.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/user/:id',
    name: 'User',
    component: () => import('@/views/User.vue'), // Lazy loading
    props: true // Pass route params as props
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
```

### Navigation and Route Access

```vue
<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';

const router = useRouter();
const route = useRoute();

// Access route params
const userId = computed(() => route.params.id);
const querySearch = computed(() => route.query.search);

// Programmatic navigation
function goToUser(id: number) {
  router.push({ name: 'User', params: { id } });
}

function goToAbout() {
  router.push('/about');
}

function goBack() {
  router.back();
}

function replaceRoute() {
  router.replace({ name: 'Home' }); // No history entry
}
</script>

<template>
  <nav>
    <!-- Declarative navigation -->
    <RouterLink to="/">Home</RouterLink>
    <RouterLink :to="{ name: 'About' }">About</RouterLink>
    <RouterLink :to="{ name: 'User', params: { id: 123 } }">
      User 123
    </RouterLink>

    <!-- Active link styling -->
    <RouterLink
      to="/dashboard"
      active-class="active"
      exact-active-class="exact-active"
    >
      Dashboard
    </RouterLink>
  </nav>

  <button @click="goToUser(456)">Go to User 456</button>
  <button @click="goBack">Back</button>

  <p>Current user ID: {{ userId }}</p>
  <p>Search query: {{ querySearch }}</p>

  <!-- Render matched component -->
  <RouterView />
</template>
```

### Navigation Guards

```typescript
// router/index.ts
import { createRouter } from 'vue-router';

const router = createRouter({
  // ... routes
});

// Global before guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = checkAuth();

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else {
    next();
  }
});

// Global after hook
router.afterEach((to, from) => {
  document.title = `${to.meta.title || 'App'} - My App`;
});

// Per-route guard
const routes = [
  {
    path: '/admin',
    component: Admin,
    beforeEnter: (to, from, next) => {
      if (isAdmin()) {
        next();
      } else {
        next('/unauthorized');
      }
    }
  }
];
```

```vue
<!-- Component guard -->
<script setup lang="ts">
import { onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router';

// Confirm before leaving
onBeforeRouteLeave((to, from) => {
  if (hasUnsavedChanges.value) {
    const answer = window.confirm('You have unsaved changes. Leave anyway?');
    return answer;
  }
});

// React to route changes (same component, different params)
onBeforeRouteUpdate((to, from) => {
  console.log(`Route updated from ${from.params.id} to ${to.params.id}`);
  fetchData(to.params.id);
});
</script>
```

## Pinia State Management

### Store Definition

```typescript
// stores/counter.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// Composition API style (recommended)
export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0);
  const name = ref('Counter Store');

  // Getters (computed)
  const doubleCount = computed(() => count.value * 2);
  const isPositive = computed(() => count.value > 0);

  // Actions
  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  async function fetchCount() {
    const response = await fetch('/api/count');
    const data = await response.json();
    count.value = data.count;
  }

  return {
    count,
    name,
    doubleCount,
    isPositive,
    increment,
    decrement,
    fetchCount
  };
});

// Options API style (alternative)
export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: ''
  }),

  getters: {
    isLoggedIn: (state) => state.user !== null,
    fullName: (state) => state.user ? `${state.user.firstName} ${state.user.lastName}` : ''
  },

  actions: {
    async login(email: string, password: string) {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      this.user = data.user;
      this.token = data.token;
    },

    logout() {
      this.user = null;
      this.token = '';
    }
  }
});
```

### Using Stores in Components

```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter';
import { useUserStore } from '@/stores/user';
import { storeToRefs } from 'pinia';

const counterStore = useCounterStore();
const userStore = useUserStore();

// Get reactive refs from store
const { count, doubleCount } = storeToRefs(counterStore);
const { user, isLoggedIn } = storeToRefs(userStore);

// Actions can be destructured directly (they're not reactive)
const { increment, decrement } = counterStore;

// Access state directly
console.log(counterStore.count);

// Modify state directly
counterStore.count++;

// Or use $patch for multiple changes
counterStore.$patch({
  count: 10,
  name: 'Updated Counter'
});

// Reset state
counterStore.$reset();
</script>

<template>
  <div>
    <p>Count: {{ count }} (Double: {{ doubleCount }})</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>

    <div v-if="isLoggedIn">
      <p>Welcome, {{ user?.firstName }}!</p>
      <button @click="userStore.logout()">Logout</button>
    </div>
  </div>
</template>
```

### Store Composition (Accessing Other Stores)

```typescript
// stores/cart.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useUserStore } from './user';

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([]);
  const userStore = useUserStore();

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  const canCheckout = computed(() =>
    userStore.isLoggedIn && items.value.length > 0
  );

  async function checkout() {
    if (!canCheckout.value) return;

    await fetch('/api/checkout', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${userStore.token}`
      },
      body: JSON.stringify({ items: items.value })
    });

    items.value = [];
  }

  return { items, total, canCheckout, checkout };
});
```

## Composables (Reusable Logic)

### Custom Composables

```typescript
// composables/useFetch.ts
import { ref, type Ref } from 'vue';

interface UseFetchOptions {
  immediate?: boolean;
}

export function useFetch<T>(url: string, options: UseFetchOptions = {}) {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function execute() {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(response.statusText);
      data.value = await response.json();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  if (options.immediate) {
    execute();
  }

  return { data, error, loading, execute };
}

// composables/useLocalStorage.ts
import { ref, watch, type Ref } from 'vue';

export function useLocalStorage<T>(key: string, defaultValue: T): Ref<T> {
  const storedValue = localStorage.getItem(key);
  const data = ref<T>(
    storedValue ? JSON.parse(storedValue) : defaultValue
  ) as Ref<T>;

  watch(
    data,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue));
    },
    { deep: true }
  );

  return data;
}

// composables/useMouse.ts
import { ref, onMounted, onUnmounted } from 'vue';

export function useMouse() {
  const x = ref(0);
  const y = ref(0);

  function update(event: MouseEvent) {
    x.value = event.pageX;
    y.value = event.pageY;
  }

  onMounted(() => {
    window.addEventListener('mousemove', update);
  });

  onUnmounted(() => {
    window.removeEventListener('mousemove', update);
  });

  return { x, y };
}
```

### Using Composables

```vue
<script setup lang="ts">
import { useFetch } from '@/composables/useFetch';
import { useLocalStorage } from '@/composables/useLocalStorage';
import { useMouse } from '@/composables/useMouse';

interface User {
  id: number;
  name: string;
  email: string;
}

const { data: user, loading, error, execute } = useFetch<User>(
  '/api/user/123',
  { immediate: true }
);

const settings = useLocalStorage('app-settings', {
  theme: 'dark',
  language: 'en'
});

const { x, y } = useMouse();
</script>

<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <div v-else-if="user">
      <h1>{{ user.name }}</h1>
      <p>{{ user.email }}</p>
    </div>

    <p>Theme: {{ settings.theme }}</p>
    <button @click="settings.theme = settings.theme === 'dark' ? 'light' : 'dark'">
      Toggle Theme
    </button>

    <p>Mouse: {{ x }}, {{ y }}</p>
  </div>
</template>
```

## Testing with Vitest

### Component Testing

```typescript
// Counter.test.ts
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import Counter from '@/components/Counter.vue';

describe('Counter', () => {
  it('renders initial count', () => {
    const wrapper = mount(Counter);
    expect(wrapper.text()).toContain('Count: 0');
  });

  it('increments count on button click', async () => {
    const wrapper = mount(Counter);

    await wrapper.find('button').trigger('click');

    expect(wrapper.text()).toContain('Count: 1');
  });

  it('accepts initial count prop', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 10 }
    });

    expect(wrapper.text()).toContain('Count: 10');
  });

  it('emits update event', async () => {
    const wrapper = mount(Counter);

    await wrapper.find('button').trigger('click');

    expect(wrapper.emitted('update')).toBeTruthy();
    expect(wrapper.emitted('update')![0]).toEqual([1]);
  });
});
```

### Testing with Pinia

```typescript
// UserProfile.test.ts
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import { beforeEach, describe, it, expect } from 'vitest';
import UserProfile from '@/components/UserProfile.vue';
import { useUserStore } from '@/stores/user';

describe('UserProfile', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('displays user name when logged in', () => {
    const userStore = useUserStore();
    userStore.user = { id: 1, firstName: 'Alice', lastName: 'Smith' };

    const wrapper = mount(UserProfile);

    expect(wrapper.text()).toContain('Alice Smith');
  });

  it('shows login prompt when not logged in', () => {
    const wrapper = mount(UserProfile);
    expect(wrapper.text()).toContain('Please log in');
  });
});
```

## TypeScript Best Practices

### Component Props with Interface

```vue
<script setup lang="ts">
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

interface Props {
  user: User;
  showEmail?: boolean;
  onUpdate?: (user: User) => void;
}

const props = withDefaults(defineProps<Props>(), {
  showEmail: true
});

// Type-safe emits
const emit = defineEmits<{
  update: [user: User];
  delete: [userId: number];
}>();

function handleUpdate() {
  emit('update', props.user);
}
</script>
```

### Generic Components

```vue
<script setup lang="ts" generic="T">
interface Props<T> {
  items: T[];
  keyFn: (item: T) => string | number;
  renderItem: (item: T) => string;
}

const props = defineProps<Props<T>>();
</script>

<template>
  <ul>
    <li v-for="item in items" :key="keyFn(item)">
      {{ renderItem(item) }}
    </li>
  </ul>
</template>
```

## Performance Optimization

### Virtual Scrolling for Large Lists

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

const items = ref(Array.from({ length: 10000 }, (_, i) => ({
  id: i,
  text: `Item ${i}`
})));

const containerHeight = 400;
const itemHeight = 40;
const scrollTop = ref(0);

const visibleCount = Math.ceil(containerHeight / itemHeight);
const startIndex = computed(() => Math.floor(scrollTop.value / itemHeight));
const endIndex = computed(() => startIndex.value + visibleCount);
const visibleItems = computed(() =>
  items.value.slice(startIndex.value, endIndex.value)
);

const offsetY = computed(() => startIndex.value * itemHeight);
const totalHeight = computed(() => items.value.length * itemHeight);

function handleScroll(event: Event) {
  scrollTop.value = (event.target as HTMLElement).scrollTop;
}
</script>

<template>
  <div
    class="virtual-list"
    :style="{ height: containerHeight + 'px', overflow: 'auto' }"
    @scroll="handleScroll"
  >
    <div :style="{ height: totalHeight + 'px', position: 'relative' }">
      <div :style="{ transform: `translateY(${offsetY}px)` }">
        <div
          v-for="item in visibleItems"
          :key="item.id"
          :style="{ height: itemHeight + 'px' }"
        >
          {{ item.text }}
        </div>
      </div>
    </div>
  </div>
</template>
```

### Lazy Loading Components

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue';

// Lazy load heavy component
const HeavyComponent = defineAsyncComponent(() =>
  import('@/components/HeavyComponent.vue')
);

// With loading/error states
const AsyncComponent = defineAsyncComponent({
  loader: () => import('@/components/AsyncComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200, // Show loading after 200ms
  timeout: 3000 // Error if takes > 3s
});
</script>

<template>
  <Suspense>
    <template #default>
      <HeavyComponent />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>
```

## Migration Guide

### From Vue 2 to Vue 3

| Vue 2 | Vue 3 | Notes |
|-------|-------|-------|
| `data() { return {} }` | `ref()`, `reactive()` | Composition API |
| `computed: {}` | `computed(() => {})` | Function-based |
| `watch: {}` | `watch()`, `watchEffect()` | Explicit watchers |
| `mounted()` | `onMounted()` | Import from 'vue' |
| `this.$emit()` | `emit()` | defineEmits |
| `props: {}` | `defineProps<>()` | TypeScript support |
| Mixins | Composables | Better composition |
| `$listeners` | Merged into `$attrs` | Simplified |
| Filters | Functions or computed | Removed |

### From React to Vue 3

| React | Vue 3 | Notes |
|-------|-------|-------|
| `useState(0)` | `ref(0)` | Need .value in script |
| `useMemo(() => x * 2, [x])` | `computed(() => x.value * 2)` | Auto-tracked |
| `useEffect(() => {}, [x])` | `watch(x, () => {})` | Explicit deps |
| `useEffect(() => {}, [])` | `onMounted()` | Lifecycle |
| `useCallback` | Not needed | Auto-stable |
| `props.name` | `props.name` | Similar |
| `setState(prev => prev + 1)` | `count.value++` | Direct mutation |
| JSX | Template | HTML-like syntax |

## Best Practices

1. **Use Composition API over Options API** for better type inference and composition
2. **Prefer `ref()` for primitives, `reactive()` for objects** or just use `ref()` everywhere
3. **Use `computed()` for derived state** instead of methods
4. **Destructure props early** with `defineProps()` for type safety
5. **Use `<script setup>`** for less boilerplate and better performance
6. **Key your v-for loops** with unique IDs for proper reactivity
7. **Use Pinia over Vuex** for better TypeScript support and devtools
8. **Lazy load routes and heavy components** for faster initial load
9. **Use composables** to extract and reuse logic across components
10. **Enable Vue DevTools** for debugging reactivity and component tree

## Resources

- **Vue 3 Docs**: https://vuejs.org/guide/introduction.html
- **Vue Router**: https://router.vuejs.org/
- **Pinia**: https://pinia.vuejs.org/
- **Vite**: https://vitejs.dev/
- **Vue DevTools**: https://devtools.vuejs.org/
- **Awesome Vue**: https://github.com/vuejs/awesome-vue

## Summary

- **Vue 3** features Composition API with `setup()`, `ref()`, `reactive()`, `computed()`, `watch()`
- **Single-File Components** (.vue) combine template, script, and style
- **TypeScript** first-class support with `defineProps<>()` and `defineEmits<>()`
- **Vue Router** for client-side routing with lazy loading and guards
- **Pinia** modern state management with Composition API style
- **Vite** lightning-fast development with HMR
- **Composables** extract and reuse logic across components
- **Progressive** adopt incrementally from simple to complex
