<script setup lang="ts">
import {ElIcon} from "element-plus";
import {WarnTriangleFilled, Menu as IconMenu} from "@element-plus/icons-vue";
import {useAsideStore} from "@/stores/asideStore"
const { setFunction } = useAsideStore()
</script>

<template>
  <el-menu>
    <el-menu-item index="2" @click="setFunction('对比推理')">
      <el-icon>
        <icon-menu/>
      </el-icon>
      <template #title>对比推理</template>
    </el-menu-item>
    <el-menu-item index="3" @click="setFunction('历史记录')">
      <el-icon>
        <WarnTriangleFilled/>
      </el-icon>
      <template #title>历史记录</template>
    </el-menu-item>
    <el-menu-item index="4" disabled>
      <el-icon>
        <WarnTriangleFilled/>
      </el-icon>
      <template #title>施工中</template>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>

</style>