# hsync
基于HTTP的文件同步工具

## 2017.10.12 update

- 添加配置文件夹忽略项

## 2017.10.18 update

- 添加服务器多目录支持
- 添加本地上传多服务器支持

## 2017.10.26 update

- 修复不能传送二进制文件的BUG
- 现在服务器端不需要配置文件 通过客户端进行设置
- 现在客户端可以传送同一个目录到多个服务器IP
- 添加CLI模式 可直接在命令行中调用
- 修改名字为 hsync
- 更新cli参数
- 修复文件打开BUG

## TODO List

- [x] 服务器全目录支持
- [x] 客户端多服务器支持
- [x] 添加CLI模式
- [ ] 远程执行命令
- [ ] 双向同步
- [ ] 严格模式
- [ ] 合并文件
- [ ] 本地监听
