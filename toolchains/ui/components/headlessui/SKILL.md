---
name: headlessui
description: Headless UI - Unstyled, fully accessible UI components for React and Vue with built-in ARIA patterns
version: 1.0.0
category: universal
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Unstyled accessible UI primitives: Menu, Dialog, Popover, Listbox, Combobox - zero runtime CSS, full keyboard/screen reader support"
    when_to_use: "Building custom-styled components with accessibility requirements, Tailwind CSS integration, need ARIA-compliant primitives without opinionated styling"
    quick_start: "1. Install @headlessui/react or @headlessui/vue 2. Import components 3. Style with Tailwind/CSS 4. Use render props for custom logic"
context_limit: 700
tags:
  - headlessui
  - react
  - vue
  - accessibility
  - unstyled
  - primitives
  - aria
  - tailwind
requires_tools: []
---

# Headless UI - Accessible Component Primitives

## Overview

Headless UI provides completely unstyled, fully accessible UI components designed to integrate beautifully with Tailwind CSS. Built by the Tailwind Labs team, it offers production-ready accessibility without imposing design decisions.

**Key Features**:
- Fully unstyled - bring your own styles
- Complete keyboard navigation
- Screen reader tested
- Focus management
- ARIA attributes handled automatically
- TypeScript support
- React 18 and Vue 3 compatible
- SSR compatible
- Render props for maximum flexibility

**Installation**:
```bash
# React
npm install @headlessui/react

# Vue
npm install @headlessui/vue
```

## Component Catalog

### Menu (Dropdown)

Accessible dropdown menus with keyboard navigation and ARIA support.

```tsx
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/20/solid'

function DropdownMenu() {
  return (
    <Menu>
      <MenuButton className="inline-flex items-center gap-2 rounded-md bg-gray-800 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-700 data-[open]:bg-gray-700 data-[focus]:outline-1 data-[focus]:outline-white">
        Options
        <ChevronDownIcon className="size-4 fill-white/60" />
      </MenuButton>

      <MenuItems
        transition
        anchor="bottom end"
        className="w-52 origin-top-right rounded-xl border border-white/5 bg-white/5 p-1 text-sm/6 text-white transition duration-100 ease-out [--anchor-gap:var(--spacing-1)] focus:outline-none data-[closed]:scale-95 data-[closed]:opacity-0"
      >
        <MenuItem>
          <button className="group flex w-full items-center gap-2 rounded-lg py-1.5 px-3 data-[focus]:bg-white/10">
            Edit
          </button>
        </MenuItem>
        <MenuItem>
          <button className="group flex w-full items-center gap-2 rounded-lg py-1.5 px-3 data-[focus]:bg-white/10">
            Duplicate
          </button>
        </MenuItem>
        <div className="my-1 h-px bg-white/5" />
        <MenuItem>
          <button className="group flex w-full items-center gap-2 rounded-lg py-1.5 px-3 data-[focus]:bg-white/10">
            Delete
          </button>
        </MenuItem>
      </MenuItems>
    </Menu>
  )
}
```

**Menu Features**:
- Arrow key navigation
- Type-ahead search
- Automatic focus management
- Escape to close
- Click outside to close
- Portal rendering for positioning
- Anchor positioning API

### Listbox (Select)

Custom select/dropdown component with full keyboard support.

```tsx
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/react'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Wade Cooper' },
  { id: 2, name: 'Arlene Mccoy' },
  { id: 3, name: 'Devon Webb' },
]

function SelectExample() {
  const [selected, setSelected] = useState(people[0])

  return (
    <Listbox value={selected} onChange={setSelected}>
      <ListboxButton className="relative w-full cursor-default rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm">
        <span className="block truncate">{selected.name}</span>
        <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>

      <ListboxOptions className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm">
        {people.map((person) => (
          <ListboxOption
            key={person.id}
            value={person}
            className="relative cursor-default select-none py-2 pl-10 pr-4 data-[focus]:bg-amber-100 data-[focus]:text-amber-900"
          >
            {({ selected }) => (
              <>
                <span className={`block truncate ${selected ? 'font-medium' : 'font-normal'}`}>
                  {person.name}
                </span>
                {selected && (
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600">
                    <CheckIcon className="h-5 w-5" aria-hidden="true" />
                  </span>
                )}
              </>
            )}
          </ListboxOption>
        ))}
      </ListboxOptions>
    </Listbox>
  )
}
```

