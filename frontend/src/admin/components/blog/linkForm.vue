<template>
    <div class="mr-5 md:mt-0 md:col-span-2">
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white sm:p-6">
                <h1 class="pb-5 font-semibold mb-6 text-md">Blog Link</h1>
                <div class="grid grid-cols-6 gap-6">
                    <div class="col-span-2 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Category</label>
                        <select v-model="selectedCategory" class="mt-3 block w-full bg-white border border-gray-300 outline-none h-10 py-1.5 pl-3 pr-10 text-gray-900 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                            <option v-for="category in categories" :key="category.category_id" :value="category.category_id">{{ category.name }}</option>
                        </select>
                    </div>
                    <div class="col-span-2 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Author</label>
                        <select v-model="selectedAuthor" class="mt-3 block w-full bg-white border border-gray-300 outline-none h-10 py-1.5 pl-3 pr-10 text-gray-900 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                            <option v-for="author in authors" :key="author.id" :value="author.id">{{ author.name }}</option>
                        </select>
                    </div>
                    <div class="col-span-2 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Status</label>
                        <select v-model="status" class="mt-3 block w-full bg-white border border-gray-300 outline-none h-10 py-1.5 pl-3 pr-10 text-gray-900 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                            <option value="live">Live</option>
                            <option value="draft">Draft</option>
                        </select>
                    </div>
                    <div class="col-span-6 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Link*</label>
                        <input v-model="link" type="text" autocomplete="given-title" class="mt-3 border rounded-sm h-10 w-full block pl-2 text-gray-500 text-sm outline-none" :class="(errors.title) ? 'border-themered' : 'border-gray-300'" />
                        <span class="mt-2 text-sm text-themered" v-if="errors.link">{{ errors.link }}</span>
                    </div>
                </div>
            </div>
            <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                <button @click="submitForm" type="button" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" :class="loading ? 'cursor-not-allowed' : 'hover:bg-indigo-700'">Proceed</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Category from "@/composables/Category"
import Author from "@/composables/Author"
import Blog from "@/composables/Blog"

const token = localStorage.getItem('blogsAccessToken')
const props = defineProps(['blog'])
const emit = defineEmits(['success', 'error'])
const link = ref('')
const errors = reactive({ link : ''})
const { categoryList } = Category()
const { listAuthors } = Author()
const { createBlog } = Blog()
const authors = ref([])
const selectedAuthor = ref(null)
const categories = ref([])
const selectedCategory = ref(null)
const loading = ref(false)
const status = ref('live')

const resetErrors = () => {

    errors.link = ''
}
const submitForm = () => {

    if(!loading.value){

        resetErrors()
        if(link.value == ''){

            errors.link = 'Link is required' 
        }else{

            loading.value = true
            const formData = new FormData()
            formData.append('link', link.value)
            formData.append('author', selectedAuthor.value)
            formData.append('category', selectedCategory.value)
            formData.append('type', 'link')
            formData.append('status', status.value)

            createBlog(token, formData).then((data)=>{

                loading.value = false
                if(data.status == 201){
                
                    resetForm()
                    emit('success', data.data.message)
                }else{

                    emit('error', data.data && data.data.message ? data.data.message : response)
                }
            })
        }
    }
}

const resetForm = () => {

    selectedAuthor.value = authors.value.length ? authors.value[0].id : null
    selectedCategory.value = categories.value.length ? categories.value[0].category_id : null
    link.value = ''
    status.value = 'live'
}

onMounted(() => {

    categoryList(token).then((data)=>{

      if(data.status == 200){
        
        categories.value = data.data
        selectedCategory.value = categories.value.length ? categories.value[0].category_id : null
      }else{

        console.log(data)
      }
      
    })

    listAuthors(token).then((data)=>{

        if(data.status == 200){
        
            authors.value = data.data.authors
            selectedAuthor.value = authors.value.length ? authors.value[0].id : null
        }else{

            console.log(data)
        }

    })
})

</script>