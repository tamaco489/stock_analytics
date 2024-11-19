package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"stock_analytics/library"
	"time"
)

const (
	NOTIFY_ARCHIVE_DIR = "../python/data/"
	NOTIFY_MESSAGE     = "test message from golang."
)

var apiExecResult bool = false

func dirWalk(dir string) (pathList []string, err error) {
	files, err := ioutil.ReadDir(dir)
	if err != nil {
		return nil, err
	}

	var paths []string
	for _, file := range files {
		if file.IsDir() {
			pathList, err = dirWalk(filepath.Join(dir, file.Name()))
			if err != nil {
				return nil, err
			}
			paths = append(paths, pathList...)
			continue
		}
		paths = append(paths, filepath.Join(dir, file.Name()))
	}

	return paths, nil
}

func notify(ctx context.Context, pathList []string) (bool, error) {
	c := library.NewClient()
	for i, path := range pathList {
		fmt.Printf("[%d] %s\n", i, path)

		f, err := os.Open(path)
		if err != nil {
			return apiExecResult, fmt.Errorf("cannot open file. %q: %v\n", path, err)
		}
		defer f.Close()

		res, err := c.NotifyMessageAndImage(ctx, NOTIFY_MESSAGE, f)
		if err != nil {
			return apiExecResult, fmt.Errorf("failed notice api. %v\n", err)
		}
		fmt.Printf("[Debug:notify] res.Message: %s, res.Status: %d, res.RateLimit: %v, res.RateLimit.ImageLimit: %d, res.RateLimit.Limit: %d, res.RateLimit.Remaining: %d\n",
			res.Message, res.Status, res.RateLimit, res.RateLimit.ImageLimit, res.RateLimit.Limit, res.RateLimit.Remaining)

		apiExecResult = !apiExecResult
		time.Sleep(time.Second * 1)
	}

	return apiExecResult, nil
}

func main() {
	pathList, err := dirWalk(NOTIFY_ARCHIVE_DIR)
	if err != nil {
		panic(err)
	}

	ctx := context.TODO()
	apiExecResult, err := notify(ctx, pathList)
	if err != nil {
		panic(err)
	}

	if !apiExecResult {
		fmt.Println("unexpected error.")
	}

	fmt.Println("success line notify api")
}
