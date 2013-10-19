Build notes for Windows:
- If you don't have python installed at C:\Python27, edit build.proj accordingly
- Execute buildVS2010.bat
   - If you got VS2012, this will fail. 
   - Edit/Copy the build script, so that it finds vcvars32.bat (just needed to replace 10.0 with 11.0).
   - Open the solution and update the toolset.
   - Compile with the build script and ignore an error regarding ./Win32 not deletable.
- Be done with it :)