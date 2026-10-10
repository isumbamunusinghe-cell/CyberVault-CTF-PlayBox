**# CV-05 — The Compromised Server**

**\*\*Domain:\*\*** Linux/System Security  
**\*\*Difficulty:\*\*** Moderate–Hard  
**\*\*Environment:\*\*** Ubuntu challenge container accessed over SSH  
**\*\*Tools:\*\*** SSH client and standard Linux command-line tools

**## Scenario**

The CyberVault investigation has identified a Linux server that may contain evidence of the incident. Connect to the server using the supplied low-privilege account, investigate its users, groups, permissions, and maintenance setup, then recover the incident evidence.

**## Connect**

Use the host and port supplied by your lab administrator:

\`\`\`bash
ssh -p 2222 player@\<challenge-host>
\`\`\`

For the current isolated VirtualBox lab, the endpoint is \`192.168.60.50:2222\` and the development account password is \`CV05-Lab-Only!\`. A later deployment may use a different host address or credential; follow the values issued for that run. Verify a new SSH host-key fingerprint with the lab administrator, especially after a reset.

**## Objective**

Investigate the server and recover the incident evidence. Submit the recovered flag through the channel specified by the lab administrator. Do not scan or connect to systems outside the supplied lab.

The environment resets to its original state when the administrator recreates the challenge container.
