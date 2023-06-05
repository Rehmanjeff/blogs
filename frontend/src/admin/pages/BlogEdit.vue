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
                        </ul>
                    </div>
                </aside>
            </div>
  
            <div class="mt-5 md:col-span-4" v-if="currentTab == 1">
              <BlogManualForm @success="hasSuccess" @error="hasError" :blog="blog"></BlogManualForm>
            </div>
        </div>
        <PageNotification @close=closeNotification :show=notificationProps.show :type=notificationProps.type :message=notificationProps.message :messageDetails=notificationProps.messageDetails></PageNotification>
    </div>
  </template>
  
<script setup>
import { ref, onMounted, reactive } from 'vue'
import BlogManualForm from '@/admin/components/blog/manualForm.vue'
import { FingerPrintIcon, LinkIcon } from '@heroicons/vue/20/solid'
import Blog from "@/composables/Blog"
import PageNotification from '@/admin/widgets/PageNotification.vue'

const props = defineProps(['id'])
const token = localStorage.getItem('blogsAccessToken')
const currentTab = ref(1)
const blog = ref(null)
const { readBlog } = Blog()
const notificationProps = reactive({
    show: false,
    message: null,
    messageDetails: '',
    type: ''
})

const hasSuccess = (message) => {

    notificationProps.type = 'success'
    notificationProps.message = message
    notificationProps.show = true
}

const closeNotification = () => {

    notificationProps.show = false
}

const hasError = (error) => {

    notificationProps.type = 'error'
    notificationProps.message = error
    notificationProps.show = true
}

onMounted(() => {

    readBlog(token, props.id).then((data)=>{

        if(data.status == 200){

            blog.value = data.data.blog
        }else{

            console.log(data)
        }
    })
})

</script>
  