import {createRouter,createWebHistory}  from 'vue-router'

import inferenceMain from '@/components/main/inference/inferenceMain.vue'
import historyMain from '@/components/main/history/historyMain.vue'

const router = createRouter({
    history : createWebHistory(),
    routes : [
        {
            path:'/',
            redirect:'/inferenceMain'
        },
        {
            path:'/inferenceMain',
            name:'inferenceMain',
            component:inferenceMain
        },
        {
            path:'/historyMain',
            name:'historyMain',
            component:historyMain
        }
    ]
})
export default router