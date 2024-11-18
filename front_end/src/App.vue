<script setup lang="tsx">

// 用户组件的导入
import asideMain from '@/components/aside/asideMain.vue'
import inferenceMain from '@/components/main/inference/inferenceMain.vue'
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
          <inferenceMain />
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

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>


<style>
</style>