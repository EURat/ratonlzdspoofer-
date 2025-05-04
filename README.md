# HardwareID Shower - Desktop Executable Build

This project is a Flask-based application to show and mask hardware IDs and network information.

## Building the Executable

To create a standalone Windows executable that runs the Flask app with administrator privileges:

1. Ensure you have Python 3.12+ installed and added to your PATH.
2. Open a command prompt in the project directory.
3. Run the build script:

```
build_exe.bat
```

This will install PyInstaller if not present and build the executable with admin rights.

The executable will be located in the `dist` folder as `app.exe`.

## Running the Executable

- Run `dist\app.exe` as administrator (it will request admin rights automatically).
- The Flask app will start and serve the web interface.
- Open your browser and navigate to `http://127.0.0.1:5000/` to use the app.

## Notes

- The `templates` and `static` folders are included in the executable.
- Make sure to run the executable with admin rights for full functionality (e.g., IP masking, process killing).
- You can share the `dist\app.exe` and this repository on GitHub for your manager.

## Dependencies

- Flask
- WMI
- psutil

These are included in the executable.

## Troubleshooting

- If the app does not start, check the console output for errors.
- Ensure no firewall or antivirus is blocking the app.
- Run the executable as administrator.
