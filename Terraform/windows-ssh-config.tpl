add-content -path C:\Users\rm\.ssh\config -value @'

Host ${hostname}
HostName ${hostname}
User ${user}
IdentityFile ${identityfile}
'@