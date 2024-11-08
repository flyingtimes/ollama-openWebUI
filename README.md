## 我希望能够把macstudio、win、linux环境下的ollama+openWebUI尽量以docker的方式固化下来

### mac下的docker不支持调用GPU的能力，因此ollama使用原生mac版本的程序来跑，其他部分docker-compose-webuiONLY的方式跑起来
### windows/linux服务器带GPU的，用docker-compose-gpu方式跑起来
### 不具备GPU的服务器，使用docker-compose-cpu方式跑起来
'''
docker compose -f xx.yaml up -d
'''