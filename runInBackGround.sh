#!/bin/bash

# Start Api.post
nohup python3 -m Api.post >api_post.out 2>api_post.err &
API_POST_PID=$!
echo "Api.post started with PID: $API_POST_PID"

# Start web-dynamic.home_page
nohup python3 -m web-dynamic.home_page >web_dynamic.out 2>web_dynamic.err &
WEB_DYNAMIC_PID=$!
echo "web-dynamic.home_page started with PID: $WEB_DYNAMIC_PID"
