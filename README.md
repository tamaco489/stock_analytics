## Container Image Build
---

<br>

Place and execute python & go for the target project.
```
docker build -t ${container-image-name} -f ./Dockerfile .
```

<br>

check container image.
```
$ docker images
REPOSITORY                     TAG       IMAGE ID       CREATED          SIZE
stock_analytics-ubuntu-20.04   0.0.1     fac09974ac69   32 seconds ago   1.35GB
```

<br>

start and access container.
```
docker run -it "stock_analytics-ubuntu-20.04:0.0.1" bash
```

<br>

python and go version check.
```
root@54ca80240479:/app# python --version
Python 3.9.16

root@54ca80240479:/app# go version
go version go1.18 linux/amd64
```

<br>

check project
```
root@54ca80240479:/app# find ./python/ -maxdepth 1 -type f -ls | egrep "py$|whl$"
    44443      4 -rwxr-xr-x   1 root     root          861 Jan  3 16:02 ./python/main.py
    44439    504 -rwxr-xr-x   1 root     root       515822 Jun 25  2022 ./python/TA_Lib-0.4.24-cp39-cp39-win_amd64.whl

root@54ca80240479:/app# find ./go/ -maxdepth 2 -type f -ls  | egrep "go$|mod$|sum$"
    44493      4 -rwxr-xr-x   1 root     root         1913 Jan  3 11:38 ./go/main.go
    44489      4 -rwxr-xr-x   1 root     root           83 Jan  2 19:01 ./go/go.mod
    44490      4 -rwxr-xr-x   1 root     root          163 Jan  2 19:01 ./go/go.sum
    44492      8 -rwxr-xr-x   1 root     root         4570 Jan  2 19:01 ./go/library/notify.go
```