<template>
    <div>
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
                      <DialogTitle class="text-base font-semibold leading-6 text-gray-900">{{ edit ? 'Edit' : 'Add' }} Author</DialogTitle>
                    </div>
                    <div class="relative flex-1 px-4 mt-6 sm:px-6">
                      <div class="w-full mb-5">
                          <label class="block text-sm font-medium text-gray-700">
                            Avatar
                            <span class="text-sm text-themered" v-if="avatarError"> ({{ avatarError }})</span>
                          </label>
                          <div>
                              <input class="hidden" ref="file" type="file" @change="updateAvatar" name="file" accept="image/*">
                              <div class="flex items-center gap-2 mt-2">
                                <img class="object-cover w-12 rounded-full" :src="author.avatar != '' ? `/assets/authors/${author.avatar}` : avatarSource" />
                                <button @click="$refs.file.click()" type="button" class="relative px-3 py-2 mt-2 overflow-hidden text-sm font-medium leading-4 text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Change</button>
                              </div>
                            </div>
                      </div>
                      <div class="w-full mb-5">
                          <label class="block text-sm font-medium text-gray-700">Name</label>
                          <input type="text" v-model="author.name" class="block w-full h-10 pl-2 mt-1 text-sm text-gray-500 border border-gray-300 rounded-sm" />
                          <div class="text-sm text-themered" v-if="nameError">{{ nameError }}</div>
                        </div>
                        <div class="w-full mb-5">
                          <label class="block text-sm font-medium text-gray-700">Designation <span class="text-xs text-gray-400">(optional)</span> </label>
                          <input type="text" v-model="author.designation" class="block w-full h-10 pl-2 mt-1 text-sm text-gray-500 border border-gray-300 rounded-sm" />
                        </div>
                      <div class="flex">
                          <button @click="proceedCreateAuthor" type="button" class="px-10 py-2 mt-20 ml-auto text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Save</button>
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
const author = reactive({id: null, name: '', avatar: '', designation:''})

watch(() => props.edit, (newValue, oldValue) => {
  
  if(newValue !== null){
    
    // edit button was clicked
    author.id = newValue.id
    author.name = newValue.name
    author.avatar = newValue.avatar
    author.designation = newValue.designation
  }else{

    // add button was clicked
    author.id = null
    author.name = ''
    author.avatar = ''
    author.designation = ''
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
      formData.append('designation', author.designation)
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
      formData.append('designation', author.designation)
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