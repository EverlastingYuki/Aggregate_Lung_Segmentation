<script setup lang="ts">
import {ElIcon} from "element-plus";
import {WarnTriangleFilled, Menu as IconMenu} from "@element-plus/icons-vue";
import {useAsideStore} from "@/stores/asideStore"
import {RouterLink} from 'vue-router'
const { setFunction } = useAsideStore()
</script>

<template>
  <el-menu :default-active="'2'">
    <RouterLink to="/inferenceMain">
      <el-menu-item index="2" @click="setFunction('对比推理')">
        <el-icon>
          <icon-menu/>
        </el-icon>
        <template #title>对比推理</template>
      </el-menu-item>
    </RouterLink>

    <RouterLink to="/historyMain">
      <el-menu-item index="3" @click="setFunction('历史记录')">
        <el-icon>
          <WarnTriangleFilled/>
        </el-icon>
        <template #title>历史记录</template>
      </el-menu-item>
    </RouterLink>

    <el-menu-item index="4" disabled>
      <el-icon>
        <WarnTriangleFilled/>
      </el-icon>
      <template #title>施工中</template>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>
  a {
  text-decoration: none;
}
</style>