**Listbox Features**:
- Single and multiple selection modes
- Type-ahead search
- Arrow key navigation
- Controlled and uncontrolled modes
- Disabled options support
- Custom value comparison

### Combobox (Autocomplete)

Searchable select component with filtering.

```tsx
import { Combobox, ComboboxInput, ComboboxOptions, ComboboxOption } from '@headlessui/react'
import { useState } from 'react'

const people = [
  { id: 1, name: 'Wade Cooper' },
  { id: 2, name: 'Arlene Mccoy' },
  { id: 3, name: 'Devon Webb' },
  { id: 4, name: 'Tom Cook' },
]

function AutocompleteExample() {
  const [selected, setSelected] = useState(people[0])
  const [query, setQuery] = useState('')

  const filtered =
    query === ''
      ? people
      : people.filter((person) =>
          person.name.toLowerCase().includes(query.toLowerCase())
        )

  return (
    <Combobox value={selected} onChange={setSelected}>
      <ComboboxInput
        className="w-full rounded-lg border-none bg-white/5 py-1.5 pr-8 pl-3 text-sm/6 text-white focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25"
        displayValue={(person) => person?.name}
        onChange={(event) => setQuery(event.target.value)}
      />

      <ComboboxOptions className="w-[var(--input-width)] rounded-xl border border-white/5 bg-white/5 p-1 [--anchor-gap:var(--spacing-1)] empty:invisible">
        {filtered.map((person) => (
          <ComboboxOption
            key={person.id}
            value={person}
            className="group flex cursor-default items-center gap-2 rounded-lg py-1.5 px-3 select-none data-[focus]:bg-white/10"
          >
            <CheckIcon className="invisible size-4 fill-white group-data-[selected]:visible" />
            <div className="text-sm/6 text-white">{person.name}</div>
          </ComboboxOption>
        ))}
      </ComboboxOptions>
    </Combobox>
  )
}
```

**Combobox Features**:
- Text input with filtering
- Keyboard navigation
- Nullable/optional selections
- Custom display values
- Async data loading support
- Multiple selection mode

### Dialog (Modal)

Accessible modal dialogs with focus trapping.

```tsx
import { Dialog, DialogPanel, DialogTitle, Transition, TransitionChild } from '@headlessui/react'
import { Fragment, useState } from 'react'

function ModalExample() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open dialog</button>

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={() => setIsOpen(false)}>
          <TransitionChild
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black/25" />
          </TransitionChild>

          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <TransitionChild
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <DialogPanel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <DialogTitle className="text-lg font-medium leading-6 text-gray-900">
                    Payment successful
                  </DialogTitle>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">
                      Your payment has been successfully submitted.
                    </p>
                  </div>

                  <div className="mt-4">
                    <button
                      type="button"
                      className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                      onClick={() => setIsOpen(false)}
                    >
                      Got it, thanks!
                    </button>
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  )
}
```

**Dialog Features**:
- Focus trapping
- Escape to close
- Scroll locking
- Return focus on close
- Portal rendering
- Nested dialogs support
- Initial focus control

### Popover

Floating panels for tooltips, dropdowns, and more.

```tsx
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react'

function PopoverExample() {
  return (
    <Popover className="relative">
      <PopoverButton className="inline-flex items-center gap-2 rounded-md bg-gray-800 py-1.5 px-3 text-sm/6 font-semibold text-white shadow-inner shadow-white/10 focus:outline-none data-[hover]:bg-gray-700 data-[focus]:outline-1 data-[focus]:outline-white">
        Solutions
      </PopoverButton>

      <PopoverPanel
        transition
        anchor="bottom"
        className="divide-y divide-white/5 rounded-xl bg-white/5 text-sm/6 transition duration-200 ease-in-out [--anchor-gap:var(--spacing-5)] data-[closed]:-translate-y-1 data-[closed]:opacity-0"
      >
        <div className="p-3">
          <a className="block rounded-lg py-2 px-3 transition hover:bg-white/5" href="#">
            <p className="font-semibold text-white">Insights</p>
            <p className="text-white/50">Measure actions your users take</p>
          </a>
          <a className="block rounded-lg py-2 px-3 transition hover:bg-white/5" href="#">
            <p className="font-semibold text-white">Automations</p>
            <p className="text-white/50">Create your own targeted content</p>
          </a>
        </div>
      </PopoverPanel>
    </Popover>
  )
}
```

