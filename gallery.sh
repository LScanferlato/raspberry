 sudo apt install python3-pip -y
 pip3 install gallery-dl


   nano ~/.config/gallery-dl/config.json

  Aggiungi la configurazione del proxy: 
    {
      "extractor": {
          "proxy": "socks5://127.0.0.1:9050"
      }
  }
  ```

  
