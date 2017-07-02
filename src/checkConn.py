# Import the module
import subprocess

# Ask the user for input
host = 'emTvUPCL001'

# Set up the echo command and direct the output to a pipe
p1 = subprocess.Popen(['ping', host], stdout=subprocess.PIPE)

# Run the command
output = p1.communicate()[0]

# print output

if 'Lost = 0 (0% loss)' in output:
    print 'Tv Connected'
else:
    print 'Connection Error'

host = 'emTvUPCL002'

# Set up the echo command and direct the output to a pipe
p1 = subprocess.Popen(['ping', host], stdout=subprocess.PIPE)

# Run the command
output = p1.communicate()[0]

# print output

if 'Lost = 0 (0% loss)' in output:
    print 'Tv Connected'
else:
    print 'Connection Error'