**Popover Features**:
- Anchor positioning
- Click or hover triggers
- Close on click outside
- Nested popovers
- Focus management
- Portal rendering

### RadioGroup

Accessible radio button groups.

```tsx
import { RadioGroup, RadioGroupOption, RadioGroupLabel } from '@headlessui/react'
import { useState } from 'react'

const plans = [
  { name: 'Startup', ram: '12GB', cpus: '6 CPUs', disk: '160 GB SSD disk' },
  { name: 'Business', ram: '16GB', cpus: '8 CPUs', disk: '512 GB SSD disk' },
  { name: 'Enterprise', ram: '32GB', cpus: '12 CPUs', disk: '1024 GB SSD disk' },
]

function RadioExample() {
  const [selected, setSelected] = useState(plans[0])

  return (
    <RadioGroup value={selected} onChange={setSelected}>
      <RadioGroupLabel className="sr-only">Server size</RadioGroupLabel>
      <div className="space-y-2">
        {plans.map((plan) => (
          <RadioGroupOption
            key={plan.name}
            value={plan}
            className="relative block cursor-pointer rounded-lg bg-white px-6 py-4 shadow-md focus:outline-none data-[focus]:outline-2 data-[focus]:outline-white/75 data-[checked]:bg-sky-900/75"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="text-sm">
                  <RadioGroupLabel as="p" className="font-medium text-white">
                    {plan.name}
                  </RadioGroupLabel>
                  <div className="flex gap-2 text-white/50">
                    <div>{plan.ram}</div>
                    <div aria-hidden="true">&middot;</div>
                    <div>{plan.cpus}</div>
                    <div aria-hidden="true">&middot;</div>
                    <div>{plan.disk}</div>
                  </div>
                </div>
              </div>
            </div>
          </RadioGroupOption>
        ))}
      </div>
    </RadioGroup>
  )
}
```

**RadioGroup Features**:
- Arrow key navigation
- Disabled options
- Custom styling states
- Controlled mode
- Description support

### Switch (Toggle)

Accessible toggle switches.

```tsx
import { Switch } from '@headlessui/react'
import { useState } from 'react'

function SwitchExample() {
  const [enabled, setEnabled] = useState(false)

  return (
    <Switch
      checked={enabled}
      onChange={setEnabled}
      className="group inline-flex h-6 w-11 items-center rounded-full bg-gray-200 transition data-[checked]:bg-blue-600"
    >
      <span className="size-4 translate-x-1 rounded-full bg-white transition group-data-[checked]:translate-x-6" />
    </Switch>
  )
}
```

**Switch Features**:
- Controlled and uncontrolled
- Label support
- Description support
- Disabled state
- Keyboard accessible (Space to toggle)

### Tab (Tabs)

Accessible tab navigation.

