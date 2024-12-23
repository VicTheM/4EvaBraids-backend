#!/bin/bash

# This file set the project up and makes it ready for run
# Run the file with admin priviledges

# Install enviroment manager
echo "Installing direnv..."
sudo apt install direnv
echo "direnv installed"

# Add direnv to shell
echo "Adding direnv to shell..."
eval "$(direnv hook bash)" # or zsh or fish
echo "direnv added to shell"

# Create direnv config directory
echo "Creating direnv config directory..."
mkdir -p ~/.config/direnv
touch ~/.config/direnv/direnvrc
echo "direnv config directory created"

# Add Poetry layout function to direnvrc
echo "Setting up ..."
cat << 'EOF' > ~/.config/direnv/direnvrc
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
echo 'layout poetry' > .envrc

# Add PYTHONPATH to .envrc
echo 'export PYTHONPATH=$PWD/app/src' >> .envrc

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