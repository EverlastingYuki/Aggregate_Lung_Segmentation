<script setup lang="ts">
import {ElImage} from 'element-plus'


import {storeToRefs} from 'pinia'
import {useInferenceStore} from '@/stores/inferenceStore'

import {
  Check, CircleCloseFilled,
  Delete,
  Edit,
  Close,
  Plus,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

const store = useInferenceStore()

const {
  workspace,
  pre_result_img_urls,
  uped_img_local_path,
  img_len,
  view_len,
  img_len_view,
  view_len_view,
  checkAll,
  indeterminate,
  selectedModels,
  models,
  isInferencing
} = storeToRefs(store)

const {
  renderContent,
  handleCheckChange,
  handleCheckAll,
  startInference,
  setListLength,
  setViewListLength,
} = store

setListLength(pre_result_img_urls);
setViewListLength(uped_img_local_path);

</script>

<template>
  <el-row>
    <!--工作区-->
    <el-col :span="4" style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 3px;padding-top: 2px; max-height: 75vh;flex-direction: column">
      <div style="height: 4.5vh;border-bottom: 2px dashed rgb(159.5, 206.5, 255);display: flex;flex-direction: row;justify-content: space-between;padding: 0.5vh">
        <div style="font-size: 2vh;justify-content: center;align-content: center;color: #409EFF">-工作区</div>
        <div style="align-content: center;">
          <el-tooltip content="新建工作区" placement="top" effect="light">
            <el-button type="primary" :icon="Plus" circle style="width: 2.5vh;height: 2.5vh;align-content: center;"/>
          </el-tooltip>
          <el-tooltip content="删除所选节点" placement="top" effect="light">
            <el-button type="danger" :icon="Close" circle style="width: 2.5vh;height: 2.5vh;align-content: center;"/>
          </el-tooltip>
        </div>
      </div>
      <el-scrollbar style="max-height: 66vh">
        <el-tree
          style="max-width: 600px"
          :data="workspace"
          show-checkbox
          node-key="id"
          render-after-expand
          :expand-on-click-node="false"
          :render-content="renderContent"
          @check-change="handleCheckChange"
      />
      </el-scrollbar>
    </el-col>

    <!--工作区选择的图像-->
    <el-col :span="9">
      <el-row align="top" :gutter="10">
        <el-col :span="24" align="middle" justify="center">
          <!-- 选择模型部分 -->
          <div>
            <el-select v-model="selectedModels" multiple clearable collapse-tags placeholder="选择推理的模型"
                       popper-class="custom-header" :max-collapse-tags="2" size="large" style="width: 20vw">
              <template #header>
                <el-checkbox v-model="checkAll" :indeterminate="indeterminate" @change="handleCheckAll">
                  All
                </el-checkbox>
              </template>
              <el-option v-for="item in models" :key="item.value" :label="item.label" :value="item.value"/>
            </el-select>

            <el-button type="primary" style="width: 15px;margin-left: 5px;">刷新</el-button>
          </div>
        </el-col>
        <el-col>
          <div style="height:5vw;"></div>
        </el-col>
        <el-col :span="24" align="middle">
          <!-- 选择的图片可视化部分 -->
          <div style="width: 95%;">
          </div>

          <div class="pre_result_show"
               :style="{ width: view_len_view+1 + 'vw', height: view_len_view + 'vw', overflowY: 'auto' }"
               style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 6px;">
            <el-image :style="{ width: img_len_view + 'vw', height: img_len_view+0.2 + 'vw' }"
                      v-for="(url, index) in uped_img_local_path"
                      :key="url" :src="url" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
                      :preview-src-list="uped_img_local_path"
                      :initial-index=index fit="cover"/>
          </div>
        </el-col>

      </el-row>
    </el-col>

    <!--            推理结果-->
    <el-col :span="11">
      <el-row align="top" :gutter="10">
        <el-col :span="24" align="middle">
          <el-button
              :type="isInferencing ? 'info' : 'primary'"
              plain
              :disabled="isInferencing"
              @click="startInference"
              style="width: 30vw;height: 4vw;">
            {{ isInferencing ? '推理中' : '开始推理' }}
          </el-button>
        </el-col>
        <el-col :span="24">
          <div style="height: 3vw;"></div>
        </el-col>
        <el-col :span="24" align="middle">
          <!-- 推理结果展示 -->
          <div class="pre_result_show"
               :style="{ width: view_len+1 + 'vw', height: view_len + 'vw', overflowY: 'auto' }"
               style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 6px;">
            <el-image :style="{ width: img_len + 'vw', height: img_len+0.2 + 'vw' }"
                      v-for="(url, index) in pre_result_img_urls"
                      :key="url" :src="url" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
                      :preview-src-list="pre_result_img_urls"
                      :initial-index=index fit="cover"/>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>