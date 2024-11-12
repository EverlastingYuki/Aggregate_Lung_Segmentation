# api

## Clear

### url
- /api/clear

### method
- GET

清理所有预测结果目录，重新创建这些目录。

### args
- 无

### request
- GET 请求，无需传递任何参数。

### return
- 成功清理目录后返回字符串 `"0"`。
- 如果在清理过程中发生错误，会捕获异常并继续执行后续操作。


## SendImage

### url
- /api/static/result/&lt;model_name&gt;/&lt;path:filename&gt;

### method
- GET

发送图像，根据请求中的模型名称和文件名返回相应的图像文件。

### args
|  args          | required | request type | type |  remarks                  |
|----------------|----------|--------------|------|---------------------------|
| model_name     |  true    |    path      | str  | 模型名称  |
| filename       |  true    |    path      | str  | 文件名  |

### request
- GET 请求，URL 中包含模型名称和文件名。

### return
- 返回指定模型的预测结果图像文件。
- 如果模型名称无效，返回错误信息和状态码 404。


## Start

### url
- /api/start

### method
- POST

开始预测接口，根据请求中的模型列表调用相应的预测函数，并返回预测结果的路径。

### args
|  args          | required | request type | type |  remarks                  |
|----------------|----------|--------------|------|---------------------------|
| image_url      |  true    |    json      | str  | 图像文件路径  |
| models         |  true    |    json      | list | 需要使用的模型列表  |

### request
```
json
{"image_url": "", "models": ["U-net", "DeepLab", "WeClip"]}
```
### return
```
json
{
    "Unet": [
        "./static/result/Unet/ID_0188_Z_0137.png"
    ],
    "Unet_WeClip": [],
    "WeClip": [],
    "deeplab": [
        "./static/result/deeplab/ID_0188_Z_0137.png"
    ],
    "deeplab_Unet": [
        "./static/result/deeplab_Unet/ID_0188_Z_0137.png"
    ],
    "deeplab_Unet_WeClip": [],
    "deeplab_WeClip": [],
    "original": [
        "./static/result/original/ID_0188_Z_0137.png"
    ]
}
```
- 返回一个 JSON 对象，包含原始图像路径和每个模型的预测结果路径。


## Upload

### url
- /api/upload

### method
- POST

上传文件接口，用于接收前端上传的图像文件，并根据图像的通道数保存为不同的路径。

### args
|  args          | required | request type | type |  remarks                  |
|----------------|----------|--------------|------|---------------------------|
| file           |  true    |    form-data | file | 需要上传的图像文件  |

### request
- 表单数据，包含一个名为 `file` 的字段，用于上传图像文件。

### return
```
json
{
    "message": "File uploaded successfully"
}
```
- 成功上传文件后返回的消息。
- 如果请求中没有文件部分，则返回错误信息和状态码 400。




