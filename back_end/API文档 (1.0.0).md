# api

## Clear

### url
- /api/clear

### method
- GET

清理所有预测结果目录，重新创建这些目录。

### 参数
- 无

### 请求示例
- GET 请求，无需传递任何参数。
```
bash
curl -X GET http://localhost:5000/api/clear
```
### 成功响应
- HTTP 状态码 200
- 响应体（字符串）: "0"

### 失败响应
- 如果在清理过程中发生错误，会捕获异常并继续执行后续操作。
- HTTP 状态码 200
- 响应体（字符串）: "0"


## GetWorkspace

### url
- /api/workspace

### method
- GET

获取 dataSource 数据

### 参数
- 无

### 请求示例
- GET 请求，无需传递任何参数。
```
bash
curl -X GET http://localhost:5000/api/workspace
```
### 成功响应
- HTTP 状态码 200
- 响应体（JSON 格式）: 包含工作区数据的 JSON 数组

### 失败响应
- HTTP 状态码 500
- 响应体（JSON 格式）: 空数组


## Start

### url
- /api/start

### method
- POST

开始预测接口，根据请求中的模型列表调用相应的预测函数，并返回预测结果的路径。

### 参数
| 参数名       | 必填 | 请求类型 | 类型   | 说明                           |
|--------------|------|----------|--------|--------------------------------|
| image_url    | 是   | json     | list   | 图像文件路径                   |
| models       | 是   | json     | list   | 需要使用的模型列表             |

### 请求示例
```
json
{
    "image_url": [
        "http://localhost:5000/api/static/uploaded/three_channel/ID_0188_Z_0137.png",
        "http://localhost:5000/api/static/uploaded/three_channel/ID_0189_Z_0132.png",
        "http://localhost:5000/api/static/uploaded/three_channel/ID_0190_Z_0070.png",
        "http://localhost:5000/api/static/uploaded/three_channel/ID_0191_Z_0140.png"
    ],
    "models": [
        "U-net",
        "DeepLab",
        "WeClip"
    ]
}
```
### 返回示例
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


## StaticFile

### url
- /api/static/&lt;path:filename&gt;

### method
- GET

发送静态文件接口，根据请求中的文件名返回相应的静态文件。

### 参数
| 参数名       | 必填 | 请求类型 | 类型   | 说明                           |
|--------------|------|----------|--------|--------------------------------|
| filename     | 是   | path     | str    | 文件名                         |

### 请求示例
- GET 请求，URL 中包含文件名。
- 例如：`http://localhost:5000/api/static/three_channel/ID_0188_Z_0137.png`

### 返回
- 返回指定的静态文件。
- 如果文件不存在，返回 404 错误。


## UpdateWorkspace

### url
- /api/update-workspace

### method
- POST

更新 workspace 数据

### 参数
| 参数名       | 必填 | 请求类型 | 类型   | 说明                           |
|--------------|------|----------|--------|--------------------------------|
| data         | 是   | json     | list   | 包含工作区数据的 JSON 数组     |

### 请求示例
```
json
{
    "data": [
        {
            "id": 1,
            "name": "Image1",
            "url": "http://localhost:5000/api/static/uploaded/three_channel/image1.png"
        },
        {
            "id": 2,
            "name": "Image2",
            "url": "http://localhost:5000/api/static/uploaded/three_channel/image2.png"
        }
    ]
}
```
### 成功响应
- HTTP 状态码 200
- 响应体（JSON 格式）: {"status": "success"}

### 失败响应
- HTTP 状态码 500
- 响应体（JSON 格式）: {"status": "error", "message": "Error details"}


## Upload

### url
- /api/upload

### method
- POST

上传文件接口

### 参数
| 参数名       | 必填 | 请求类型 | 类型   | 说明                           |
|--------------|------|----------|--------|--------------------------------|
| files        | 是   | form-data | list   | 文件列表                       |

### 请求示例
```
bash
curl -X POST http://localhost:5000/api/upload -F "files=@/path/to/image1.png" -F "files=@/path/to/image2.png"
```
### 成功响应
- HTTP 状态码 200
- 响应体（JSON 格式）: 包含上传文件信息的 JSON 数组
```
json
[
    {
        "name": "image1.png",
        "url": "http://localhost:5000/api/static/uploaded/three_channel/image1.png"
    },
    {
        "name": "image2.png",
        "url": "http://localhost:5000/api/static/uploaded/three_channel/image2.png"
    }
]
```
### 失败响应
- HTTP 状态码 400
- 响应体（JSON 格式）: {"status": "error", "message": "No file part in the request"}

- HTTP 状态码 500
- 响应体（JSON 格式）: {"status": "error", "message": "Error"}




