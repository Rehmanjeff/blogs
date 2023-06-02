<template>
  <div>
    <TransitionRoot as="template" :show="sidebarOpen">
      <Dialog as="div" class="relative z-50 lg:hidden" @close="sidebarOpen = false">
        <TransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-gray-900/80" />
        </TransitionChild>

        <div class="fixed inset-0 flex">
          <TransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="-translate-x-full">
            <DialogPanel class="relative flex flex-1 w-full max-w-xs mr-16">
              <TransitionChild as="template" enter="ease-in-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-300" leave-from="opacity-100" leave-to="opacity-0">
                <div class="absolute top-0 flex justify-center w-16 pt-5 left-full">
                  <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                    <span class="sr-only">Close sidebar</span>
                    <XMarkIcon class="w-6 h-6 text-white" aria-hidden="true" />
                  </button>
                </div>
              </TransitionChild>
              <!-- Sidebar component, swap this element with another sidebar if you like -->
              <div class="flex flex-col px-6 pb-4 overflow-y-auto bg-gray-900 grow gap-y-5 ring-1 ring-white/10">
                <div class="flex items-center h-16 shrink-0">
                  <img class="w-auto h-8" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500" alt="Your Company" />
                </div>
                <nav class="flex flex-col flex-1">
                  <div v-for="item in navigation" :key="item.name">
                      <Disclosure v-if="!item.children" as="div" class="space-y-1">
                          <DisclosureButton classes="nav-item" :class="[item.href == $route.path ? 'bg-gray-200 text-gray-900' : 'hover:bg-gray-700 hover:text-white text-gray-300']" class="flex items-center w-full p-2 text-sm text-left rounded-md group focus:outline-none">
                              <component :is="item.icon" :class="[item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-300', 'mr-3 flex-shrink-0 h-6 w-6']" aria-hidden="true" />
                              <RouterLink :to="item.href" class="flex-1">
                                  {{ item.name }}
                              </RouterLink>
                          </DisclosureButton>
                      </Disclosure>
                      <Disclosure v-else as="div" class="space-y-1" v-slot="{ open }">
                          <DisclosureButton classes="nav-item nav-item-dropdown" :is-dropdown-active="item.hrefs.includes($route.path)" class="flex items-center w-full p-2 text-sm text-left text-gray-300 rounded-md hover:bg-gray-700 hover:text-white group focus:outline-none">
                              <component :is="item.icon" :class="[item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-300', 'mr-3 flex-shrink-0 h-6 w-6']" aria-hidden="true" />
                              <span class="flex-1">
                                  {{ item.name }}
                              </span>
                              <svg :class="[open ? 'rotate-90' : '', 'ml-3 flex-shrink-0 h-5 w-5 transform text-gray-400 group-hover:text-gray-300 transition-colors ease-in-out duration-150']" viewBox="0 0 20 20" aria-hidden="true">
                                  <path d="M6 6L14 10L6 14V6Z" fill="currentColor" />
                              </svg>
                          </DisclosureButton>
                          <DisclosurePanel class="space-y-1">
                              <DisclosureButton v-for="subItem in item.children" :key="subItem.name" as="div">
                                  <RouterLink :to="subItem.href" :class="[subItem.href == $route.path ? 'bg-gray-200 text-gray-900' : 'hover:bg-gray-700 hover:text-white text-gray-300']" class="flex items-center w-full py-2 pr-2 text-sm rounded-md group pl-11">
                                      {{ subItem.name }}
                                  </RouterLink>
                              </DisclosureButton>
                          </DisclosurePanel>
                      </Disclosure>
                  </div>
                </nav>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Static sidebar for desktop -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
      <!-- Sidebar component, swap this element with another sidebar if you like -->
      <div class="flex flex-col px-6 pb-4 overflow-y-auto bg-gray-900 grow gap-y-5">
        <div class="flex items-center h-16 shrink-0">
          <img class="w-auto h-8" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=500" alt="Your Company" />
        </div>
        <nav class="flex flex-col flex-1">
          <div v-for="item in navigation" :key="item.name">
              <Disclosure v-if="!item.children" as="div" class="space-y-1">
                  <DisclosureButton classes="nav-item" :class="[item.href == $route.path ? 'bg-gray-200 text-gray-900' : 'hover:bg-gray-700 hover:text-white text-gray-300']" class="flex items-center w-full p-2 text-sm text-left rounded-md group focus:outline-none">
                      <component :is="item.icon" :class="[item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-300', 'mr-3 flex-shrink-0 h-6 w-6']" aria-hidden="true" />
                      <RouterLink :to="item.href" class="flex-1">
                          {{ item.name }}
                      </RouterLink>
                  </DisclosureButton>
              </Disclosure>
              <Disclosure v-else as="div" class="space-y-1" v-slot="{ open }">
                  <DisclosureButton classes="nav-item nav-item-dropdown" :is-dropdown-active="item.hrefs.includes($route.path)" class="flex items-center w-full p-2 text-sm text-left text-gray-300 rounded-md hover:bg-gray-700 hover:text-white group focus:outline-none">
                      <component :is="item.icon" :class="[item.current ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-300', 'mr-3 flex-shrink-0 h-6 w-6']" aria-hidden="true" />
                      <span class="flex-1">
                          {{ item.name }}
                      </span>
                      <svg :class="[open ? 'rotate-90' : '', 'ml-3 flex-shrink-0 h-5 w-5 transform text-gray-400 group-hover:text-gray-300 transition-colors ease-in-out duration-150']" viewBox="0 0 20 20" aria-hidden="true">
                          <path d="M6 6L14 10L6 14V6Z" fill="currentColor" />
                      </svg>
                  </DisclosureButton>
                  <DisclosurePanel class="space-y-1">
                      <DisclosureButton v-for="subItem in item.children" :key="subItem.name" as="div">
                          <RouterLink :to="subItem.href" :class="[subItem.href == $route.path ? 'bg-gray-200 text-gray-900' : 'hover:bg-gray-700 hover:text-white text-gray-300']" class="flex items-center w-full py-2 pr-2 text-sm rounded-md group pl-11">
                              {{ subItem.name }}
                          </RouterLink>
                      </DisclosureButton>
                  </DisclosurePanel>
              </Disclosure>
          </div>
        </nav>
      </div>
    </div>

    <div class="lg:pl-72">
      <div class="sticky top-0 z-10 flex items-center h-16 px-4 bg-white border-b border-gray-200 shadow-sm shrink-0 gap-x-4 sm:gap-x-6 sm:px-6 lg:px-8">
        <button type="button" class="-m-2.5 p-2.5 text-gray-700 lg:hidden" @click="sidebarOpen = true">
          <span class="sr-only">Open sidebar</span>
          <Bars3Icon class="w-6 h-6" aria-hidden="true" />
        </button>

        <!-- Separator -->
        <div class="w-px h-6 bg-gray-900/10 lg:hidden" aria-hidden="true" />

        <div class="flex self-stretch flex-1 gap-x-4 lg:gap-x-6">
          <form class="relative flex flex-1" action="#" method="GET">
            <label for="search-field" class="sr-only">Search</label>
            <MagnifyingGlassIcon class="absolute inset-y-0 left-0 w-5 h-full text-gray-400 pointer-events-none" aria-hidden="true" />
            <input id="search-field" class="block w-full h-full py-0 pl-8 pr-0 text-gray-900 border-0 placeholder:text-gray-400 focus:ring-0 sm:text-sm" placeholder="Search..." type="search" name="search" />
          </form>
          <div class="flex items-center gap-x-4 lg:gap-x-6">
            <button type="button" class="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
              <span class="sr-only">View notifications</span>
              <BellIcon class="w-6 h-6" aria-hidden="true" />
            </button>

            <!-- Separator -->
            <div class="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10" aria-hidden="true" />

            <!-- Profile dropdown -->
            <Menu as="div" class="relative">
              <MenuButton class="-m-1.5 flex items-center p-1.5">
                <span class="sr-only">Open user menu</span>
                <img class="w-8 h-8 rounded-full bg-gray-50" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
                <span class="hidden lg:flex lg:items-center">
                  <span class="ml-4 text-sm font-semibold leading-6 text-gray-900" aria-hidden="true">Tom Cook</span>
                  <ChevronDownIcon class="w-5 h-5 ml-2 text-gray-400" aria-hidden="true" />
                </span>
              </MenuButton>
              <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
                <MenuItems class="absolute right-0 z-10 mt-2.5 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                  <MenuItem v-for="item in userNavigation" :key="item.name" v-slot="{ active }">
                    <a :href="item.href" :class="[active ? 'bg-gray-50' : '', 'block px-3 py-1 text-sm leading-6 text-gray-900']">{{ item.name }}</a>
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>

      <main class="flex flex-col flex-1 min-h-screen bg-gray-100">
        <div class="px-4 sm:px-6 lg:px-8">
          <slot></slot>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, DialogPanel,  Menu, MenuButton, MenuItem,  MenuItems, TransitionChild,  TransitionRoot } from '@headlessui/vue'
