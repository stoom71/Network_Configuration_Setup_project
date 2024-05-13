import socket
import argparse
import sys
import os
import datetime

# Parse input arguments 
parser = argparse.ArgumentParser(description = "My Server")

parser.add_argument("-p", '--port', type = int, required = True, help = 'port number')
parser.add_argument("-d", '--directory', type = str, required = True, help = 'root directory') 

args = parser.parse_args() #reads the command line -p and -d



# Check if valid port and directory arguments are provided
try:
    if args.port < 0 or args.port > 65353: # Raise a ValueError if port number is less than 0 or greater than 65535
        raise ValueError('Invalid port number. Please enter a port number between 0 and 65535.')
    elif args.port > 0 and args.port < 1024:
        print('Warning: Using well known port number.')
except ValueError as e:
    print('Error:', e, file=sys.stderr)
    sys.exit(1)
    
print('{}: entered port number, {}: entered root directory path'.format(args.port, args.directory))


filename = 'HelloWorld.html'
filepath = os.path.join(args.directory, filename)

if not os.path.isfile(filename):
  #If the file isn't found then, 404 Not FOund error will return
  response = "HTTP/1.1 404 Not Found\r\n"
  print(response)
else:
  #Else the file has been found, read the contents and determine the content type
  with open(filepath, 'rb') as x:
    content = x.read()
  if filename.endswith('.html'):
    content_type = 'text/html' # if filename.endswith('.html') else 'application/octet-stream'


  #Generate http response if file is found
  #Since the file is opened in binary 
  httpResponse = b''
  httpResponse = b'HTTP/1.1 200 OK\r\n'
  httpResponse += b"Content-Type: " + content_type.encode() + b"\r\n"
  httpResponse += b"Content-Length: " + str(len(content)).encode() + b"\r\n"
  httpResponse += b"Date: " + datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT').encode() + b"\r\n"
  #datetime.datetime.utcnow() gets the current date and time in Coordinated Universal Time (UTC).
  httpResponse += b"Last-Modified: " + datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath)).strftime('%a, %d %b %Y %H:%M:%S GMT').encode() + b"\r\n"
  httpResponse += b"\r\n"
  httpResponse += content

  # Print to stdout http header and http response
  print(httpResponse.decode())

sys.exit(0)
