<template>
    

    <PrimeDataTable :value="categories" ref="categoryTable" :paginator="true" class="p-datatable-customers primeDatatable" :rows="10" dataKey="id" :rowHover="true" v-model:filters="filters" filterDisplay="menu" :loading="loading" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries" :globalFilterFields="['fullName', 'designation.title','designation.employmentType', 'role']" responsiveLayout="scroll">
      
        <template #header>    
            <div class="flex justify-content-center align-items-center">
                <h5 class="flex items-center justify-center m-0 text-lg">
                    Categories
                </h5>          
                <div class="flex items-center justify-center ml-auto">
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <PrimeInputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </span>
                    <div class="ml-3">
                        <div @click="showForm = true" class="flex flex-row items-center px-3 py-2 text-sm text-white bg-blue-600 rounded-md cursor-pointer hover:bg-blue-700" :to="{ name: 'AdminCategoryCreate' }">
                            <PlusSmIconSolid class="w-5 h-5" aria-hidden="true" />
                            Add Category
                        </div>
                    </div>
                    <div class="ml-3 cursor-pointer" @click="exportDataToCSV(categoryTable)">
                        <div class="flex flex-row items-center justify-center gap-1 px-3 py-2 text-sm rounded-md btn bg-exportBtnBg text-exportBtnTxt">
                            <ExternalLinkIcon class="w-5 h-5" aria-hidden="true" />
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
      <PrimeColumn field="id" header="ID" style="min-width: 4rem">
          <template #body="{data, index}">
              <div class="flex items-center">
                  <span class="inline-block">
                    {{ getCategoryID(index) }}
                  </span>
              </div>
          </template>
      </PrimeColumn>
      <PrimeColumn field="name" header="Name" sortable style="min-width: 25rem">
          <template #body="{data}">
              <div class="flex items-center">
                  <span class="inline-block">
                    {{ data.name }}
                  </span>
              </div>
          </template>
          <template #filter="{filterModel}">
              <PrimeInputText type="text" v-model="filterModel.value" class="p-column-filter" placeholder="Search"/>
          </template>
      </PrimeColumn>
      <PrimeColumn field="created_at" header="Created At" :exportable="true" :hidden="true">
          <template #body="{data}">
              {{ data.created_at }}
          </template>
      </PrimeColumn>
      <PrimeColumn header="Actions" style="min-width: 14rem">
          <template #body="{data}">
            <span @click="proceedEdit(data)" class="cursor-pointer">Edit</span>
          </template>
      </PrimeColumn>
    </PrimeDataTable>


    <CategoryFormDialog @success="formSuccess" @data="showSuccess"  @isClosed="showForm = false" :display="showForm" :edit=category></CategoryFormDialog>
    <PageNotification @close=closeNotification :show=notificationProps.show :type=notificationProps.type :message=notificationProps.message :messageDetails=notificationProps.messageDetails></PageNotification>   
</template>

    
<script setup>
import CommonFunctions from '@/composables/commonFunctions.js'
import PageNotification from '@/admin/widgets/PageNotification.vue'
import { FilterMatchMode, FilterOperator } from 'primevue/api'
import { PlusIcon as PlusSmIconSolid } from '@heroicons/vue/20/solid'
import { EnvelopeIcon as ExternalLinkIcon } from '@heroicons/vue/20/solid'
import { onMounted, reactive, ref } from 'vue'
import CategoryFormDialog from '@/admin/components/category/CategoryFormDialog.vue'
import Category from '@/composables/Category';

const token = ref(localStorage.getItem('blogsAccessToken'))
const {categoryList} = Category()   
const loading = ref(false)
const categories = ref([])
const categoryTable = ref([])
const { exportDataToCSV } = CommonFunctions()
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] }
})
const showForm = ref(false)
const category = ref(null)

// Compute the category ID
const getCategoryID = (index) => {
  return index + 1;
};

const notificationProps = reactive({
    show: false,
    message: null,
    messageDetails: '',
    type: ''
})
const closeNotification = () => {
    notificationProps.show = false

}
    
categories.value = ref[('')]

const getCategory=()=>{
    categoryList(token.value).then((data)=>{
        categories.value = data.data
    })
}



const proceedEdit = (data) => {
    
    category.value = data
    showForm.value = true
}

const formSuccess = () => {


}

const showSuccess = () => {
    getCategory()
  notificationProps.show = true;
  notificationProps.message = 'Category Save successfully !'
  notificationProps.type ='success'

  setTimeout(() => {
    notificationProps.show = false;
  }, 5000); // 5 seconds
};


onMounted(() => {
    getCategory()
  })


</script>