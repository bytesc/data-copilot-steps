# data-copilot-steps

✨ **大语言模型 (LLM) 的*<u>可解释型</u>*自然语言数据库查询系统 (RAG)**

通过自然语言提问，使用大语言模型智能解析数据库结构，对数据进行智能多表结构化查询和统计计算，根据查询结果智能绘制多种图表。
生成链路过程完全开放可修改，可解释，实现可靠的自然语言数据分析。
Pywebio 交互式前端网页，不必须 openai api，100%纯 Python 代码。 

🚩[English Readme](./README.en.md)

[📺项目在线演示连接](http://www.bytesc.top:8037/) 

### 相关项目
- [基于大语言模型 (LLM)和并发预测模型的自然语言数据库查询系统 (RAG) https://github.com/bytesc/data-copilot-v2](https://github.com/bytesc/data-copilot-v2)
- [基于代码生成和函数调用(function call)的大语言模型(LLM)智能体 https://github.com/bytesc/data-copilot-functions](https://github.com/bytesc/data-copilot-functions)]()

🚩[个人网站：www.bytesc.top](http://www.bytesc.top) 


🔔 如有项目相关问题，欢迎在本项目提出`issue`，我一般会在 24 小时内回复。


## 功能简介

- 1, 使用自然语言提问
- 2, 实现多表结构化查询和统计计算
- 3, 实现智能绘制多种类型的 echart 图表制作
- 4, 智能解析数据库结构，使用不同的 mysql 数据库无需额外配置
- 5, ✨ 生成链路过程完全开放可修改，可解释，实现可靠的自然语言数据分析
- 6, 能够处理大语言模型表现不稳定等异常情况
- 7, 支持本地离线部署 (需 GPU) `huggingface` 格式模型 (例如`qwen-7b`) 
- 8, 支持 `openai` 格式(如 `glm` ,`deepseek`)和 dashscope `qwen` 的 api 接口

## 技术创新点

- 脱离 langchain 等框架，完全开放实现
- ✨ 生成链路过程完全开放可修改，可解释，实现可靠的自然语言数据分析


## 如何使用

### 安装依赖

python 版本 3.10

```bash
pip install -r requirement.txt
```

### 填写配置信息

`./config/config.yaml` 是配置信息文件。

#### 数据库配置
连接即可，模型会自动读取数据库结构，无需额外配置
```yml
mysql: mysql+pymysql://root:123456@127.0.0.1/data_copilot
# mysql: mysql+pymysql://用户名:密码@地址:端口/数据库名
```

#### 大语言模型配置
如果使用 `deepseek` api （推荐）
```yml
llm:
  model_provider: openai #qwen #openai
  model: deepseek-chat
  url: "https://api.deepseek.com/v1/"

# https://api-docs.deepseek.com/
```


如果使用 openai api （此处填写的是 glm 的 openai 兼容 api）

```yml
llm:
  model_provider: openai
  model: glm-4
  url: "https://open.bigmodel.cn/api/paas/v4/"

# glm-4
# https://open.bigmodel.cn
```

如果需要本地离线部署，相关代码在 `./llm_access/qwen_access.py`

#### 获取 apikey

如果使用 `openai` 格式 api 的 api-key

如果从[deepseek-api 官网](https://api-docs.deepseek.com/)获取 `deepseek` 大语言模型的 api-key

如果从[bigmodel 官网](https://open.bigmodel.cn/)获取 `chatglm` 大语言模型的 api-key


保存 `api-key` 到 `llm_access/api_key_openai.txt`

### 运行

main.py 是项目入口，运行此文件即可启动服务器

```bash
python main.py 
```

## 界面展示

智能解析任意数据库的结构，用户输入自然语言问题
![](./readme_img/img1.png)

LLM 智能生成 SQL，用户检查后执行 
![](./readme_img/img2.png)

如果对查询结果不满意，可以修改或者重新生成 sql
![](./readme_img/img3.png)

LLM 智能生成绘图的 python 代码
![](./readme_img/img4.png)

自动绘图
![](./readme_img/img5.png)

![](./readme_img/imga.png)
![](./readme_img/imgb.png)
![](./readme_img/imgc.png)

# 开源许可证

此翻译版本仅供参考，以 LICENSE 文件中的英文版本为准

MIT 开源许可证：

版权所有 (c) 2025 bytesc

特此授权，免费向任何获得本软件及相关文档文件（以下简称“软件”）副本的人提供使用、复制、修改、合并、出版、发行、再许可和/或销售软件的权利，但须遵守以下条件：

上述版权声明和本许可声明应包含在所有副本或实质性部分中。

本软件按“原样”提供，不作任何明示或暗示的保证，包括但不限于适销性、特定用途适用性和非侵权性。在任何情况下，作者或版权持有人均不对因使用本软件而产生的任何索赔、损害或其他责任负责，无论是在合同、侵权或其他方面。

