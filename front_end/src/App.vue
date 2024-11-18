<script setup lang="tsx">

// 按钮，多选框的导入
import {
  Avatar,
  Menu as IconMenu,
  WarnTriangleFilled
} from '@element-plus/icons-vue'
import {onMounted, ref, watch} from 'vue'
import type {CheckboxValueType, UploadProps, UploadUserFile} from 'element-plus'
// 展示预测结果的导入
import {ElIcon, ElImage,} from 'element-plus'
// 上传图片的导入
import { storeToRefs } from 'pinia'
import {useInferenceStore} from '@/stores/inferenceStore'
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
          <el-menu>
            <el-menu-item index="2">
              <el-icon>
                <icon-menu/>
              </el-icon>
              <template #title>对比推理</template>
            </el-menu-item>
            <el-menu-item index="3" disabled>
              <el-icon>
                <WarnTriangleFilled/>
              </el-icon>
              <template #title>施工中</template>
            </el-menu-item>
            <el-menu-item index="4" disabled>
              <el-icon>
                <WarnTriangleFilled/>
              </el-icon>
              <template #title>施工中</template>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- 主体部分 -->
        <el-main style="padding: 5px;padding-top: 20px">
          <el-row>
            <!--            工作区-->
            <el-col :span="4" style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 2px;padding-top: 8px">
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
            </el-col>

            <!--            工作区选择的图像-->
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
                  <!--                  <img :src="temp_dir" alt="">-->
                  <!--                  <img :src="uped_img_local_path[0]" alt="">-->
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

/* 自定义树节点样式 */
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.avatar-uploader .el-upload {
  border: 2px dashed rgb(159.5, 206.5, 255);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>