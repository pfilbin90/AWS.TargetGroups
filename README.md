# NG.DevOps.AWSTargetGroups
In it's current state, this code will not function on it's own.  You must modify it to fit your needs.  
This repo is meant to be used with a Jenkins job.  It accepts an AWS Hostname as a Jenkins parameter, then passes that parameter into the python code to run the scripts.

| File Name | Description |
| --------- | :---------- |
| match_tg.py | Main function used by Jenkins job.  Matches hostname to TG (find_tgs.py), then deregisters it.  Then runs runcommand.py for IISReset. Finally adds hostname back to matched target group.|
| find_tgs.py | Uses the given hostname to find which target group the host belongs to |
| runcommand.py | Sends a powershell command with Octo.exe syntax to a windows Octopus server. This command starts an Octopus job named IISReset to reset the IIS services
