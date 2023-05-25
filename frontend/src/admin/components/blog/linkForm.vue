<template>
    <div class="mr-5 md:mt-0 md:col-span-2">
        <div class="shadow overflow-hidden sm:rounded-md">
            <div class="px-4 py-5 bg-white sm:p-6">
                <h1 class="pb-5 font-semibold mb-6 text-md">Blog Link</h1>
                <div class="grid grid-cols-6 gap-6">
                    <div class="col-span-6 mb-5">
                        <label for="title" class="block text-sm font-medium text-gray-700">Link*</label>
                        <input v-model="link" type="text" autocomplete="given-title" class="mt-3 border rounded-sm h-10 w-full block pl-2 text-gray-500 text-sm outline-none" :class="(errors.title) ? 'border-themered' : 'border-gray-300'" />
                        <span class="mt-2 text-sm text-themered" v-if="errors.link">{{ errors.link }}</span>
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
const link = ref('')
const errors = reactive({ link : ''})

const resetErrors = () => {

    errors.link = ''
}
const submitForm = () => {

    resetErrors()
    if(link.value == ''){

        errors.link = 'Link is required' 
    }else{

        // api call here
    }
}

if(props.blog){

    link.value = props.blog.link
}

</script>