import { Bars3Icon, BellIcon, CalendarIcon, ChartPieIcon, Cog6ToothIcon, DocumentDuplicateIcon, FolderIcon, HomeIcon, UsersIcon, XMarkIcon } from '@heroicons/vue/24/outline'
import { ChevronDownIcon, MagnifyingGlassIcon } from '@heroicons/vue/20/solid'
import { Disclosure, DisclosureButton, DisclosurePanel } from '@headlessui/vue'

const navigation = [
  { name: 'Dashboard', href: '/admin', icon: HomeIcon, current: true },
  {
    name: 'Blogs',
    icon: UsersIcon,
    current: false,
    hrefs:[
        '/admin/blogs',
        '/admin/blogs/create',
    ],
    children: [
        { name: 'List', href: '/admin/blogs/list'},
        { name: 'Add', href: '/admin/blogs/create'},
    ],
  },
  {
    name: 'Categories',
    icon: UsersIcon,
    current: false,
    hrefs:[
        '/admin/categories'
    ],
    children: [
        { name: 'List', href: '/admin/categories/list'}
    ],
  },
  {
    name: 'Authors',
    icon: UsersIcon,
    current: false,
    hrefs:[
        '/admin/authors'
    ],
    children: [
        { name: 'List', href: '/admin/authors/list'}
    ],
  },
]
const teams = [
  { id: 1, name: 'Heroicons', href: '#', initial: 'H', current: false },
  { id: 2, name: 'Tailwind Labs', href: '#', initial: 'T', current: false },
  { id: 3, name: 'Workcation', href: '#', initial: 'W', current: false },
]
const userNavigation = [
  { name: 'Your profile', href: '#' },
  { name: 'Sign out', href: '#' },
]

const sidebarOpen = ref(false)

</script>