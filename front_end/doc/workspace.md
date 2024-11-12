### 获取 dataSource 数据(后端需要将保存的配置文件以json的形式发给前端)
- 接口 URL: /workspace
- 请求方法: GET
- 请求参数: 无
- 响应数据:
- 成功响应:HTTP 状态码: 200
- 响应体（JSON 格式）:
```json
[
  {
    "id": ,
    "label": ,
    "children": [
      {
        "id": ,
        "label": ,
        "url": ,
        "children": []
      },
    ]
  }
]
```
示例：
```json
[
  {
    "id": 1,
    "label": "工作区名",
    "children": [
      {
        "id": 2,
        "label": "文件名",
        "url": "图片存在本地的路径",
        "children": []
      },
    ]
  }
]
```
- 失败响应:HTTP 状态码: 500
- 响应体（JSON 格式）
```json
[]
```

### 更新 workspace 数据(前端发送workspace数据给后端保存)
- 接口 URL: /update-workspace
- 请求方法: POST
- 请求参数: 
```json
[
  {
    "id": ,
    "label": ,
    "children": [
      {
        "id": ,
        "label": ,
        "url": ,
        "children": []
      },
    ]
  }
]
```
- 响应数据:
- 成功响应:HTTP 状态码: 200
- 响应体（JSON 格式）:
```json
{
  "status": "success"
}

```
- 失败响应:HTTP 状态码: 500
- 响应体（JSON 格式）
```json
{
  "status": "error",
  "message": "Error details"
}


```
### 上传文件接口(前端上传文件给后端保存)
- 接口 URL: /upload
- 请求方法: POST
- 请求参数: 表单数据:files: 文件列表
```json
{
    files:
    [file1<File>, file2<File>, file3<File> .....]
}

```
- 响应数据:
- 成功响应:HTTP 状态码: 200
- 响应体（JSON 格式）:
```json
[
  {
    "name": "文件名",
    "url": "存在本地的路径"
  },
  {
    "name": "文件名",
    "url": "存在本地的路径"
  }
]

```
- 失败响应:HTTP 状态码: 500
- 响应体（JSON 格式）
```json
{
  "status": "error",
  "message": "Error"
}

```