```tsx
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from '@headlessui/react'

function TabExample() {
  const categories = [
    {
      name: 'Recent',
      posts: [
        { id: 1, title: 'Does drinking coffee make you smarter?' },
        { id: 2, title: "So you've bought coffee... now what?" },
      ],
    },
    {
      name: 'Popular',
      posts: [
        { id: 1, title: 'Is tech making coffee better or worse?' },
        { id: 2, title: 'The most innovative things happening in coffee' },
      ],
    },
  ]

  return (
    <TabGroup>
      <TabList className="flex space-x-1 rounded-xl bg-blue-900/20 p-1">
        {categories.map((category) => (
          <Tab
            key={category.name}
            className="w-full rounded-lg py-2.5 text-sm font-medium leading-5 text-blue-700 ring-white/60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 data-[selected]:bg-white data-[selected]:shadow data-[hover]:bg-white/[0.12] data-[focus]:outline-1"
          >
            {category.name}
          </Tab>
        ))}
      </TabList>
      <TabPanels className="mt-2">
        {categories.map((category, idx) => (
          <TabPanel
            key={idx}
            className="rounded-xl bg-white p-3 ring-white/60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"
          >
            <ul>
              {category.posts.map((post) => (
                <li key={post.id} className="relative rounded-md p-3 hover:bg-gray-100">
                  <h3 className="text-sm font-medium leading-5">{post.title}</h3>
                </li>
              ))}
            </ul>
          </TabPanel>
        ))}
      </TabPanels>
    </TabGroup>
  )
}
```

**Tab Features**:
- Arrow key navigation
- Default selected tab
- Manual activation
- Vertical/horizontal orientation
- Controlled mode

### Disclosure (Accordion)

Expandable content sections.

```tsx
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/react'
import { ChevronUpIcon } from '@heroicons/react/20/solid'

function DisclosureExample() {
  return (
    <Disclosure>
      {({ open }) => (
        <>
          <DisclosureButton className="flex w-full justify-between rounded-lg bg-purple-100 px-4 py-2 text-left text-sm font-medium text-purple-900 hover:bg-purple-200 focus:outline-none focus-visible:ring focus-visible:ring-purple-500/75">
            <span>What is your refund policy?</span>
            <ChevronUpIcon
              className={`${open ? 'rotate-180 transform' : ''} h-5 w-5 text-purple-500`}
            />
          </DisclosureButton>
          <DisclosurePanel className="px-4 pb-2 pt-4 text-sm text-gray-500">
            If you're unhappy with your purchase for any reason, email us within 90 days and we'll refund you in full, no questions asked.
          </DisclosurePanel>
        </>
      )}
    </Disclosure>
  )
}
```

**Disclosure Features**:
- Controlled and uncontrolled
- Default open state
- Render props for state access
- Multiple disclosures (accordion pattern)
- Smooth animations with Transition

### Transition

Animation component for enter/leave transitions.

```tsx
import { Transition } from '@headlessui/react'
import { useState } from 'react'

function TransitionExample() {
  const [isShowing, setIsShowing] = useState(false)

  return (
    <>
      <button onClick={() => setIsShowing(!isShowing)}>Toggle</button>
      <Transition
        show={isShowing}
        enter="transition-opacity duration-300"
        enterFrom="opacity-0"
        enterTo="opacity-100"
        leave="transition-opacity duration-200"
        leaveFrom="opacity-100"
        leaveTo="opacity-0"
      >
        <div className="rounded-md bg-blue-500 p-4 text-white">
          I will fade in and out
        </div>
      </Transition>
    </>
  )
}
```

**Transition Features**:
- CSS class-based transitions
- Enter/leave lifecycle
- Nested transitions (child coordination)
- Appears support (initial mount animation)
- Works with React 18 concurrent mode

## Advanced Patterns

### Render Props Pattern

Access component state for custom rendering.

```tsx
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/react'

function RenderPropsExample() {
  return (
    <Listbox value={selected} onChange={setSelected}>
      {({ open }) => (
        <>
          <ListboxButton>
            Options {open ? '▲' : '▼'}
          </ListboxButton>
          <ListboxOptions>
            <ListboxOption value="a">
              {({ selected, focus }) => (
                <div className={focus ? 'bg-blue-500' : ''}>
                  {selected && '✓'} Option A
                </div>
              )}
            </ListboxOption>
          </ListboxOptions>
        </>
      )}
    </Listbox>
  )
}
```

### Controlled Components

Full control over component state.

