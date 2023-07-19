import argparse
import subprocess
import sys

ascii_art = '''

                              __
                            .d$$b
                          .' TO$;\\
                         /  : TP._;
                        / _.;  :Tb|
                       /   /   ;j$j
                   _.-"       d$$$$
                 .' ..       d$$$$;
                /  /P'      d$$$$P. |\\
               /   "      .d$$$P' |\^"l
             .'           `T$P^"""""  :
         ._.'      _.'                ;
      `-.-".-'-' ._.       _.-"    .-"
    `.-" _____  ._              .-"
   -(.g$$$$$$$b.              .'
     ""^^T$$$P^)            .(:
       _/  -"  /.'         /:/;
    ._.'-'`-'  ")/         /;/;
 `-.-"..--""   " /         /  ;
.-" ..--""        -'          :
..--""--.-"         (\      .-(\\
  ..--""              `-\(\/;`
    _.                      :
                            ;`-
                           :\\
                           ;  
  ______                       __
 /_  __/___  _________ _____ _/ /
  / / / __ \/ ___/ __ `/ __ `/ / 
 / / / /_/ / /  / /_/ / /_/ / /  
/_/  \____/_/   \__, /\__,_/_/   
               /____/            
'''

print(ascii_art)


parser = argparse.ArgumentParser(description='Torgal command-line interface')
parser.add_argument('command', choices=['host', 'user', 'email', 'logout'], nargs='?', help='the command to run')
parser.add_argument('--hostname', help='the hostname to use with the host command')
parser.add_argument('--username', help='the username to use with the user command')
parser.add_argument('--messageid', help='the message ID to use with the email command')
parser.add_argument('--logoutusername', help='the username to use with the logout command')
parser.add_argument('--messageidsfile', help='the path to a file containing message IDs to use with the email command')
args = parser.parse_args()

if args.command == 'host':
    if args.hostname:
        subprocess.run(['python', 'plugins/EndpointActivityByUser.py', args.hostname])
    else:
        subprocess.run(['python', 'plugins/EndpointActivityByUser.py'])
elif args.command == 'user':
    if args.username:
        subprocess.run(['python', 'plugins/UserActivityByEndpoint.py', args.username])
    else:
        subprocess.run(['python', 'plugins/UserActivityByEndpoint.py'])
elif args.command == 'email':
    if args.messageid:
        subprocess.run(['python', 'plugins/Quarantine.py', args.messageid])
    elif args.messageidsfile:
        with open(args.messageidsfile, 'r') as f:
            message_ids = f.read().splitlines()
        for message_id in tqdm(message_ids, desc='Processing messages', unit='message'):
            subprocess.run(['python', 'plugins/Quarantine.py', message_id])
            time.sleep(5)
        input('Processing complete. Press Enter to continue...')
    else:
        subprocess.run(['python', 'plugins/Quarantine.py'])
elif args.command == 'logout':
    if args.username:
        subprocess.run(['python', 'plugins/Logout.py', args.username])
    else:
        subprocess.run(['python', 'plugins/Logout.py'])
elif args.command is None:
    print("No command specified.")
    print("usage: torgal.py [-h] {host,user,email,logout}")
