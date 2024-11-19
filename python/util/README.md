### LINE Notify (python)
---

Sending images using LINE Message API in python.

<br>

* Reserve
```
export LINE_NOTIFY_TOKEN='C7***************************************G9'
```
```
$ env |grep "LINE_NOTIFY_TOKEN"
LINE_NOTIFY_TOKEN=C7***************************************G9
```

<br>

* execute
```
cd ./python/
```

```
$ python main.py
'check_line_notify_request' was successfully processed.
{'status': 200, 'message': 'ok', 'targetType': 'USER', 'target': 'hoge123'}
send: ./data/01_candle_chart_gree.inc.png
send: ./data/02_candle_sma_chart_gree.inc.png
send: ./data/03_bb_chart_gree.inc.png
'send_line_notify' was successfully processed.
{'status': 200, 'message': 'ok'}
```