```tsx
import { Tab, TabGroup, TabList, TabPanel, TabPanels } from '@headlessui/react'
import { useState } from 'react'

function ControlledTabs() {
  const [selectedIndex, setSelectedIndex] = useState(0)

  return (
    <TabGroup selectedIndex={selectedIndex} onChange={setSelectedIndex}>
      <TabList>
        <Tab>Tab 1</Tab>
        <Tab>Tab 2</Tab>
        <Tab>Tab 3</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>Content 1</TabPanel>
        <TabPanel>Content 2</TabPanel>
        <TabPanel>Content 3</TabPanel>
      </TabPanels>
      <button onClick={() => setSelectedIndex(0)}>Reset to first tab</button>
    </TabGroup>
  )
}
```

### Portal Rendering

Render components outside DOM hierarchy.

```tsx
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react'
import { createPortal } from 'react-dom'

function PortalMenu() {
  return (
    <Menu>
      <MenuButton>Options</MenuButton>
      {createPortal(
        <MenuItems>
          <MenuItem>
            <button>Edit</button>
          </MenuItem>
          <MenuItem>
            <button>Delete</button>
          </MenuItem>
        </MenuItems>,
        document.body
      )}
    </Menu>
  )
}
```

### Form Integration

Use with form libraries like React Hook Form.

