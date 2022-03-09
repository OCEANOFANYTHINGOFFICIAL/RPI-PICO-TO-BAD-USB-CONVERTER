@echo off
@REM Background color: Blue
@REM Foreground color: White
color 0e
@REM This Program Will Configure Raspberry Pi Pico As A Bad USB Or USB Rubber Ducky Device
echo This Program Will Configure Raspberry Pi Pico As A Bad USB Or USB Rubber Ducky Device
echo.
echo This Program Is Written By: Nakshatra Ranjan Saha (OCEAN OF ANYTHING)
echo.
echo.
echo If You Really Want To Configure Your Raspberry Pi Pico As A Bad USB Or USB Rubber Ducky Device Then Press Any Key Or Else Press Ctrl+C To Exit.
pause >nul
echo.
echo.
echo.
cls
echo Now Follow The Instructions To Configure Your Raspberry Pi Pico As A Bad USB Or USB Rubber Ducky Device.
echo.
echo.
echo.
echo [1] First You Need To Connect Your Raspberry Pi Pico To Your Computer.
echo.
echo.
echo [2] Now You Have To Provide Your Raspberry Pi Pico's Directory URL In The Prompt Below.
echo.
set /p rpi_dir_url=[*]URL: 
echo.
echo.
echo [3] Now Disconnect Your Raspberry Pi Pico From Your Computer And Then Reconnect It To Your System With Holding The "BOOTSET" Button On Your Raspberry Pi Pico. It Will Reset Your Raspberry Pi Pico.
echo.
echo.
echo And Thats All. Now After This The Entire Process Will Be Automatically Completed. It Will Take Some Time. So Just Take A Coffee Break. During This Process Your Raspberry Pi Pico Will Be Disconnected From Your Computer Several Times. Dont Worry. It Will Be Reconnected To Your Computer After The Process Is Completed.
echo.
echo.
echo.
echo.
echo [+] Resetting Firmware...
Timeout /t 3 >nul
echo [#] Done!
echo [+] Resetting Hardware...
:%@Try%
copy "reset.uf2" "%rpi_dir_url%\reset.uf2" >nul
echo [#] Done!
Timeout /t 10 >nul
echo [+] Installing New Firmware...
Timeout /t 3 >nul
copy "firmware.uf2" "%rpi_dir_url%\firmware.uf2" >nul
echo [#] Done!
Timeout /t 10 >nul
echo [+] Installing Bootloader Firmware...
copy "boot.py" "%rpi_dir_url%\boot.py" >nul
echo [#] Done!
echo [+] Installing Firmware Libraries...
Xcopy "lib\adafruit_hid" "%rpi_dir_url%\lib\adafruit_hid" /E /H /C /I >nul
echo [#] Done!
echo [+] Installing Payload Converter Firmware And Runtimes...
copy "code.py" "%rpi_dir_url%\code.py" >nul
echo [#] Done!
echo [+] Installing Payloads...
copy "payload.dd" "%rpi_dir_url%\payload.dd" >nul
copy "payload2.dd" "%rpi_dir_url%\payload2.dd" >nul
copy "payload3.dd" "%rpi_dir_url%\payload3.dd" >nul
copy "payload4.dd" "%rpi_dir_url%\payload4.dd" >nul
echo [#] Done!
cls
echo.
echo.
echo.
echo Congratulations! Your Raspberry Pi Pico Has Been Configured As A Bad USB Or USB Rubber Ducky Device.
echo Now You Can Use It As A USB Rubber Ducky Device By Writing Ducky Script In "payload.dd" File.
echo Be Careful. The Moment You Write The Ducky Script In "payload.dd" File It Will Be Executed. So Make Sure That You Have A Backup Of Your "payload.dd" File.
echo.
echo.
echo.
echo.
echo.
echo Pres Enter To Exit.
pause >nul
