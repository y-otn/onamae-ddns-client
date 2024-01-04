# onamae-ddns-client

Unofficial Python Implementation of Onamae.com's DDNS Client.

## Requirements

- Python 3.7 or higher

## Setup (Example for Linux, systemd)

1. Clone this repository:

   ```bash
   git clone https://github.com/y-otn/onamae-ddns-client.git
   cd onamae-ddns-client
   ```

2. Modify the following items in `onamae_ddns_client.py` (L8-L12):
   - `INTERVAL`
   - `USERID`
   - `PASSWORD`
   - `HOSTNAME` (optional)
   - `DOMNAME`

3. Place the script and set appropriate permissions:

   ```bash
   sudo mv onamae_ddns_client.py /usr/local/bin/
   sudo chown root:root /usr/local/bin/onamae_ddns_client.py
   sudo chmod 600 /usr/local/bin/onamae_ddns_client.py
   ```

4. Register as a service for automatic startup (this will also start it immediately):

   ```bash
   sudo cp onamae_ddns_client.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now onamae_ddns_client.service
   ```

5. Check the service status:

   ```bash
   sudo systemctl status onamae_ddns_client.service
   ```

## Disclaimer

- Please be aware that this script is an unofficial implementation and is not officially recognized or endorsed. Use it at your own risk.
- Ensure that `onamae_ddns_client.py` is not repeatedly triggered by cron or similar services, as it is designed to run continuously.

## References

- [LinuxやMacで お名前.com ダイナミックDNS の IPアドレスを更新する #dns - Qiita](https://qiita.com/ats124/items/59ec0f444d00bbcea27d)
- [お名前.comのDDNSをスクリプトから行う | メモ帳](https://blog.sky-net.pw/post/%E3%81%8A%E5%90%8D%E5%89%8D.com%E3%81%AEddns%E3%82%92%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%8B%E3%82%89%E8%A1%8C%E3%81%86/)
- [お名前ドットコムのDDNSのIPをLinuxから更新する、onamae_ddns - THUNの遊戯室](https://www.thun-techblog.com/index.php/blog/onamae-ddns-linux/)
