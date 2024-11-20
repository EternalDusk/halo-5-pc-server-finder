# Halo 5 PC Server Finder
Track the server you're currently connected to in Halo 5: Forge.  
*Now you can blame lag with accuracy! ;P*  

Built using **Python 3.12.7**.

---

## How to Run the Program
1. **Download the latest release** from the [Releases](#) section.  
2. **Run the program as administrator.**  
   ⚠ Elevated privileges are required to sniff packets. Make sure to run the script in an Administrator Command Prompt.
3. The IP of the server you're connected to will be displayed. That's it!

---

## Running from Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/halo-5-pc-server-finder.git
   cd halo-5-pc-server-finder
   ```

2. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run the program as administrator**:
   Open an elevated/administrator command prompt and run:
   ```bash
   python main.py
   ```

---

## Building from Source with PyInstaller

To build the executable in a clean environment and avoid bloat:

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
    ```bash
    venv\Scripts\activate
    ```

3. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Build the executable**:
   ```bash
   pyinstaller --onefile --manifest=main.manifest main.py
   ```

5. **Find your build**:  
   The executable will be located in the `dist` folder.

---

## To-Do List
- [ ] Curate a list of server IPs.  
- [ ] Add a feature to monitor server ping in real time.  
- [ ] Replace the terminal interface with a GUI using PyAutoGUI.

---

## Contributing
Feel free to open issues or submit pull requests to improve this tool. All contributions are welcome!  

--- 
