<template>
    <div aria-live="assertive" class="fixed inset-0 z-20 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start">
      <div class="flex flex-col items-center w-full space-y-4 sm:items-end">
        <transition enter-active-class="transition duration-300 ease-out transform" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
          <div v-if="show" class="w-full max-w-sm overflow-hidden bg-white rounded-lg shadow-lg pointer-events-auto ring-1 ring-black ring-opacity-5">
            <div class="p-4">
              <div class="flex items-start">
                <div class="flex-shrink-0">
                  <CheckCircleIcon v-if="type == 'success'" class="w-6 h-6 text-green-400" aria-hidden="true" />
                  <XCircleIcon v-else-if="type == 'error'" class="w-6 h-6 text-themered" aria-hidden="true" />
                </div>
                <div class="ml-3 w-0 flex-1 pt-0.5">
                  <p :class="type == 'success' ? 'text-themegreen' : 'text-themered'" class="text-sm text-gray-900">{{message}}</p>
                  <p v-if="messageDetails != ''" class="mt-1 text-sm text-gray-500">{{messageDetails}}</p>
                </div>
                <div class="flex flex-shrink-0 ml-4">
                  <button type="button" @click="this.$emit('close')" class="inline-flex text-gray-400 bg-white rounded-md hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    <span class="sr-only">Close</span>
                    <XMarkIcon class="w-5 h-5" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </template>
  
  <script setup>
  
  import { ref } from 'vue'
  import { CheckCircleIcon, XCircleIcon } from '@heroicons/vue/20/solid'
  import { XMarkIcon } from '@heroicons/vue/20/solid' 
  
  const props = defineProps(['show', 'type', 'message', 'messageDetails'])
  const emit = defineEmits(['close'])

  </script>