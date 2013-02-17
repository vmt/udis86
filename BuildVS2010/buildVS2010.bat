echo off
call "C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\vcvarsall.bat" x86_amd64

msbuild.exe udis86.sln /t:Clean
msbuild.exe build.proj /t:Clean,BuildRelease_x86,BuildRelease_x64,PostBuild
REM msbuild.exe build.proj /t:Clean,BuildRelease_x86,BuildRelease_x64,BuildDebug_x86,BuildDebug_x64,PostBuild
pause