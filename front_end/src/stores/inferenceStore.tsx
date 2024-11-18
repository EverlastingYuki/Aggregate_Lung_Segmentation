// src/stores/treeStore.tsx
import {defineStore} from 'pinia';
import {computed, onMounted, ref, watchEffect} from 'vue';
import axios from 'axios';
import type {CheckboxValueType, UploadProps, UploadUserFile} from 'element-plus';
import {ElMessage} from 'element-plus';
import {CircleCloseFilled, CirclePlusFilled} from '@element-plus/icons-vue';
import type Node from 'element-plus/es/components/tree/src/model/node';

// 定义 Tree 数据结构
interface Tree {
    id: number;
    label: string;
    url?: string;
    children?: Tree[];
}

export const useInferenceStore = defineStore('useInferenceStore', () => {
    const _id = ref(1000);
    const _imgList = ref<File[]>([]);
    const _fileProcessing = ref(false);
    const _fileList = ref<UploadUserFile[]>([]);
    const _appendNode = ref<Node | null>(null);

    const workspace = ref<Tree[]>([
        {id: 1, label: '工作区1', children: []},
        {id: 2, label: '工作区2', children: []},
        {id: 3, label: '工作区3', children: []},
    ]);
    const selectedNodes = ref<Tree[]>([]);
    const pre_result_img_urls = ref<string[]>([]);
    const uped_img_local_path = ref<string[]>([]);
    const img_len = ref(0);
    const view_len = ref(0);
    const img_len_view = ref(0);
    const view_len_view = ref(0);
    const checkAll = ref(false);
    const indeterminate = ref(false);
    const selectedModels = ref<CheckboxValueType[]>([]);
    const models = ref([
        {value: 'U-net', label: 'U-net'},
        {value: 'DeepLab', label: 'DeepLab'},
        {value: 'WeClip', label: 'WeClip'},
    ]);
    const isInferencing = ref(false);

    const _handleFileChange: UploadProps['beforeUpload'] = (file) => {
        if (!['image/jpeg', 'image/png', 'image/tif'].includes(file.type)) {
            ElMessage.error('图片格式必须为 JPG、PNG 或 TIF');
            return false;
        }

        _imgList.value.push(file);

        if (!_fileProcessing.value) {
            _fileProcessing.value = true;
            Promise.resolve().then(() => {
                const rootNode = _appendNode.value?.data as Tree;
                _append(rootNode, _imgList.value);
                _imgList.value.forEach((fileItem) => {
                });
                console.log("上传的文件列表：", _imgList.value);
                _imgList.value = [];
                _fileProcessing.value = false;
            });
        }
        return false;
    };
    const _append = async (data: Tree, files: File[]) => {
        try {
            const formData = new FormData();
            files.forEach((file) => formData.append('files', file));
            const response = await axios.post('/api/upload', formData);
            handleAvatarSuccess(response.data);

            const uploadedFiles = response.data;
            uploadedFiles.forEach((file: { name: string, url: string }) => {
                const newNode: Tree = {
                    id: _id.value++,
                    label: file.name,
                    url: file.url,
                    children: [],
                };
                if (!data.children) data.children = [];
                data.children.push(newNode);
            });
            workspace.value = [...workspace.value];
            await axios.post('/api/update-workspace', workspace.value);
        } catch (error) {
            console.error('Failed to append node:', error);
        }
    };
    const _getAppendNode = (node: Node) => {
        _appendNode.value = node;
    };
    const _remove = (node: Node, data: Tree) => {
        const parent = node.parent;
        const children: Tree[] = parent.data.children || parent.data;
        const index = children.findIndex((d) => d.id === data.id);
        children.splice(index, 1);
        workspace.value = [...workspace.value];
    };
    const sqrtAndCeil = (x: number) => Math.ceil(Math.sqrt(x));
    const setListLength = (list: any) => {
        const sp_number = sqrtAndCeil(list.length);
        img_len.value = 25 / sp_number;
        view_len.value = 26;
    };
    const setViewListLength = (list: any) => {
        const sp_number = sqrtAndCeil(list.value.length);
        img_len_view.value = 25 / sp_number;
        view_len_view.value = 26;
    };
    // 上传图片
    const handleAvatarSuccess = (response: any) => {
        ElMessage.success('图片上传成功');
    };
    const renderContent = (h: any, {node, data}: { node: Node; data: Tree }) => {
        return (
            <span class="custom-tree-node">
        <span>{node.label}</span>
                {node.level === 1 ? (
                    <div style="position:relative">
                        <el-upload
                            file-list={_fileList.value}
                            action="#"
                            multiple
                            limit={100}
                            before-upload={_handleFileChange}
                            show-file-list={false}
                            style="height:20px;width:60px;position:absolute;right:-30px"
                        >
                            <div style="position: absolute;bottom:6.5px">
                                <el-icon color="#409eff" size="20px"
                                         onClick={() => _getAppendNode(node)}
                                ><CirclePlusFilled/></el-icon>
                            </div>
                        </el-upload>
                        <div
                            style={{
                                marginLeft: '-10px',
                                position: 'absolute',
                                bottom: '-14px',
                                display: 'none'
                            }}
                        >
                            <el-icon
                                color="#fc3d49"
                                size="20px"
                                onClick={() => _remove(node, data)}
                            ><CircleCloseFilled/></el-icon>
                        </div>
                    </div>
                ) : (
                    <div style="position:relative">
                        <div
                            style={{
                                marginLeft: '-13.5vw',
                                position: 'absolute',
                                bottom: '-14px'
                            }}
                        >
                            <img src={data.url} style="width: 25px;height: 25px" alt=""/>
                        </div>
                    </div>
                )}
      </span>
        );
    };
    const handleCheckChange = (node: Node, checked: boolean) => {
        if (checked) {
            selectedNodes.value.push(node)
        } else {
            selectedNodes.value = selectedNodes.value.filter((n) => n.id !== node.id)
        }
        uped_img_local_path.value = [];  // 初始化为一个空数组
        for (let i = 0; i < selectedNodes.value.length; i++) {
            const temp_node = selectedNodes.value[i];

            // 判断 node.url 是否为 string 类型
            if (typeof temp_node.url === 'string') {
                uped_img_local_path.value.push((temp_node.url));
            }
        }
        console.log("要用于推理的文件列表：", uped_img_local_path.value);
        setViewListLength(uped_img_local_path);
    };
    const handleCheckAll = (val: CheckboxValueType) => {
        indeterminate.value = false;
        selectedModels.value = val ? models.value.map((m) => m.value) : [];
    };
    const startInference = async () => {
        if (!uped_img_local_path.value.length || !selectedModels.value.length) {
            ElMessage.error('请上传图片并选择模型');
            return;
        }

        isInferencing.value = true;
        try {
            const response = await axios.post('/api/start', {
                image_url: uped_img_local_path.value,
                models: selectedModels.value,
            });

            if (response.status === 200) {
                ElMessage.success('推理完成');
                pre_result_img_urls.value = [
                    ...response.data.Unet,
                    ...response.data.deeplab,
                    ...response.data.WeClip,
                ];
                setListLength(pre_result_img_urls);
            } else {
                ElMessage.error('推理失败');
            }
        } catch (error) {
            ElMessage.error(`推理失败: ${error}`);
        } finally {
            isInferencing.value = false;
        }
    };


    const isAllChecked = computed(() => selectedModels.value.length === models.value.length);
    const isNoneChecked = computed(() => selectedModels.value.length === 0);


    watchEffect(() => {
        if (isNoneChecked.value) {
            checkAll.value = false;
            indeterminate.value = false;
        } else if (isAllChecked.value) {
            checkAll.value = true;
            indeterminate.value = false;
        } else {
            indeterminate.value = true;
        }
    });
    onMounted(async () => {
  try {
    // 请求后端获取 dataSource 数据
    const response = await axios.get('/api/workspace');
    workspace.value = response.data;
  } catch (error) {
    console.error('Failed to fetch workspace:', error);
  }
});
    return {
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
        isInferencing,
        renderContent,
        handleCheckChange,
        handleCheckAll,
        startInference,
        setListLength,
        setViewListLength,
    };
});
