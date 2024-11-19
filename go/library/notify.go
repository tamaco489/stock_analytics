package library

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/google/uuid"
)

// LINE Notify API Document
// https://notify-bot.line.me/doc/ja/

const (
	GET_REQUEST_CONTENT_TYPE  = "application/json"
	POST_REQUEST_CONTENT_TYPE = "application/x-www-form-urlencoded"
)

var (
	baseURL                     string
	accessToken                 string
	ErrNotifyInvalidAccessToken = errors.New("invalid access token")
)

func init() {
	accessToken = os.Getenv("LINE_NOTIFY_TOKEN")
	baseURL = os.Getenv("LINE_NOTIFY_BASEURL")
}

type Client struct {
	HTTPClient *http.Client
}

func NewClient() *Client {
	return &Client{HTTPClient: http.DefaultClient}
}

type Request struct {
	Method string
	Path   string
}

func NewRequest(method, path string, data interface{}) *Request {
	return &Request{
		Method: method,
		Path:   path,
	}
}

type RateLimit struct {
	Limit          int
	Remaining      int
	ImageLimit     int
	ImageRemaining int
	Reset          time.Time
}

type NotifyResponse struct {
	Status    int    `json:"status"`
	Message   string `json:"message"`
	RateLimit RateLimit
}

func (c *Client) NotifyMessageOnly(ctx context.Context, message string) (*NotifyResponse, error) {
	return c.NotifyWithImageURL(ctx, message, "", "")
}

func (c *Client) NotifyMessageAndImage(ctx context.Context, message string, image io.Reader) (*NotifyResponse, error) {
	body, contentType, err := c.NotifyRequestBodyWithImage(message, image)
	if err != nil {
		return nil, err
	}
	return c.NotifyRequest(ctx, body, contentType)
}

func (c *Client) NotifyWithImageURL(ctx context.Context, message, imageThumbnail, imageFullSize string) (*NotifyResponse, error) {
	body, contentType := c.NotifyRequestBody(message, imageThumbnail, imageFullSize)
	return c.NotifyRequest(ctx, body, contentType)
}

func (c *Client) NotifyRequest(ctx context.Context, body io.Reader, contentType string) (*NotifyResponse, error) {
	url := baseURL + "/notify"

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, body)
	if err != nil {
		return nil, fmt.Errorf("failed to new request: %w", err)
	}

	req.Header.Set("Content-Type", contentType)
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", accessToken))

	res, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to notify: %w", err)
	}
	defer res.Body.Close()

	nRes := &NotifyResponse{}
	if err = json.NewDecoder(res.Body).Decode(nRes); err != nil {
		return nil, fmt.Errorf("failed to decode notification response: %w", err)
	}

	nRes.RateLimit.Parse(res.Header)

	if res.StatusCode == http.StatusUnauthorized {
		return nRes, ErrNotifyInvalidAccessToken
	}

	if res.StatusCode != http.StatusOK {
		return nRes, errors.New(nRes.Message)
	}

	return nRes, nil
}

func (c *Client) NotifyRequestBody(message, imageThumbnail, imageFullSize string) (io.Reader, string) {
	v := url.Values{}
	v.Add("message", message)

	if imageThumbnail != "" {
		v.Add("imageThumbnail", imageThumbnail)
	}

	if imageFullSize != "" {
		v.Add("imageFullsize", imageFullSize)
	}

	return strings.NewReader(v.Encode()), POST_REQUEST_CONTENT_TYPE
}

func (c *Client) NotifyRequestBodyWithImage(message string, image io.Reader) (io.Reader, string, error) {
	var b bytes.Buffer
	w := multipart.NewWriter(&b)

	if err := w.WriteField("message", message); err != nil {
		return nil, "", err
	}

	randomID, err := uuid.NewRandom()
	if err != nil {
		return nil, "", err
	}

	fw, err := w.CreateFormFile("imageFile", randomID.String())
	if err != nil {
		return nil, "", err
	}

	if _, err = io.Copy(fw, image); err != nil {
		return nil, "", err
	}

	if err = w.Close(); err != nil {
		return nil, "", err
	}

	return &b, w.FormDataContentType(), nil
}

func (r *RateLimit) Parse(header http.Header) {
	if v, err := strconv.Atoi(header.Get("X-RateLimit-Limit")); err == nil {
		r.Limit = v
	}

	if v, err := strconv.Atoi(header.Get("X-RateLimit-Remaining")); err == nil {
		r.Remaining = v
	}

	if v, err := strconv.Atoi(header.Get("X-RateLimit-ImageLimit")); err == nil {
		r.ImageLimit = v
	}

	if v, err := strconv.Atoi(header.Get("X-RateLimit-ImageRemaining")); err == nil {
		r.ImageRemaining = v
	}

	if v, err := strconv.ParseInt(header.Get("X-RateLimit-Reset"), 10, 64); err == nil {
		r.Reset = time.Unix(v, 0)
	}
}
