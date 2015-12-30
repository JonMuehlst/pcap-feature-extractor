# Contribute
  1. Fork the repository
  2. Commit to your local fork
  3. Issue a Pull request

# Push changes to github
  1. Update all the relevant changes in `changelog.txt` (See the file for structure)  
    1.1 Use git diff to easily view changes
  2. Use `git add filenames...` to add all modified and new files. (Also add TODO, changelog itself, temp etc...)
  3. Use `git status` to see if you missed anything
  4. Commit the changes - `git commit -F changelog.txt`
  5. Push changes to remote - `git push  <REMOTENAME> <LOCALBRANCHNAME>:<REMOTEBRANCHNAME>`  
    5.1. e.g. `push origin dev:dev`

# Verify code is up-to-date with remote
  1. Fetch the up-to-date code using `git fetch`
  2. Run `git status`

# Add a feature to the code  
  1. Define what you want to implement  
  2. Write documentation  
  3. Write a test in advance  
  4. Implement  

# Write a test case  
  1. Pick a scenario  
  2. Define the correct outcome for the specific case  
  3. Simulate the above  
