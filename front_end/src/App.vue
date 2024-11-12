<script setup lang="tsx">

// 按钮，多选框的导入
import {Avatar, Menu as IconMenu, Plus, WarnTriangleFilled,CirclePlusFilled,CircleCloseFilled} from '@element-plus/icons-vue'
import {onMounted, ref, watch} from 'vue'
import type {CheckboxValueType, UploadProps, UploadUserFile} from 'element-plus'
// 展示预测结果的导入
import {ElIcon, ElImage, ElMessage, ElUpload} from 'element-plus'


// 上传图片的导入
import axios from 'axios'
import type Node from 'element-plus/es/components/tree/src/model/node'


// 预测结果显示的具体实现
const pre_result_img_urls = ref<string[]>([])

const img_len = ref(0)
const view_len = ref(0)
const img_len_view = ref(0)
const view_len_view = ref(0)

setListLength(pre_result_img_urls);

function sqrtAndCeil(x: number): number {
  // 首先计算平方根
  const sqrtValue = Math.sqrt(x);
  // 然后使用 Math.ceil 向上取整
  return Math.ceil(sqrtValue);
}

function setListLength(list: any) {

  let sp_number;
  sp_number = sqrtAndCeil(list.length)

  img_len.value = 25 / sp_number
  view_len.value = 26

}

function setViewListLength(list: any) {

  let sp_number;
  sp_number = sqrtAndCeil(list.length)

  img_len_view.value = 25 / sp_number
  view_len_view.value = 26

}

// 页面加载时向后端请求获取workspace数据
onMounted(async () => {
  try {
    // 请求后端获取 dataSource 数据
    const response = await axios.get('/api/workspace');
    workspace.value = response.data;
  } catch (error) {
    console.error('Failed to fetch workspace:', error);
  }
});


// 定义workspace数据的 Tree 类型
interface Tree {
  id: number
  label: string
  url?: string
  children?: Tree[]
}

let id = 1000


// 上传图片到服务器的具体实现
const imageUrl = ref('')
// 用于推理的图像列表
const uped_img_local_path = ref<any[]>([])

// 图片文件列表
const fileList = ref<UploadUserFile[]>([])

// 树的节点数据
const workspace = ref<Tree[]>([
  {
    id: 1,
    label: '工作区1',
    children: [],
  },
  {
    id: 2,
    label: '工作区2',
    children: [],
  },
  {
    id: 3,
    label: '工作区3',
    children: [],
  },
])

// 复选框选中的节点列表
const selectedNodes = ref<Tree[]>([])


// 上传图片并创建新节点
const append = async (data: Tree, files: File[]) => {
  try {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));

    // 上传图片数据到后端
    const response = await axios.post('/api/upload', formData);
    const uploadedFiles = response.data; // 接收图片路径和文件名
    handleAvatarSuccess(response.data)

    // 根据上传的文件创建新节点
    uploadedFiles.forEach((file: { name: string, url: string }) => {
      const newNode: Tree = {
        id: id++,
        label: file.name,
        url: file.url,
        children: [],
      };
      if (!data.children) data.children = [];
      data.children.push(newNode);
    });

    // 更新树形数据
    workspace.value = [...workspace.value];

    // 同步 dataSource 到后端
    await axios.post('/api/update-workspace', workspace.value);
  } catch (error) {
    console.error('Failed to append node:', error);
  }
};

// 获取需要增加节点的工作区
const appendNode = ref<Node>()
const getAppendNode = (node: Node) => {
  appendNode.value = node
  console.log(appendNode.value)
}

// 删除节点
const remove = (node: Node, data: Tree) => {
  const parent = node.parent
  const children: Tree[] = parent.data.children || parent.data
  const index = children.findIndex((d) => d.id === data.id)
  children.splice(index, 1)
  workspace.value = [...workspace.value]
}


// 图像元数据的列表
const imgList = ref<File[]>([])
let fileProcessing = false; // 标记文件是否正在处理中

// 实现图像选择的方法
const handleFileChange: UploadProps['beforeUpload'] = (file) => {
  imgList.value.push(file); // 将文件添加到 imgList

  // 如果没有在处理文件，则通过微任务批量处理
  if (!fileProcessing) {
    fileProcessing = true; // 标记为正在处理中
    Promise.resolve().then(() => {
      // 文件处理逻辑
      const rootNode = appendNode.value?.data as Tree // 假设选择的是第一个根节点

      append(rootNode, imgList.value);

      imgList.value.forEach((fileItem) => {

      });


      // 打印所有上传的文件
      console.log("上传的文件列表：", imgList.value);

      // 清空 imgList
      imgList.value = [];
      fileProcessing = false; // 重置标记
    });
  }

  return false; // 阻止默认上传行为
};

