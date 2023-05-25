<template>
    <div class="mr-5 md:mt-0 md:col-span-2">
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white sm:p-6">
                <h1 class="pb-5 font-semibold mb-6 text-md">Blog Details</h1>
                <div class="grid grid-cols-6 gap-6">

                    <div class="col-span-6 mb-5">
                        <label for="title" class="block text-sm font-medium text-gray-700">Category</label>
                        <select v-model="category" class="mt-3 border border-gray-300 rounded-sm h-10 w-full block pl-2 text-gray-500 text-sm outline-none">
                            <option value="">Select category</option>
                            <option v-for="(item,index) in categories" :key="index" :value=item.id>
                                {{ item.name }}
                            </option>
                        </select>
                    </div>

                    <div class="col-span-6 mb-5">
                        <label for="title" class="block text-sm font-medium text-gray-700">Title*</label>
                        <input v-model="title" type="text" autocomplete="given-title" class="mt-3 border rounded-sm h-10 w-full block pl-2 text-gray-500 text-sm outline-none" :class="(errors.title) ? 'border-themered' : 'border-gray-300'" />
                        <span class="mt-2 text-sm text-themered" v-if="errors.title">{{ errors.title }}</span>
                    </div>

                    <div class="col-span-6 mb-5">
                        <label for="title" class="block text-sm font-medium text-gray-700">Description*</label>
                        <div class="mt-3 ">
                            <QuillEditor class="editor" theme="snow" :content="content" contentType="html" ref="quillEditorRef" />
                        </div>
                        <span class="mt-2 text-sm text-themered" v-if="errors.description">{{ errors.description }}</span>
                    </div>
                </div>
            </div>
            <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                <button @click="submitForm" type="button" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Proceed</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps(['blog'])
const quillEditorRef = ref(null)
const content = ref('')
const title = ref('')
const errors = reactive({ titlle : '', description : ''})
const category = ref('')
const categories = ref([
    {id: 1, name: 'cate one'},
    {id:2, name: 'cate two'}
])

const resetErrors = () => {

    errors.title = errors.description = ''
}
const submitForm = () => {

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

        // api call here
    }
}

if(props.blog){

    category.value = props.blog.category
    title.value = props.blog.title
    content.value = props.blog.description
}

</script>

<style>
    .editor { min-height: 200px }
</style>