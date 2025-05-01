# Model Context Protocol

### Step by step process

<ol>
<li>Download the Cursor IDE</li>

<li>Right click the IDE file and go to propertise and activate Executable as Program</li>

<li>Open the Cursor IDE</li>

```bash
sudo apt-get install --reinstall ubuntu-desktop
```

<li>Go to Cursor IDE file Directory Localtion</li>

```bash
cd Desktop/
```

<li>Run the below Command</li>

```bash
chmod +x Cursor-0.49.4-x86_64.AppImage 
```

<li>Provide Permission</li>

```bash
sudo chmod 4755 /home/bikas/Desktop/squashfs-root/usr/share/cursor/chrome-sandbox
```

<li>Go to the squashfs-root directory</li>

```bash
cd squashfs-root
```

<li>For run the IDE</li>

```bash
./AppRun
```

### uv

<li>Create venv using uv</li>

```bash
uv venv
```

<li>Activate venv</li>

```bash
source .venv/bin/activate
```

<li>Install Library</li>

```bash
uv add langchain-groq
uv add pandas
```

<li>Run file</li>

```bash
uv run app.py
```
</ol>

For open Cursor IDE using Command 

```bash
sudo apt-get install --reinstall ubuntu-desktop
cd Desktop/ # IDE Location Directory
chmod +x Cursor-0.49.4-x86_64.AppImage 
sudo chmod 4755 /home/bikas/Desktop/squashfs-root/usr/share/cursor/chrome-sandbox
cd squashfs-root
./AppRun
```
