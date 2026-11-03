import subprocess
from pathlib import Path

# Path to your local .env file
env_path = Path('.env')
if not env_path.exists():
    print("❌ Error: .env file not found in the project root!")
    exit(1)

# Read variables, ignoring comments and blank lines
env_vars = []
with open(env_path, 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            env_vars.append(line)

if env_vars:
    print(f"🚀 Pushing {len(env_vars)} environment variables to AWS Elastic Beanstalk...")
    # Runs: eb setenv KEY1=val1 KEY2=val2 ...
    subprocess.run(['eb', 'setenv'] + env_vars)
    print("✅ Successfully updated AWS environment properties!")
else:
    print("⚠️ No valid environment variables found in your .env file.")