<script setup lang="tsx">
// 导入系统包
import {storeToRefs} from 'pinia'
// 导入用户store
import {useAsideStore} from "@/stores/asideStore"
const { selectedAsideFunction } = storeToRefs(useAsideStore())
import {RouterView} from 'vue-router'
// 用户组件的导入
import asideMain from '@/components/aside/asideMain.vue'
import inferenceMain from '@/components/main/inference/inferenceMain.vue'
import historyMain from '@/components/main/history/historyMain.vue'

</script>

<template>
  <div class="common-layout">
    <el-container class="main-container" style="height: 100vh;">
      <!-- 标题-->
      <el-header height="55px" style="border-bottom: 1px solid var(--el-border-color)">
        <div style="width: 100%; height: 100%;display: inline-flex;align-items: center;justify-content: center;">
          <el-icon :size="25" color="#606266">
            <Avatar/>
          </el-icon>
          <el-text size="large" tag="b">肺部影像segment</el-text>
        </div>
      </el-header>
      <el-container height="100vh">
        <!-- 侧边栏 -->
        <el-aside width="10vw" style="border-right: 1px solid var(--el-border-color);">
          <asideMain/>
        </el-aside>
        <!-- 主体部分 -->
        <el-main style="padding: 5px;padding-top: 20px">
<!--          <inferenceMain v-if="selectedAsideFunction === '对比推理'"/>-->
<!--          <historyMain v-if="selectedAsideFunction === '历史记录'"/>-->
          <RouterView></RouterView>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.custom-header {
  .el-checkbox {
    display: flex;
    height: unset;
  }
}
</style>
