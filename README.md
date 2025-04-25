# Model Context Protocol

## Download the Cursor IDE

## Right click the IDE file and go to propertise and activate Executable as Program

# Open the Cursor IDE

```bash
sudo apt-get install --reinstall ubuntu-desktop
```

# Go to Cursor IDE file Directory Localtion

```bash
cd Desktop/
```

# Run the below Command

```bash
chmod +x Cursor-0.49.4-x86_64.AppImage 
```

# Provide Permission

```bash
sudo chmod 4755 /home/bikas/Desktop/squashfs-root/usr/share/cursor/chrome-sandbox
```

# Go to the squashfs-root directory

```bash
cd squashfs-root
```

# For run the IDE

```bash
./AppRun
```

### uv

# Create venv using uv

```bash
uv venv
```

# Activate venv

```bash
source .venv/bin/activate
```

# Install Library

```bash
uv add langchain-groq
uv add pandas
```

# Run file

```bash
uv run app.py
```