```tsx
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/react'
import { useForm, Controller } from 'react-hook-form'

function FormExample() {
  const { control, handleSubmit } = useForm()

  const onSubmit = (data) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Controller
        name="country"
        control={control}
        rules={{ required: true }}
        render={({ field }) => (
          <Listbox {...field}>
            <ListboxButton>Select country</ListboxButton>
            <ListboxOptions>
              <ListboxOption value="us">United States</ListboxOption>
              <ListboxOption value="ca">Canada</ListboxOption>
              <ListboxOption value="mx">Mexico</ListboxOption>
            </ListboxOptions>
          </Listbox>
        )}
      />
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Vue Support

Headless UI works identically in Vue 3.

```vue
<script setup>
import { ref } from 'vue'
import {
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from '@headlessui/vue'

const people = [
  { id: 1, name: 'Wade Cooper' },
  { id: 2, name: 'Arlene Mccoy' },
  { id: 3, name: 'Devon Webb' },
]

const selectedPerson = ref(people[0])
</script>

<template>
  <Listbox v-model="selectedPerson">
    <ListboxButton>{{ selectedPerson.name }}</ListboxButton>
    <ListboxOptions>
      <ListboxOption
        v-for="person in people"
        :key="person.id"
        :value="person"
        v-slot="{ active, selected }"
      >
        <li :class="{ 'bg-blue-500': active }">
          {{ selected ? '✓' : '' }} {{ person.name }}
        </li>
      </ListboxOption>
    </ListboxOptions>
  </Listbox>
</template>
```

## TypeScript Support

Full type safety with TypeScript.

```tsx
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react'

interface User {
  id: number
  name: string
  role: 'admin' | 'user'
}

interface UserMenuProps {
  user: User
  onEdit: (user: User) => void
  onDelete: (userId: number) => void
}

function UserMenu({ user, onEdit, onDelete }: UserMenuProps) {
  return (
    <Menu as="div" className="relative">
      <MenuButton className="btn">{user.name}</MenuButton>
      <MenuItems className="menu">
        <MenuItem>
          {({ focus }) => (
            <button
              className={focus ? 'bg-blue-500' : ''}
              onClick={() => onEdit(user)}
            >
              Edit
            </button>
          )}
        </MenuItem>
        <MenuItem>
          {({ focus }) => (
            <button
              className={focus ? 'bg-red-500' : ''}
              onClick={() => onDelete(user.id)}
            >
              Delete
            </button>
          )}
        </MenuItem>
      </MenuItems>
    </Menu>
  )
}
```

## Tailwind CSS Integration

Headless UI is designed for Tailwind CSS.

### Data Attributes for States

Headless UI v2 uses data attributes for state styling.

```tsx
// Modern approach with data attributes
<MenuButton className="data-[active]:bg-blue-500 data-[disabled]:opacity-50">
  Options
</MenuButton>

// Available states
// data-[active] - Element is active/focused
// data-[selected] - Element is selected
// data-[disabled] - Element is disabled
// data-[open] - Element/panel is open
// data-[focus] - Element has focus
// data-[checked] - Element is checked (Switch)
```

### Tailwind Plugin

Configure Tailwind for Headless UI states.

```js
// tailwind.config.js
module.exports = {
  plugins: [
    require('@headlessui/tailwindcss')
  ]
}
```

Now use modifiers:

```tsx
<MenuButton className="ui-active:bg-blue-500 ui-disabled:opacity-50">
  Options
</MenuButton>
```

## Accessibility Features

### ARIA Attributes

All ARIA attributes managed automatically:

- `aria-expanded` on disclosure buttons
- `aria-selected` on tab/option elements
- `aria-checked` on switches
- `aria-labelledby` for associations
- `aria-describedby` for descriptions
- `role` attributes (menu, listbox, dialog, etc.)

### Keyboard Navigation

Full keyboard support built-in:

- **Arrow keys**: Navigate options/tabs
- **Enter/Space**: Select/activate
- **Escape**: Close menus/dialogs
- **Tab**: Focus management
- **Home/End**: First/last item (where applicable)
- **Type-ahead**: Search by typing

### Focus Management

Automatic focus handling:

- Return focus on close (Dialog, Menu, Popover)
- Focus trap in modals
- Initial focus control
- Skip to focused element on open

### Screen Reader Support

Tested with:
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (macOS, iOS)
- TalkBack (Android)

## Server-Side Rendering

Fully compatible with Next.js, Remix, and other SSR frameworks.

```tsx
// app/page.tsx (Next.js 13+)
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react'

export default function Page() {
  return (
    <Menu>
      <MenuButton>Options</MenuButton>
      <MenuItems>
        <MenuItem>
          <button>Edit</button>
        </MenuItem>
      </MenuItems>
    </Menu>
  )
}
```

No special configuration needed - components work identically on server and client.

## Best Practices

1. **Always provide labels** - Use sr-only classes for hidden labels
2. **Style all states** - Use data attributes for active, selected, disabled states
3. **Test keyboard navigation** - Verify Tab, arrows, Enter, Escape work
4. **Use semantic HTML** - Let components render as appropriate elements
5. **Provide focus indicators** - Always show focus states for keyboard users
6. **Test with screen readers** - Verify announcements are correct
7. **Handle loading states** - Show appropriate UI during async operations
8. **Use controlled mode when needed** - For complex state management
9. **Combine with Transition** - Add smooth animations to open/close
10. **Portal overlays** - Use portals for menus/dialogs to avoid z-index issues

## Common Pitfalls

❌ **Missing Tailwind classes for states**:
```tsx
// WRONG - no visual feedback
<MenuButton>Options</MenuButton>

// CORRECT
<MenuButton className="data-[active]:bg-blue-500 data-[open]:bg-blue-600">
  Options
</MenuButton>
```

❌ **Not using Fragment for render props**:
```tsx
// WRONG - adds extra div
<Transition show={isOpen}>
  <div>Content</div>
</Transition>

// CORRECT
<Transition show={isOpen} as={Fragment}>
  <div>Content</div>
</Transition>
```

❌ **Forgetting to handle controlled state**:
```tsx
// WRONG - onChange does nothing
<Listbox value={selected}>
  <ListboxOptions>...</ListboxOptions>
</Listbox>

// CORRECT
<Listbox value={selected} onChange={setSelected}>
  <ListboxOptions>...</ListboxOptions>
</Listbox>
```

## Resources

- **Documentation**: https://headlessui.com
- **GitHub**: https://github.com/tailwindlabs/headlessui
- **Examples**: https://headlessui.com/react/menu#examples
- **Tailwind UI**: Premium components built with Headless UI

## Summary

- **Headless UI** provides unstyled, accessible component primitives
- **Zero runtime CSS** - bring your own styles with Tailwind or custom CSS
- **Full accessibility** - ARIA, keyboard navigation, screen reader support built-in
- **React and Vue** - Identical APIs for both frameworks
- **TypeScript** - Complete type definitions included
- **Render props** - Access component state for custom rendering
- **SSR compatible** - Works with Next.js, Remix, Nuxt
- **Perfect for** - Custom design systems, Tailwind CSS integration, accessible components
