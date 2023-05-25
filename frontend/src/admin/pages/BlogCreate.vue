<template>
  <div class="pb-6">
      <div class="lg:grid lg:grid-cols-5">
          <div class="md:col-span-1">
              <aside aria-label="Sidebar">
                  <div class="overflow-y-auto py-4 px-3 rounded">
                      <ul class="space-y-1">
                          <li>
                              <a href="#" @click.prevent="toggleTab(1)" :class="[(currentTab == 1 ? 'bg-gray-200 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'), 'group flex items-center px-3 py-2 text-sm font-medium rounded-md']">
                                  <span class="ml-3 flex items-center">
                                      <FingerPrintIcon :class="[currentTab == 1 ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-500', 'flex-shrink-0 -ml-1 mr-3 h-6 w-6']" aria-hidden="true" />
                                      <span class="truncate">Manual</span>
                                  </span>
                              </a>
                          </li>
                          <li>
                            <a href="#" @click.prevent="toggleTab(2)" :class="[(currentTab == 2 ? 'bg-gray-200 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'), 'group flex items-center px-3 py-2 text-sm font-medium rounded-md']">
                                  <span class="ml-3 flex items-center">
                                      <LinkIcon :class="[currentTab == 2 ? 'text-gray-500' : 'text-gray-400 group-hover:text-gray-500', 'flex-shrink-0 -ml-1 mr-3 h-6 w-6']" aria-hidden="true" />
                                      <span class="truncate">Link</span>
                                  </span>
                              </a>
                          </li>
                      </ul>
                  </div>
              </aside>
          </div>

          <div class="mt-5 md:col-span-4" v-if="currentTab == 1">
            <BlogManualForm></BlogManualForm>
          </div>
          <div class="mt-5 md:col-span-4" v-if="currentTab == 2">
            <BlogLinkForm></BlogLinkForm>
          </div>
      </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BlogManualForm from '@/admin/components/blog/manualForm.vue'
import BlogLinkForm from '@/admin/components/blog/linkForm.vue'
import { FingerPrintIcon, LinkIcon } from '@heroicons/vue/20/solid'

const currentTab = ref(1)

const toggleTab = (index) => {

  currentTab.value = index
}
</script>
