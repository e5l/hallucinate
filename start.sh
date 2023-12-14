#!/bin/bash

# Name of the tmux session
SESSION="AppSession"

# Path to the Python scripts and npm project
LLM_SERVER_PATH="llm_server.py"
IMAGE_SERVER_PATH="image_server.py"
HALLUCINATE_WEB_PATH="hallucinate-web"

# Start new tmux session
tmux new-session -d -s $SESSION

# Split window into three panes
tmux split-window -h
tmux split-window -v

# Select pane 0, navigate to the llm_server.py directory and run it
tmux select-pane -t 0
tmux send-keys "cd $(dirname $LLM_SERVER_PATH)" C-m
tmux send-keys "python $(basename $LLM_SERVER_PATH)" C-m

# Select pane 1, navigate to the image_server.py directory and run it
tmux select-pane -t 1
tmux send-keys "cd $(dirname $IMAGE_SERVER_PATH)" C-m
tmux send-keys "python $(basename $IMAGE_SERVER_PATH)" C-m

# Select pane 2, navigate to the hallucinate-web directory and start npm
tmux select-pane -t 2
tmux send-keys "cd $HALLUCINATE_WEB_PATH" C-m
tmux send-keys "npm run dev" C-m

# Attach to the tmux session
tmux attach-session -t $SESSION

