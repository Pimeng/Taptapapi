> [!WARNING]
> 看到这个项目请不要到处传，自己知道就好

# Taptap API Faker
## 介绍
由于 Taptap 官方API限制太多，难以抓包，于是我重新设计了一套API以供自己方便使用

***

## 食用方法
首先将本项目克隆下来   
``` bash
git clone https://github.com/Pimeng/taptapapi.git
```
然后使用这条命令安装本项目的依赖
``` bash
pip install .
```

or

```
pip install -r requirements.txt
```
完成后只需要使用
``` bash
python main.py
```
即可启动
> [!TIP]
> 默认监听`0.0.0.0:8080`，如有需要可以通过下面的方式修改

<details>
    <summary>1. 使用命令行参数</summary>
    启动方式

    ``` bash
    python main.py --host 127.0.0.1 --port 8000
    ```

</details>

<details>
    <summary>2. 使用环境变量</summary>

    ``` bash
    HOST=127.0.0.1 PORT=8000 python main.py
    ```

</details>

<details>
    <summary>3. 使用配置文件</summary>
    在根目录下创建config.json文件并按照如下编辑，其中 `host` 是监听IP地址， `port` 是监听端口


    ``` json
    {
        "host": "0.0.0.0",
        "port": "8080"
    }
    ```

</details>

***

## 开发文档
请访问   
[https://tapapi.talobot.top](https://tapapi.talobot.top)   
或者   
[https://pimeng.apifox.cn](https://pimeng.apifox.cn)   

## 致谢
 - [Taptap](https://www.taptap.cn)
 - Httpcanary
 - [ApiFox](https://apifox.com)