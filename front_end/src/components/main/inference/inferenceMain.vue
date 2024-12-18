<script setup lang="ts">
import {ElImage} from 'element-plus'


import {storeToRefs} from 'pinia'
import {useInferenceStore} from '@/stores/inferenceStore'

import {CirclePlus, Close, Plus, Tools,Search,} from '@element-plus/icons-vue'
import {VueDraggable} from 'vue-draggable-plus'

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
  new_workspace_name,
  isInferencing,
  pre_results,
  draggable_tag_list,
  mapping_tag_dict,
  showed_draggable_tag_list,
    treeRef,
        filter_node_text,
} = storeToRefs(store)

const {
  renderContent,
  handleCheckChange,
  handleCheckAll,
  startInference,
  setListLength,
  setViewListLength,
  createNewWorkspace,
  refreshNewWorkspaceName,
  removeSelectedNodes,
  dobleClickToTransferTag,
    filterNode,
} = store


setViewListLength(uped_img_local_path);

</script>

<template>
  <el-row>
    <!--工作区-->
    <el-col :span="4"
            style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 3px;padding-top: 2px; max-height: 75vh;flex-direction: column">
      <div
          style="height: 4.5vh;border-bottom: 2px dashed rgb(159.5, 206.5, 255);display: flex;flex-direction: row;justify-content: space-between;padding: 0.5vh">
        <div style="font-size: 2vh;justify-content: center;align-content: center;color: #409EFF">
          <a>&nbsp;工作区&nbsp;&nbsp;</a>
          <el-input style="width: 6.5vw" placeholder="按名称筛选" :prefix-icon="Search" v-model="filter_node_text"/>
        </div>
        <div style="align-content: center;">
          <el-popover placement="bottom" :width="300" trigger="click" title="新建工作区"
                      @hide="refreshNewWorkspaceName">
            <template #reference>
              <el-button type="primary" :icon="Plus" circle style="width: 2.5vh;height: 2.5vh;align-content: center;"/>
            </template>
            <template #default>
              <el-input
                  v-model="new_workspace_name"
                  style="width: 240px"
                  placeholder="请输入新的工作区名称"
              >
                <template #prepend>
                  <el-button :icon="CirclePlus" style="color:#409EFF; background-color: rgb(216.8, 235.6, 255)"
                             @click="createNewWorkspace"/>
                </template>
              </el-input>
            </template>
          </el-popover>
          <el-tooltip content="删除所选节点" placement="top" effect="light">
            <el-button type="danger" :icon="Close" circle style="width: 2.5vh;height: 2.5vh;align-content: center;"
                       @click="removeSelectedNodes"/>
          </el-tooltip>
        </div>
      </div>
      <el-scrollbar style="max-height: 66vh">
        <el-tree
            ref="treeRef"
            style="max-width: 600px"
            :data="workspace"
            show-checkbox
            node-key="id"
            render-after-expand
            :expand-on-click-node="false"
            :render-content="renderContent"
            @check-change="handleCheckChange"
            :filter-node-method="filterNode"
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
          <div style="height: 1.5vw;"></div>
        </el-col>
        <el-col :span="24" align="middle" style="position: relative;">
          <VueDraggable
              class="draggable-container1"
              v-model="showed_draggable_tag_list"
              :animation="100"
              ghostClass="ghost"
              group="people"
              :style="{ width: view_len+1 + 'vw'}"
              style="display:flex;flex-direction: row;"
          >
<!--            <el-tag round-->
<!--                    v-for="(item, index) in showed_draggable_tag_list" :key="index"-->
<!--                        :style="{ backgroundColor: item.bg_color, width: img_len + 'vw', border: '2px solid ' + item.border_color}"></el-tag>-->
            <div v-for="(item, index) in showed_draggable_tag_list" :key="index" >
              <el-popover placement="top" :width="100"
                        trigger="hover">
              <template #reference>
                <el-tag round
                        @dblclick="() => dobleClickToTransferTag(item.name)"
                        :style="{ backgroundColor: item.bg_color, width: img_len + 'vw', border: '2px solid ' + item.border_color}"></el-tag>
              </template>
              <div>{{ item.name }}</div>
            </el-popover>
            </div>

          </VueDraggable>
          <el-popover placement="left" :width="310" trigger="click" title="请将不需要的标签拖拽至此">
            <template #reference>
              <el-tag round type="primary" size="large" style="position: absolute;top: 0;left:3.5vw">
                <el-icon>
                  <Tools/>
                </el-icon>
              </el-tag>
            </template>
            <VueDraggable
                class="draggable-container0"
                v-model="draggable_tag_list"
                :animation="100"
                ghostClass="ghost"
                group="people"
                style="height: 200px; width: 270px; border: 2px solid #a0cfff;border-radius: 3px;padding: 3px; overflow: auto"
            >
              <div v-for="(item, index) in draggable_tag_list" :key="index" style="padding: 2px">
                <el-tag round
                        @dblclick="() => dobleClickToTransferTag(item.name)"
                        :style="{ backgroundColor: item.bg_color, width: 4 + 'vw', border: '2px solid ' + item.border_color}"></el-tag>
              {{ item.name }}
              </div>
            </VueDraggable>
          </el-popover>
          <div style="height: 0.3vw"></div>
        </el-col>
        <el-col :span="24" align="middle">
          <!-- 推理结果展示 -->
          <div class="pre_result_show"
               :style="{ width: view_len+1 + 'vw', height: view_len + 'vw', overflowY: 'auto' }"
               style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 6px;display:flex;flex-direction: row">

            <div v-for="(item, index) in showed_draggable_tag_list" :key="index" class="result_v_mod"
                 :style="{ width: img_len + 'vw', height: img_len*uped_img_local_path.length + 'vw' }">
              <el-image :style="{ width: img_len-0.1 + 'vw', height: img_len + 'vw' }"
                        v-for="(url, index) in pre_results[mapping_tag_dict[item.name]]"
                        :key="url" :src="url" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
                        :preview-src-list="pre_results[mapping_tag_dict[item.name]]"
                        :initial-index=index fit="cover"/>
            </div>

          </div>
        </el-col>
      </el-row>
    </el-col>
  </el-row>
</template>

<style scoped>
.result_v_mod {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>