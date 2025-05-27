
# Data-Copilot Steps
✨ **An *Interpretable* Natural Language Database Query System (RAG) for Large Language Models (LLM)**
Query databases using natural language, intelligently parse database structures with large language models, perform structured multi-table queries and statistical calculations on data, and intelligently generate various types of charts based on query results. The entire generation process is open, modifiable, and interpretable, achieving reliable natural language data analysis.
Pywebio interactive front-end web page, no need for OpenAI API, 100% pure Python code.
🚩 [简体中文](./README.md)

[📺 Project Online Demonstration Link](http://www.bytesc.top:8037/)

### Related Projects
- [Natural Language Database Query System (RAG) based on Large Language Models (LLM) and Concurrent Prediction Models](https://github.com/bytesc/data-copilot-v2)

🚩[Personal Website: www.bytesc.top](http://www.bytesc.top)
🔔 If you have any questions about the project, please feel free to raise an `issue` in this project. I usually reply within 24 hours.

## Function Overview
- 1. Query using natural language
- 2. Implement multi-table structured queries and statistical calculations
- 3. Intelligent generation of various types of ECharts
- 4. Intelligent parsing of database structures, no extra configuration needed for different MySQL databases
- 5. ✨ The entire generation process is open, modifiable, and interpretable, achieving reliable natural language data analysis
- 6. Handle anomalies such as instability in large language models
- 7. Support local offline deployment (requires GPU) for `huggingface` format models (e.g., `qwen-7b`)
- 8. Support `openai` format (e.g., `glm`, `deepseek`) and dashscope `qwen` API interfaces

## Technical Innovations
- Independent from frameworks like langchain, completely open implementation
- ✨ The entire generation process is open, modifiable, and interpretable, achieving reliable natural language data analysis

## How to Use

### Install Dependencies
Python version 3.10
```bash
pip install -r requirement.txt
```

### Fill in Configuration Information
`./config/config.yaml` is the configuration file.

#### Database Configuration
Connect and the model will automatically read the database structure without extra configuration
```yml
mysql: mysql+pymysql://root:123456@127.0.0.1/data_copilot
# mysql: mysql+pymysql://username:password@address:port/databasename
```

#### Large Language Model Configuration
If using the `deepseek` API (recommended)
```yml
llm:
  model_provider: openai #qwen #openai
  model: deepseek-chat
  url: "https://api.deepseek.com/v1/"
# https://api-docs.deepseek.com/
```
If using the OpenAI API (here you fill in the OpenAI-compatible API for glm)
```yml
llm:
  model_provider: openai
  model: glm-4
  url: "https://open.bigmodel.cn/api/paas/v4/"
# glm-4
# https://open.bigmodel.cn
```
For local offline deployment, the relevant code is in `./llm_access/qwen_access.py`

#### Obtain API Key
If using the `openai` format API's API-key
If obtaining the `deepseek` large language model API-key from the [deepseek-api official website](https://api-docs.deepseek.com/)
If obtaining the `chatglm` large language model API-key from the [bigmodel official website](https://open.bigmodel.cn/)
Save the `api-key` to `llm_access/api_key_openai.txt`

### Run
`main.py` is the entry point of the project. Run this file to start the server.
```bash
python main.py
```

## Interface Display
Intelligently parse the structure of any database, and the user inputs natural language questions
![](./readme_img/img1.png)
LLM intelligently generates SQL, and the user checks and executes it
![](./readme_img/img2.png)
If you are not satisfied with the query results, you can modify or regenerate the SQL
![](./readme_img/img3.png)
LLM intelligently generates the Python code for plotting
![](./readme_img/img4.png)
Automatic plotting
![](./readme_img/img5.png)

![](./readme_img/imga.png)
![](./readme_img/imgb.png)
![](./readme_img/imgc.png)

# Open Source License
This translation is for reference only. The English version in the LICENSE file prevails.
MIT Open Source License:
Copyright (c) 2025 bytesc
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
