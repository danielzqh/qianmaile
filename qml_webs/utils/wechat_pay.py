import time
import uuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings
import requests
import json
import base64


wechat_config = settings.WECHAT_PAY

def get_private_key():
    with open(wechat_config['private_key'], "r") as f:
        return f.read()

def sign(method, url, body_str):
    """generate v3 signature"""
    private_key_str = get_private_key()
    from cryptography.hazmat.primitives import serialization
    private_key = serialization.load_pem_private_key(
        private_key_str.encode("utf-8"), password=None, backend=default_backend()
    )
    timestamp = str(int(time.time()))
    nonce_str = str(uuid.uuid4()).replace("-", "")
    message = f"{method}\n{url}\n{timestamp}\n{nonce_str}\n{body_str}\n"
    # print("\n" + "="*50)
    # print("==== sign message repr ====")
    # print("sign message:", repr(message))
    sign_result = private_key.sign(message.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
    import base64
    sign_64 = base64.b64encode(sign_result).decode("utf-8")
    return timestamp, nonce_str, sign_64

def create_native_order(out_trade_no, total_fee, description):
    """
    generate native order
    out_trade_no: local order number
    total_fee: yuan
    return dict: {code_url, prepay_id, ...}
    """
    url_path = "/v3/pay/transactions/native"
    full_url = f"https://api.mch.weixin.qq.com{url_path}"
    amount = int(round(total_fee * 100))

    req_body = {
        "appid": wechat_config['app_id'],
        "mchid": wechat_config['mch_id'],
        "out_trade_no": out_trade_no,
        "description": description,
        "notify_url": wechat_config['notify_url'],
        "amount": {"total": amount, "currency": "CNY"},
        "notify_url": "https://qianmaile.com.cn/pay/wechat_notify/",
    }
    import json
    body_json = json.dumps(req_body)
    ts, nonce, sig = sign("POST", url_path, body_json)
    #auth = f'MCH-V3-SHA256 serial="{wechat_config["serial_no"]}",nonce="{nonce}",timestamp="{ts}",signature="{sig}"'
    auth = f'WECHATPAY2-SHA256-RSA2048 mchid="{wechat_config['mch_id']}",nonce_str="{nonce}",timestamp="{ts}",serial_no="{wechat_config['serial_no']}",signature="{sig}"'
    headers = {"Authorization": auth, "Content-Type": "application/json"}
    # print("\n" + "=" * 50)
    # print("URL:", full_url)
    # print("sign url:", url_path)
    # print("Body:", body_json)
    # print("authorization:", auth)
    # print("serial no:", wechat_config["serial_no"])

    resp = requests.post(full_url, headers=headers, data=body_json.encode("utf-8"))
    return resp.json()

def generate_qrcode_data(code_url):
    """generate qr code base64"""
    import qrcode
    from io import BytesIO
    import base64
    qr = qrcode.make(code_url)
    buf = BytesIO()
    qr.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"

def wx_query_order(out_trade_no):
    url_path = f"/v3/pay/transactions/out-trade-no/{out_trade_no}?mchid={wechat_config['mch_id']}"
    full_path = f"https://api.mch.weixin.qq.com{url_path}"
    body = ""
    ts, nonce, sig = sign("GET", url_path, body)
    auth_header = f'WECHATPAY2-SHA256-RSA2048 mchid="{wechat_config['mch_id']}",serial_no="{wechat_config['serial_no']}",nonce_str="{nonce}",timestamp="{ts}",signature="{sig}"'

    # print("=== DEBUG INFO ===")
    # print("mchid:", wechat_config['mch_id'])
    # print("serial_no:", wechat_config['serial_no'])
    # print("timestamp:", ts)
    # print("nonce:", nonce)
    # print("signature(base64):", sig)
    # print("auth_header:", auth_header)

    headers = {"Authorization": auth_header, "Accept": "application/json"}
    params = {"mchid": wechat_config['mch_id']}
    resp = requests.get(full_path, headers=headers, timeout=10)
    print("wx_query_order resp:", out_trade_no, resp.status_code, resp.text)
    if resp.status_code != 200:
        return None
    return resp.json()


def wx_aes_gcm_decrypt(nonce, ciphertext, associated_data):
    """wechat v3 notify aes-gcm decrypt"""
    API_V3_KEY = wechat_config['api_v3_key']
    key_bytes = API_V3_KEY.encode("utf-8")
    nonce_bytes = nonce.encode("utf-8")
    ad_bytes = associated_data.encode("utf-8")
    cipher_all = base64.b64decode(ciphertext)
    tag = cipher_all[-16:]
    cipher_data = cipher_all[:-16]
    cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(nonce_bytes, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(ad_bytes)
    raw = decryptor.update(cipher_data) + decryptor.finalize()
    return json.loads(raw.decode("utf-8"))