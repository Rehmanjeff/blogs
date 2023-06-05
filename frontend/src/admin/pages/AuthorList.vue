<template>

    <div>
        <PrimeDataTable :value="authors" ref="authorsTable" :paginator="true" class="p-datatable-customers primeDatatable" :rows="10" dataKey="id" :rowHover="true" v-model:filters="filters" filterDisplay="menu" :loading="loading" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries" :globalFilterFields="['fullName', 'designation.title','designation.employmentType', 'role']" responsiveLayout="scroll">
        <template #header>
            <div class="flex justify-content-center align-items-center">
                <h5 class="m-0 text-lg flex items-center justify-center">
                    Authors
                </h5>
                <div class="flex items-center justify-center ml-auto">
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <PrimeInputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </span>
                    <div class="ml-3">
                        <div @click="addAuthor()" class="flex flex-row items-center cursor-pointer bg-blue-600 px-3 py-2 text-white text-sm hover:bg-blue-700 rounded-md" :to="{ name: 'AdminCategoryCreate' }">
                            <PlusSmIconSolid class="h-5 w-5" aria-hidden="true" />
                            Add Author
                        </div>
                    </div>
                    <div class="ml-3 cursor-pointer" @click="exportDataToCSV(authorsTable)">
                        <div class="flex flex-row items-center justify-center px-3 py-2 text-sm btn bg-exportBtnBg text-exportBtnTxt rounded-md gap-1">
                            <ExternalLinkIcon class="h-5 w-5" aria-hidden="true" />
                            <span> Export</span>
                        </div>
                    </div>
                </div>
            </div>
        </template>
        <template #loading>
            <div class="loader"></div>
        </template>
        <template #empty>
            <span v-if="!loading" class="flex items-center justify-center">No records found</span>
        </template>
        <PrimeColumn field="name" header="Name" sortable style="min-width: 25rem">
            <template #body="{data}">
                <div class="flex items-center">
                    <span v-if="data.avatar" class="inline-block mr-3">
                        <img class="rounded-full w-12 thumbnail" :src="`/assets/authors/${data.avatar}`">
                    </span>
                    <span v-else class="inline-block mr-3">
                        <img class="rounded-full w-12 thumbnail" src="/assets/default.png">
                    </span>
                    <span class="inline-block">
                        {{ data.name }}
                    </span>
                </div>
            </template>
            <template #filter="{filterModel}">
                <PrimeInputText type="text" v-model="filterModel.value" class="p-column-filter" placeholder="Search"/>
            </template>
        </PrimeColumn>
        <PrimeColumn field="created_at" header="Created">
            <template #body="{data}">
                {{ data.created_at }}
            </template>
        </PrimeColumn>
        <PrimeColumn header="Actions" style="min-width: 14rem">
            <template #body="{data}">
                <span @click="proceedEdit(data)">Edit</span>
            </template>
        </PrimeColumn>
        </PrimeDataTable>

        <AuthorFormDialog @hasError="formError" @success="formSuccess" @isClosed="showForm = false" :display="showForm" :edit=author></AuthorFormDialog>
        <PageNotification @close=closeNotification :show=notificationProps.show :type=notificationProps.type :message=notificationProps.message :messageDetails=notificationProps.messageDetails></PageNotification>
    </div>
    
</template>
    
<script setup>
    import CommonFunctions from '@/composables/commonFunctions.js'
    import { FilterMatchMode, FilterOperator } from 'primevue/api'
    import { PlusIcon as PlusSmIconSolid } from '@heroicons/vue/20/solid'
    import { EnvelopeIcon as ExternalLinkIcon } from '@heroicons/vue/20/solid'
    import { ref, reactive, onMounted } from 'vue'
    import AuthorFormDialog from '@/admin/components/authors/AuthorFormDialog.vue'
    import PageNotification from '@/admin/widgets/PageNotification.vue'
    import Author from '@/composables/Author.js'
    
    const loading = ref(false)
    const authors = ref([])
    const authorsTable = ref([])
    const { exportDataToCSV } = CommonFunctions()
    const { listAuthors } = Author()
    const filters = ref({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] }
    })
    const showForm = ref(false)
    const token = localStorage.getItem('blogsAccessToken')
    const author = ref(null)
    const notificationProps = reactive({
        show: false,
        message: null,
        messageDetails: '',
        type: ''
    })

    const proceedEdit = (data) => {

        author.value = data
        showForm.value = true
    }

    const formSuccess = (message) => {

        showForm.value = false
        notificationProps.type = 'success'
        notificationProps.message = message
        notificationProps.show = true

        getAllAuthors()
    }

    const closeNotification = () => {

        notificationProps.show = false
    }

    const formError = (error) => {

        showForm.value = false
        notificationProps.type = 'error'
        notificationProps.message = error
        notificationProps.show = true
    }

    const getAllAuthors = () => {

        listAuthors(token).then((response) => {
          
          if(response.status == 200){
              
            authors.value = response.data.authors
          } else {
              
            console.log('Error loading authors')
          }
      })
    }

    const addAuthor = () => {

        author.value = null
        showForm.value = true
    }

    onMounted(() => {

        getAllAuthors()
    })
    
</script>