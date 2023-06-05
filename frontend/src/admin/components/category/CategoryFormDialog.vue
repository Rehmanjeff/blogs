<template>
    
    <TransitionRoot as="template" :show="display">
    <Dialog as="div" class="relative z-10" @close="closeDialog">
      <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-500" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-hidden">
        <div class="absolute inset-0 overflow-hidden">
          <div class="fixed inset-y-0 right-0 flex max-w-full pl-10 pointer-events-none">
            <TransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="translate-x-full">
              <DialogPanel class="relative w-screen max-w-md pointer-events-auto">
                <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-500" leave-from="opacity-100" leave-to="opacity-0">
                  <div class="absolute top-0 left-0 flex pt-4 pr-2 -ml-8 sm:-ml-10 sm:pr-4">
                    <button type="button" class="text-gray-300 rounded-md hover:text-white focus:outline-none focus:ring-2 focus:ring-white" @click="closeDialog">
                      <span class="sr-only">Close panel</span>
                      <XMarkIcon class="w-6 h-6" aria-hidden="true" />
                    </button>
                  </div>
                </TransitionChild>
                <div class="flex flex-col h-full py-6 overflow-y-scroll bg-white shadow-xl">
                  <div class="px-4 sm:px-6">
                    <DialogTitle class="text-base font-semibold leading-6 text-gray-900">{{ edit ? 'Edit' : 'Add' }} Category</DialogTitle>
                  </div>
                  <div class="relative flex-1 px-4 mt-6 sm:px-6">
                    <div class="w-full mb-5">
                        <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                        <input type="text" v-model="name" name="name" id="name" autocomplete="name" class="block w-full h-10 pl-2 mt-1 text-sm text-gray-500 border border-gray-300 rounded-sm" />
                    </div>
                    <div class="flex"  @click="closeDialog">
                        <button type="button" @click="saveCategory" :disabled="name.trim() === ''" class="px-10 py-2 mt-20 ml-auto text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Save</button>
                    </div>
                  </div>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
  <PageNotification @close=closeNotification :show=notificationProps.show :type=notificationProps.type :message=notificationProps.message :messageDetails=notificationProps.messageDetails></PageNotification>
  
</template>

<script setup>
import { ref, reactive, watch } from 'vue' 
import PageNotification from '@/admin/widgets/PageNotification.vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/20/solid'
import Category from "@/composables/Category"

const props = defineProps(['edit', 'display'])
const emit = defineEmits(['isClosed', 'success', 'data'])
const {categoryName} = Category()
const token = ref(localStorage.getItem('blogsAccessToken'))

const name = ref('')
const notificationProps = reactive({
    show: false,
    message: null,
    messageDetails: '',
    type: ''
})

watch(() => props.edit, (newValue, oldValue) => {
    
    name.value = props.edit.name
})

const closeNotification = () => {


}
// Api request to save the category name to the database 
const saveCategory = ()=>{
  if(name.value != ''){
    categoryName(name.value, token.value).then((data)=>{
      if(data.status == 201){
        resetValue()
        emit('data')
      }else{
        notificationProps.show = true
        notificationProps.message = data.response.data.message
        notificationProps.type = "error"
      }
      
    })
  } 
}

const resetValue = ()=>{
  name.value = ''
}

const closeDialog = () => {

    emit('isClosed')
}

</script>