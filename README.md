# DeepSeek 标题修改器

一个简单的 Chrome 扩展程序，用于自动修改 DeepSeek 聊天页面的标题，使其与当前对话内容保持同步。

## 功能特点

- 自动监测并更新 DeepSeek 聊天页面的标题
- 使标题与当前对话内容保持一致
- 轻量级设计，低资源占用

## 安装说明

1. 下载此扩展程序的源代码
2. 打开 Chrome 浏览器，进入扩展程序管理页面（chrome://extensions/）
3. 开启右上角的"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择包含此扩展程序源代码的文件夹

## 使用方法

安装完成后，扩展程序会自动在 DeepSeek 聊天页面（chat.deepseek.com）运行。无需任何额外设置，页面标题将自动与对话内容同步。

## 技术说明

- 使用 Chrome Extension Manifest V2
- 仅在 DeepSeek 聊天页面（chat.deepseek.com）运行
- 使用内容脚本（Content Script）实现标题更新功能

## 权限说明

- `tabs`: 用于访问标签页信息
- `*://chat.deepseek.com/*`: 仅在 DeepSeek 聊天页面运行

## 版本信息

当前版本：1.0 