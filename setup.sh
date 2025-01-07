#!/bin/bash

# Run with sudo to install packages

# Install MongoDB

echo "Installing MongoDB..."

sudo apt-get install gnupg curl
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc |
  sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
    --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl daemon-reload
sudo systemctl enable mongod
sudo systemctl status mongod

mongod --version

# Install pipx

echo "Installing pipx..."

sudo apt update
sudo apt install pipx
pipx ensurepath

pipx --version

# Install Poetry

echo "Installing Poetry..."

pipx install poetry

poetry --version

# Install enviroment manager
echo "Installing direnv..."

sudo apt install direnv

direnv --version

# Add direnv to shell

echo "Adding direnv to shell..."
eval "$(direnv hook $SHELL)"
echo "direnv added to shell"

# Create direnv config directory

echo "Creating direnv config directory..."

mkdir -p ~/.config/direnv
touch ~/.config/direnv/direnvrc

# Add Poetry layout function to direnvrc

echo "Setting up direnvrc..."
cat <<'EOF' >~/.config/direnv/direnvrc
layout_poetry() {
  if [[ ! -f pyproject.toml ]]; then
    log_error 'No pyproject.toml found. Use `poetry new` or `poetry init` to create one first.'
    exit 2
  fi

  poetry run true

  export VIRTUAL_ENV=$(poetry env info --path)
  export POETRY_ACTIVE=1
  PATH_add "$VIRTUAL_ENV/bin"
}
EOF

# Add direnv layout to .envrc

echo 'layout poetry' >.envrc

# Add PYTHONPATH to .envrc

echo 'export PYTHONPATH=$PWD/app/src' >>.envrc

# Load .envrc

direnv allow

echo "Setup complete"
echo -e "\n"
echo "Upadating packages and installing dependencies..."

poetry lock --no-update
poetry install

echo -e "\n"
echo "All set! remeber to start your database brfore running app"
echo -e "\n\n"
