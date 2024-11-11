<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { ElMessage, ElUpload, ElIcon } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'
import type { CheckboxValueType, UploadFile } from 'element-plus'

const imageUrl = ref('')
const pre_result_img_urls = ref<string[]>([])
const result_img_list_len = ref(0)
const img_len = ref(0)
const veiw_len = ref(0)
const checkAll = ref(false)
const indeterminate = ref(false)
const localImageUrl = ref('') 
const value = ref<CheckboxValueType[]>([])
const models = ref([{ value: 'U-net', label: 'U-net' }, { value: 'DeepLab', label: 'DeepLab' }, { value: 'WeClip', label: 'WeClip' }])
const isInferencing = ref(false) // 控制推理按钮的状态


const beforeAvatarUpload = (rawFile: any) => {
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
    ElMessage.error('Avatar picture must be JPG or PNG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}


// 动态设置图片显示列表的大小
function setListLength(list: any) {
  if (list.length <= 1) {
    img_len.value = 25
    veiw_len.value = 26
  } else if (list.length <= 4 && list.length >= 2) {
    img_len.value = 12.5
    veiw_len.value = 26
  } else {
    img_len.value = 8.33
    veiw_len.value = 26
  }
}

// 获取模型名称列表的请求
const fetchModels = async () => {
  try {
    const response = await axios.get('/api/models')
    if (response.status === 200) {
      models.value = response.data.map((model: string) => ({
        value: model,
        label: model,
      }))
      ElMessage.success('模型列表已更新')
    }
  } catch (error) {
    ElMessage.error('获取模型列表失败，使用默认列表')
  }
}
 // 保存后端返回的文件路径
 // 用于展示的 blob URL

const handleChange = (file: any) => {
  const formData = new FormData()
  formData.append('file', file.raw)

  axios.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }).then((response) => {
    if (response.status === 200) {
      ElMessage.success('图片上传成功')
      localImageUrl.value = URL.createObjectURL(file.raw)  // 用于展示
      imageUrl.value = response.data.file_path  // 用于推理
    } else {
      ElMessage.error('图片上传失败')
    }
  }).catch((error) => {
    ElMessage.error(`上传失败: ${error}`)
  })
}

// 触发推理请求
const startInference = async () => {
  if (!imageUrl.value || value.value.length === 0) {
    ElMessage.error('请上传图片并选择模型')
    return
  }

  isInferencing.value = true

  try {
    const response = await axios.post('/api/inference', {
      image_url: imageUrl.value,
      models: value.value,
    })

    if (response.status === 200) {
      ElMessage.success('推理完成')
      pre_result_img_urls.value = response.data.result_images
      setListLength(pre_result_img_urls.value)
    } else {
      ElMessage.error('推理失败')
    }
  } catch (error) {
    ElMessage.error(`推理失败: ${error}`)
  } finally {
    isInferencing.value = false
  }
}

// 初始化时获取模型名称列表
onMounted(() => {
  fetchModels()
})

</script>

<template>
  <div class="common-layout">
    <el-container class="main-container" style="height: 100vh;">
      <el-header height="55px" style="border-bottom: 1px solid var(--el-border-color)">
        <div style="display: inline-flex; align-items: center; justify-content: center;">
          <el-icon :size="25" color="#606266">
            <Avatar />
          </el-icon>
          <el-text size="large" tag="b">肺部影像segment</el-text>
        </div>
      </el-header>

      <el-container>
        <!-- 选择模型部分 -->
        <el-aside width="15vw" style="border-right: 1px solid var(--el-border-color);">
          <el-button @click="fetchModels" type="primary" style="margin-left: 10px;">刷新</el-button>
        </el-aside>

        <!-- 上传图片与推理按钮 -->
        <el-main>
          <el-row>
            <el-col :span="11">
              <el-upload class="avatar-uploader" :before-upload="beforeAvatarUpload" :on-change="handleChange">
                <img v-if="imageUrl" :src="imageUrl" class="avatar" style="height: 25vw;width: 25vw;" />
                <el-icon v-else class="avatar-uploader-icon" style="height: 25vw;width: 25vw;">
                  <Plus />
                </el-icon>
              </el-upload>

              <el-select v-model="value" multiple clearable collapse-tags placeholder="选择推理的模型" size="large" style="width: 20vw">
                <el-option v-for="item in models" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>

              <el-button :disabled="isInferencing" :type="isInferencing ? 'info' : 'primary'" @click="startInference" plain style="width: 30vw; height: 4vw;">
                {{ isInferencing ? '推理中' : '开始推理' }}
              </el-button>
            </el-col>

            <!-- 推理结果展示 -->
            <el-col :span="11">
              <div class="pre_result_show" :style="{ width: veiw_len + 1 + 'vw', height: veiw_len + 'vw', overflowY: 'auto' }" style="border: 2px dashed rgb(159.5, 206.5, 255);border-radius: 6px;">
                <el-image v-for="(url, index) in pre_result_img_urls" :key="url" :src="url" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2" :initial-index="index" fit="cover" />
              </div>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.avatar-uploader .avatar { width: 178px; height: 178px; display: block; }
</style>