// 节点的渲染方法
const renderContent = (
    h: any,
    {node, data}: { node: Node; data: Tree }
) => {
  return (
      <span class="custom-tree-node">
      <span>{node.label}</span>
        {node.level === 1 && (
            <div style="position:relative">
              <el-upload
                  file-list={fileList.value}
                  class="upload-demo"
                  action="#"
                  multiple
                  limit={100}
                  before-upload={handleFileChange}
                  style="height:20px;width:60px;position: absolute;right:-30px"
                  show-file-list={false}
              >
                <div style="position: absolute;bottom:6.5px">
                  <el-icon color="#409eff" size="20px"
                         onClick={() => getAppendNode(node)}
                         ><CirclePlusFilled /></el-icon>
                </div>

              </el-upload>
              <div
                  style={{
                    marginLeft: '-10px',
                    position: 'absolute',
                    bottom: '-14px',
                    display: "none"
                  }}
              >
                <el-icon
                  color="#fc3d49"
                  size="20px"
                  onClick={() => remove(node, data)}
                ><CircleCloseFilled /></el-icon>
              </div>
            </div>
        )}
    </span>
  )
}

// 处理节点选择
const handleCheckChange = (node: Node, checked: boolean) => {
  if (checked) {
    selectedNodes.value.push(node)
  } else {
    selectedNodes.value = selectedNodes.value.filter((n) => n.id !== node.id)
  }
  uped_img_local_path.value = selectedNodes.value.map((node) => node.url);
  console.log("要用于推理的文件列表：", uped_img_local_path.value);
  setViewListLength(pre_result_img_urls);

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



const handleAvatarSuccess = (response: any) => {
  ElMessage.success('图片上传成功')
}

const beforeAvatarUpload = (rawFile: any) => {
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png' && rawFile.type !== 'image/fit') {
    ElMessage.error('Avatar picture must be JPG or PNG format!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('Avatar picture size can not exceed 2MB!')
    return false
  }
  return true
}

// const handleChange = (file: any) => {
//   const formData = new FormData()
//   formData.append('file', file.raw)
//   console.log(formData)
//
//   axios.post('/api/upload', formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data'
//     }
//   }).then((response) => {
//     if (response.status === 200) {
//       handleAvatarSuccess(response.data)
//       // console.log(response.data)
//       imageUrl.value = URL.createObjectURL(file.raw)
//       console.log(imageUrl.value)
//       // uped_img_local_path.value = response.data.file_path
//       //回传本地图片的路径
//     } else {
//       ElMessage.error('上传失败')
//     }
//   }).catch((error) => {
//     ElMessage.error(`上传失败: ${error}`)
//   })
// }


// 多选框的具体实现
const checkAll = ref(false)
const indeterminate = ref(false)
const selectedModels = ref<CheckboxValueType[]>([])//这个value绑定了多选框的选中值
const models = ref([
  {
    value: 'U-net',
    label: 'U-net',
  },
  {
    value: 'DeepLab',
    label: 'DeepLab',
  },
  {
    value: 'WeClip',
    label: 'WeClip',
  },
])
watch(selectedModels, (val) => {
  if (val.length === 0) {
    checkAll.value = false
    indeterminate.value = false
  } else if (val.length === models.value.length) {
    checkAll.value = true
    indeterminate.value = false
  } else {
    indeterminate.value = true
  }
})
const handleCheckAll = (val: CheckboxValueType) => {
  indeterminate.value = false
  if (val) {
    selectedModels.value = models.value.map((_) => _.value)
  } else {
    selectedModels.value = []
  }
}



// 触发推理请求
const isInferencing = ref(false) // 控制推理按钮的状态


const startInference = async () => {

  if (!uped_img_local_path.value || selectedModels.value.length === 0) {
    ElMessage.error('请上传图片并选择模型')
    return
  }

  isInferencing.value = true

  try {
    const response = await axios.post('/api/start', {
      image_url: uped_img_local_path.value,
      models: selectedModels.value,
    })
    console.log(response)

    if (response.status === 200) {
      ElMessage.success('推理完成')
      // pre_result_img_urls.value = response.data.result_images
      console.log(response.data)
      pre_result_img_urls.value = [
        ...response.data.Unet,
        ...response.data.deeplab,
        ...response.data.WeClip
      ]
      console.log("?")
      console.log(pre_result_img_urls.value)
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
// onMounted(() => {
//   fetchModels()
// })


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
        <el-aside width="15vw" style="border-right: 1px solid var(--el-border-color);">
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
                  default-expand-all
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