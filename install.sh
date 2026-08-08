#!/data/data/com.termux/files/usr/bin/bash

Omni Toolkit – One‑click installer for Termux

set -e

echo "[*] Checking Termux environment..."
if [ ! -d /data/data/com.termux ]; then
echo "[!] This script is meant for Termux on Android."
exit 1
fi

echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing system dependencies..."
pkg install -y python git arp-scan foremost qrencode zbar tesseract

echo "[*] Installing Python libraries..."
pip install -r requirements.txt

echo "[*] Creating Omni directory structure..."
mkdir -p ~/Omni/{core,data,logs,wordlists,themes}

echo "[*] Copying Omni files..."
cp -r core/ ~/Omni/core/
cp -r themes/ ~/Omni/themes/
cp menu.py file_picker.py ~/Omni/
cp -r wordlists/ ~/Omni/wordlists/ 2>/dev/null || true

echo "[*] Setting up welcome banner..."
cat > ~/.termux_load.sh << 'EOFW'
#!/data/data/com.termux/files/usr/bin/bash
clear
python3 ~/Omni/core/load_anim.py
python3 ~/Omni/core/welcome.py
echo -e "\n\033[1;36mPress any key to continue...\033[0m"
read -k1
EOFW
chmod +x ~/.termux_load.sh

echo "[*] Adding welcome to .zshrc..."
if ! grep -q "source ~/.termux_load.sh" ~/.zshrc; then
echo -e "\n# Omni welcome loader\nsource ~/.termux_load.sh" >> ~/.zshrc
fi

echo "[*] Creating 'omni' alias..."
if ! grep -q "alias omni=" ~/.zshrc; then
echo "alias omni='python3 ~/Omni/menu.py'" >> ~/.zshrc
fi

echo "[] Making Python files executable..."
chmod +x ~/Omni/.py ~/Omni/core/*.py

echo ""
echo "✅ Omni Toolkit installed successfully!"
echo ""
echo "Usage:"
echo "  - Type 'omni' to open the interactive menu"
echo "  - Or run standalone: ~/Omni/core/recon.py subdomains example.com"
echo ""
echo "To apply a unified theme, run 'omni', go to Settings → Option 6."
echo ""
echo "Close and reopen Termux to see your new welcome banner."
chmod +x install.sh

