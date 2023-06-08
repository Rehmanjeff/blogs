<template>
    <div class="mr-5 md:mt-0 md:col-span-2">
        <div class="overflow-hidden shadow sm:rounded-md">
            <div class="px-4 py-5 bg-white sm:p-6">
                <h1 class="pb-5 mb-6 font-semibold text-md">Blog Details</h1>
                <div class="grid grid-cols-6 gap-6">

                    <div class="col-span-2 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Category</label>
                        <select v-model="selectedCategory" class="block w-full h-10 pl-2 mt-3 text-sm text-gray-500 border border-gray-300 rounded-sm outline-none">
                            <option v-for="(item,index) in categories" :key="index" :value=item.category_id>
                                {{ item.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col-span-2 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Author</label>
                        <select v-model="selectedAuthor" class="block w-full h-10 pl-2 mt-3 text-sm text-gray-500 border border-gray-300 rounded-sm outline-none">
                            <option v-for="(item,index) in authors" :key="index" :value=item.id>
                                {{ item.name }}
                            </option>
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
                        <label class="block text-sm font-medium text-gray-700">Title*</label>
                        <input v-model="title" type="text" autocomplete="given-title" class="block w-full h-10 pl-2 mt-3 text-sm text-gray-500 border rounded-sm outline-none" :class="(errors.title) ? 'border-themered' : 'border-gray-300'" />
                        <span class="mt-2 text-sm text-themered" v-if="errors.title">{{ errors.title }}</span>
                    </div>

                    <div class="col-span-6 mb-5">
                        <label class="block text-sm font-medium text-gray-700">Description*</label>
                        <div class="mt-3 ">
                            <QuillEditor class="editor" theme="snow" :content="content" contentType="html" ref="quillEditorRef" />
                        </div>
                        <span class="mt-2 text-sm text-themered" v-if="errors.description">{{ errors.description }}</span>
                    </div>
                </div>
            </div>
            <div class="px-4 py-3 text-right bg-gray-50 sm:px-6">
                <button @click="submitForm" type="button" class="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Proceed</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import Category from "@/composables/Category"
import Author from "@/composables/Author"
import Blog from "@/composables/Blog"

const token = localStorage.getItem('blogsAccessToken')
const props = defineProps(['blog'])
const emit = defineEmits(['success', 'error'])
const quillEditorRef = ref(null)
const content = ref('')
const title = ref('')
const errors = reactive({ title : '', description : ''})
const { categoryList } = Category()
const { listAuthors } = Author()
const { createBlog, updateBlog } = Blog()
const authors = ref([])
const selectedAuthor = ref(null)
const categories = ref([])
const selectedCategory = ref(null)
const loading = ref(false)
const edit = ref(false)
const status = ref('live')

const resetErrors = () => {

    errors.title = errors.description = ''
}
const submitForm = () => {

    if(!loading.value){

        resetErrors()
        const quillEditor = quillEditorRef.value
        if(quillEditor){

            content.value = quillEditor.getHTML()
        }

        if(title.value == ''){

            errors.title = 'Title is required' 
        }else if(quillEditor.getText().trim() == ''){

            errors.description = 'Description is required' 
        }else{

            loading.value = true
            if(edit.value == false){

                const formData = new FormData()
                formData.append('name', title.value)
                formData.append('description', content.value)
                formData.append('author', selectedAuthor.value)
                formData.append('category', selectedCategory.value)
                formData.append('type', 'manual')
                formData.append('status', status.value)

                createBlog(token, formData).then((data)=>{
                    console.log(data)

                    loading.value = false
                    if(data.status == 201){
                    
                        resetForm()
                        emit('success', data.data.message)
                    }else{

                        emit('error', data.data && data.data.message ? data.data.message : response)
                    }
                })
            }else{

                const formData = new FormData()
                formData.append('name', title.value)
                formData.append('description', content.value)
                formData.append('author', selectedAuthor.value)
                formData.append('category', selectedCategory.value)
                formData.append('type', 'manual')
                formData.append('status', status.value)

                updateBlog(token, formData, edit.value).then((data)=>{

                    loading.value = false
                    if(data.status == 200){
                    
                        emit('success', data.data.message)
                    }else{

                        emit('error', data.data && data.data.message ? data.data.message : response)
                    }
                })
            }
        }
    }
}

// const resetForm = () => {

//     selectedAuthor.value = authors.value.length ? authors.value[0].id : null
//     selectedCategory.value = categories.value.length ? categories.value[0].category_id : null
//     title.value = content.value = ''
//     status.value = 'live'

//     const quillEditor = quillEditorRef.value
//     quillEditor.setContents([])
// }

const resetForm = () => {
  if (authors.value.length > 0) {
    selectedAuthor.value = authors.value[0].id;
  } else {
    selectedAuthor.value = null;
  }

  if (categories.value.length > 0) {
    selectedCategory.value = categories.value[0].category_id;
  } else {
    selectedCategory.value = null;
  }

  title.value = '';
  content.value = '';
  status.value = 'live';

  const quillEditor = quillEditorRef.value;
  quillEditor.setContents([]);
};

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

    watch(() => props.blog, (newValue, oldValue) => {
  
        if(newValue !== null){
            
            title.value = newValue.name
            selectedAuthor.value = newValue.author
            selectedCategory.value = newValue.category
            status.value = newValue.status

            const quillEditor = quillEditorRef.value
            quillEditor.setHTML(newValue.description)
            edit.value = newValue.id
        }
    })
})

</script>

<style>
.editor {
  min-height: 200px;
}
</style>