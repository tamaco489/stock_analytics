#!/bin/bash
# =====================================
# Execution Preparation.
# =====================================
TMP=$(mktemp)
trap "rm -rf ${TMP}" EXIT
ERROR_COUNTER=0

PYTHON_TOOL=$(find ./python/main.py -type f | wc -l)
GO_TOOL=$(find ./go/main.go | wc -l)

PREPARATION() {
    if [ $PYTHON_TOOL -ne 1 ] || [ $GO_TOOL -ne 1 ]; then
        echo "[result:failed] No executable program exists."
        ERROR_COUNTER=$(($ENV_VARS_COUNTER+1))
        echo $ERROR_COUNTER >> $TMP
    fi

    ENV_VARS=($(env | egrep "LINE_NOTIFY_TOKEN|LINE_NOTIFY_BASEURL" | awk -F "=" '{print $1}'))
    ENV_VARS_COUNTER=$(echo ${#ENV_VARS[*]})

    if [ $ENV_VARS_COUNTER -lt 2 ]; then
        echo "[result:failed] Please reset the environment variables."
        echo "ex) export LINE_NOTIFY_TOKEN='C7***************************************G9' LINE_NOTIFY_BASEURL='https://notify-api.line.me/api'"
        ERROR_COUNTER=$(($ENV_VARS_COUNTER+1))
        echo $ERROR_COUNTER >> $TMP
    fi
}

PREPARATION_RESULT() {
    if [ $ERROR_COUNTER -eq 0 ] && [ $? -eq 0 ]; then
        echo "[result:success] No abnormalities. Execute the program."
    else
        echo "[result:failed] Cannot execute program. Terminates the verification script."
        exit 0
    fi
}


# =====================================
# Analyze with python program.
# =====================================
# pythonプログラムを実行
EXEC_PYTHON_ANALYZE() {
    echo "start."
    cd ./python/
    python main.py
    echo $?
    echo "end."
    cd -
}

# =====================================
# LINE Notification with Go Program.
# =====================================
# pythonプログラムが正常終了し、且つ./python/data/ディレクトリに「*.png」ファイルが生成されていることを確認
# goプログラムを実行




# PREPARATION > $TMP
PREPARATION
PREPARATION_RESULT
EXEC_PYTHON_ANALYZE
exit 0