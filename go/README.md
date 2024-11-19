### LINE Notify (go)
---

Sending images using LINE Message API in go.

<br>

* Reserve
```
export LINE_NOTIFY_TOKEN='C7***************************************G9' LINE_NOTIFY_BASEURL='https://notify-api.line.me/api'
```
```
$ env | egrep "LINE_NOTIFY_TOKEN|LINE_NOTIFY_BASEURL"
LINE_NOTIFY_BASEURL=https://notify-api.line.me/api
LINE_NOTIFY_TOKEN=C7***************************************G9
```

<br>

* execute
```
cd ./go/
```

```
$ go run main.go
&{200 ok USER sample_user}
```