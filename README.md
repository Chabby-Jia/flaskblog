## flask-blog
## 安装依赖

`pip install -r requirements.txt`

## 生产环境部署

安装uwsgi

`pip install uwsgi`

启动uwsgi

`uwsgi --ini uwsgi.ini`


3、配置nginx做转发
    
`nginx.conf`
```
server{
    listen 80;
    server_name yourname;
    location / {
        proxy_pass http://127.0.0.1:5000; 
    }
}
```

## docker环境部署

`docker build -t blog .`

**替换host为宿主机代码目录**

`docker run -d --name blog -p 39005:5000 -p 39006:9191 -v <you host>:/home/blog blog uwsgi --ini ./uwsgi.ini`
    
