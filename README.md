# 项目名称：多功能API系统

## 项目简介

本项目是一个基于Flask框架的多功能API系统，旨在提供停车、化妆师品、食堂系统等多个领域的API接口。

## API接口列表

### 停车系统

* `/parking/add`: 添加新的停车信息
* `/parking/get`: 获取停车信息
* `/parking/update`: 更新停车信息
* `/parking/delete`: 删除停车信息

### 化妆师品系统

* `/cosmetics/add`: 添加新的化妆师品信息
* `/cosmetics/get`: 获取化妆师品信息
* `/cosmetics/update`: 更新化妆师品信息
* `/cosmetics/delete`: 删除化妆师品信息

### 食堂系统

* `/canteen/add`: 添加新的食堂信息
* `/canteen/get`: 获取食堂信息
* `/canteen/update`: 更新食堂信息
* `/canteen/delete`: 删除食堂信息

## 使用方法

1. 安装Flask框架：`pip install flask`
2. 克隆项目仓库：`git clone https://github.com/your-username/your-repo-name.git`
3. 进入项目目录：`cd your-repo-name`
4. 运行API服务器：`python app.py`
5. 使用API接口：使用工具如Postman或curl来访问API接口

## 依赖项

* Flask 1.1.2
* SQLite 3.32.3

