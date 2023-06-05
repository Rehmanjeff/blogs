<template>
    <div>
      <TransitionRoot as="template" :show="display">
      <Dialog as="div" class="relative z-10" @close="closeDialog">
        <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-500" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-hidden">
          <div class="absolute inset-0 overflow-hidden">
            <div class="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
              <TransitionChild as="template" enter="transform transition ease-in-out duration-500 sm:duration-700" enter-from="translate-x-full" enter-to="translate-x-0" leave="transform transition ease-in-out duration-500 sm:duration-700" leave-from="translate-x-0" leave-to="translate-x-full">
                <DialogPanel class="pointer-events-auto relative w-screen max-w-md">
                  <TransitionChild as="template" enter="ease-in-out duration-500" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-500" leave-from="opacity-100" leave-to="opacity-0">
                    <div class="absolute left-0 top-0 -ml-8 flex pr-2 pt-4 sm:-ml-10 sm:pr-4">
                      <button type="button" class="rounded-md text-gray-300 hover:text-white focus:outline-none focus:ring-2 focus:ring-white" @click="closeDialog">
                        <span class="sr-only">Close panel</span>
                        <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                      </button>
                    </div>
                  </TransitionChild>
                  <div class="flex h-full flex-col overflow-y-scroll bg-white py-6 shadow-xl">
                    <div class="px-4 sm:px-6">
                      <DialogTitle class="text-base font-semibold leading-6 text-gray-900">{{ author ? 'Edit' : 'Add' }} Author</DialogTitle>
                    </div>
                    <div class="relative mt-6 flex-1 px-4 sm:px-6">
                      <div class="w-full mb-5">
                          <label class="block text-sm font-medium text-gray-700">
                            Avatar
                            <span class="text-sm text-themered" v-if="avatarError"> ({{ avatarError }})</span>
                          </label>
                          <div>
                              <input class="hidden" ref="file" type="file" @change="updateAvatar" name="file" accept="image/*">
                              <div class="flex items-center gap-2 mt-2">
                                <img class="w-12 object-cover rounded-full" :src="author.avatar != '' ? `/assets/authors/${author.avatar}` : avatarSource" />
                                <button @click="$refs.file.click()" type="button" class="relative overflow-hidden mt-2 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Change</button>
                              </div>
                            </div>
                      </div>
                      <div class="w-full mb-5">
                          <label class="block text-sm font-medium text-gray-700">Name</label>
                          <input type="text" v-model="author.name" class="mt-1 border border-gray-300 rounded-sm h-10 w-full block pl-2 text-gray-500 text-sm" />
                          <div class="text-sm text-themered" v-if="nameError">{{ nameError }}</div>
                        </div>
                      <div class="flex">
                          <button @click="proceedCreateAuthor" type="button" class="ml-auto mt-20 bg-indigo-600 py-2 px-10 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Save</button>
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
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue' 
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { XMarkIcon } from '@heroicons/vue/20/solid'
import Author from '@/composables/Author.js'

const defaultAvatar = '/assets/default.png'
const { createAuthor, updateAuthor } = Author()
const token = localStorage.getItem('blogsAccessToken')
const props = defineProps(['edit', 'display'])
const emit = defineEmits(['isClosed', 'success', 'hasError'])
const avatarError = ref(false)
const nameError = ref(false)
const selectedFile = ref(null)
const avatarSource = ref(defaultAvatar)
const author = reactive({id: null, name: '', avatar: ''})

watch(() => props.edit, (newValue, oldValue) => {
  
  if(newValue !== null){
    
    // edit button was clicked
    author.id = newValue.id
    author.name = newValue.name
    author.avatar = newValue.avatar
  }else{

    // add button was clicked
    author.id = null
    author.name = ''
    author.avatar = ''
    avatarSource.value = defaultAvatar
  }
})

const closeDialog = () => {

  emit('isClosed')
}

const updateAvatar = (e) => {

  let file = e.target.files[0]
  selectedFile.value = e.target.files[0]
  let reader = new FileReader()  

  if(file['size'] < 2111775){ // limit is 2MB

      reader.onloadend = (file) => {
        
        avatarSource.value = reader.result
        author.avatar = ''
      }              
      reader.readAsDataURL(file)
  }else{

      selectedFile.value = null
      emit('hasError', 'Image must be 2MB or less')
  }
}

const proceedCreateAuthor = () => {

  resetErrors()
  if(selectedFile.value == null && author.id == null){
    
    avatarError.value = 'Required'
  }else if(author.name == ''){

    nameError.value = 'Required'
  }else{

    if(author.id == null){

      // send add author
      const formData = new FormData()
      formData.append('name', author.name)
      formData.append('avatar', selectedFile.value)
      createAuthor(token, formData).then((response) => {
            
          if(response.status == 201){
              
            emit('success', response.data.message)
          } else {
              
            emit('hasError', response.data && response.data.message ? response.data.message : response)
          }
      })
    }else{

      // send update author
      const formData = new FormData()
      formData.append('name', author.name)
      formData.append('avatar', selectedFile.value)
      updateAuthor(token, formData, author.id).then((response) => {
            
          if(response.status == 200){
              
            emit('success', response.data.message)
          } else {
              
            emit('hasError', response.data && response.data.message ? response.data.message : response)
          }
      })
    }
  }
}

const resetErrors = () => {

  nameError.value = avatarError.value = false
}

</script>