// src/stores/treeStore.tsx
import {defineStore} from 'pinia';
import {computed, onMounted, reactive, ref, watchEffect} from 'vue';
import axios from 'axios';
import type {CheckboxValueType, UploadProps, UploadUserFile} from 'element-plus';
import {ElMessage, ElPopover} from 'element-plus';
import {CircleCloseFilled, Edit, Plus} from '@element-plus/icons-vue';
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
    const _rename_popover = ref();
    const _rename_button_ref = ref();
    const _renamed_workspace = ref<string>('');

    const workspace = ref<Tree[]>([
        {id: 1, label: '工作区1', children: []},
        {id: 2, label: '工作区2', children: []},
        {id: 3, label: '工作区3', children: []},
    ]);
    const new_workspace_name = ref("");
    const selectedNodes = ref<Tree[]>([]);
    const pre_result_img_urls = ref<string[]>([]);
    const pre_results = reactive({
        Unet: [],
        Unet_WeClip: [],
        WeClip: [],
        deeplab: [],
        deeplab_Unet: [],
        deeplab_Unet_WeClip: [],
        deeplab_WeClip: [],
    });
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
        if (!['image/jpeg', 'image/png', 'image/tiff'].includes(file.type)) {
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

    const _updateBackendWorkspace = async () => {
        try {
            await axios.post('/api/update-workspace', workspace.value);
        } catch (error) {
            console.error('Failed to update workspace:', error);
        }
    };
    const _append = async (data: Tree, files: File[]) => {
        try {
            const formData = new FormData();
            files.forEach((file) => formData.append('files', file));
            const response = await axios.post('/api/upload', formData);
            handleAvatarSuccess(response.data);

            const uploadedFiles = response.data;
            uploadedFiles.forEach((file: {
                name: string,
                url: string
            }) => {
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
    // 使用 data.id 在 workspace 中查找并删除对应节点
    const findAndRemoveNode = (tree: Tree[], id: number) => {
        for (let i = 0; i < tree.length; i++) {
            if (tree[i].$treeNodeId === id) {
                tree.splice(i, 1); // 删除找到的节点
                return true; // 停止递归
            }
            if (tree[i].children) {
                const found = findAndRemoveNode(tree[i].children, id);
                if (found) return true;
            }
        }
        return false; // 未找到节点
    };
    findAndRemoveNode(workspace.value, data.id);
};
    const _printNode = (node:any) => {
        console.log("打印节点：", node);
    };

    const removeSelectedNodes = () => {
        selectedNodes.value.forEach((node) => {
            const temp_node = ref<Tree>(
                {
                    id: node.$treeNodeId,
                    label: node.label,
                    url: node.url,
                }
            )
            _remove(node, temp_node.value);
        });
        selectedNodes.value = [];
        workspace.value = [...workspace.value];
        _updateBackendWorkspace();
        uped_img_local_path.value = [];
    };
    const createNewWorkspace = () => {
        const newWorkspace: Tree = {
            id: _id.value++,
            label: new_workspace_name.value,
            children: [],
        };
        workspace.value.push(newWorkspace);
        workspace.value = [...workspace.value];
        _updateBackendWorkspace();
    };
    const refreshNewWorkspaceName = () => {
        new_workspace_name.value = "";
    };

    const sqrtAndCeil = (x: number) => Math.ceil(Math.sqrt(x));
    const setListLength = (list: any) => {
        // const sp_number = sqrtAndCeil(list.length);
        img_len.value = 25.8 / 7;
        view_len.value = 26;
    };
    const setViewListLength = (list: any) => {
        const sp_number = sqrtAndCeil(list.value.length);
        img_len_view.value = 25 / sp_number;
        view_len_view.value = 26;
    };
    // 上传图片
    const updateNodeLabel = (id: number, newLabel: string) => {
        console.log("id: ", id);
        const node = workspace.value.find(item => item.$treeNodeId === id);
        console.log("node: ", node);
        console.log("newLabel: ", newLabel)
        if (node) {
            node.label = newLabel; // 直接更新 workspace 中的 label
            workspace.value = [...workspace.value]; // 强制更新，确保视图刷新
        }
    };

    const handleAvatarSuccess = (response: any) => {
        ElMessage.success('图片上传成功');
    };
    const renderContent = (h: any, {node, data}: {
        node: Node;
        data: Tree
    }) => {
        const newLabel = ref(node.label);
        return (
            <span
                style={{
                    flex: "1",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    fontSize: "12px"
                }}
            >
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
                            style="height:20px;width:60px;position:absolute;right:-2vh;top:1.3vh"
                        >
                            <div style="position: absolute;bottom:1.5vh">
                                <el-tooltip content="添加图片" placement="top" effect="light">
                                    <el-button type="primary" icon={Plus} circle
                                               style="width: 2.2vh;height: 2.2vh;align-content: center"
                                               onClick={() => _getAppendNode(node)}
                                    />
                                </el-tooltip>
                            </div>
                        </el-upload>
                        <ElPopover placement="bottom" width={240} trigger="click" title="重命名">
                            {{
                                reference: () => (
                                    <el-button type="success" icon={Edit} circle
                                               style="width: 2.2vh;height: 2.2vh;align-content: center;margin-right:0.75vh"
                                    />
                                ),
                                default: () => <div>
                                    <el-input
                                        v-model={newLabel.value}
                                        style="width: 220px"
                                        placeholder="请输入新的名称"
                                        prefix-icon={Edit}
                                        onInput={() => updateNodeLabel(node.data.$treeNodeId, newLabel.value)}
                                        onBlur={() => _updateBackendWorkspace()}
                                    />
                                </div>
                            }}
                        </ElPopover>

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
            let temp_node = selectedNodes.value[i];

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
                pre_results.Unet = response.data.Unet;
                pre_results.deeplab = response.data.deeplab;
                pre_results.WeClip = response.data.WeClip;
                pre_results.Unet_WeClip = response.data.Unet_WeClip;
                pre_results.deeplab_Unet = response.data.deeplab_Unet;
                pre_results.deeplab_WeClip = response.data.deeplab_WeClip;
                pre_results.deeplab_Unet_WeClip = response.data.deeplab_Unet_WeClip;
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
        new_workspace_name,
        pre_results,
        renderContent,
        handleCheckChange,
        handleCheckAll,
        startInference,
        setListLength,
        setViewListLength,
        createNewWorkspace,
        refreshNewWorkspaceName,
        removeSelectedNodes,
    };
});
