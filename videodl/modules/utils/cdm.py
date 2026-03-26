'''
Function:
    Implementation of CDM Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import base64
import requests
from pywidevine import PSSH, Cdm, Device


'''initcdm'''
def initcdm(pssh_value, cdm_wvd_file_path: str):
    if pssh_value is None: return
    device = Device.load(cdm_wvd_file_path)
    assert device.security_level == 3
    pssh_value = PSSH(pssh_value)
    if pssh_value.system_id == PSSH.SystemId.PlayReady: pssh_value.to_widevine()
    cdm = Cdm.from_device(device)
    cdm_session_id = cdm.open()
    challenge = cdm.get_license_challenge(cdm_session_id, pssh_value)
    return cdm, cdm_session_id, challenge


'''closecdm'''
def closecdm(cdm: Cdm, cdm_session_id, response):
    cdm.parse_license(cdm_session_id, response)
    keys = []
    for key in cdm.get_keys(cdm_session_id):
        if "CONTENT" in key.type: keys += [f"{key.kid.hex}:{key.key.hex()}"]
    cdm.close(cdm_session_id)
    return keys


'''SearchPsshValueUtils'''
class SearchPsshValueUtils():
    PLAYREADY_SCHEME_ID = "9A04F079-9840-4286-AB92-E65BE0885F95"
    '''getpsshfrominit'''
    @staticmethod
    def getpsshfrominit(init_url, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        content, offsets, offset = requests.get(init_url, **request_overrides).content, [], 0
        while True:
            if (offset := content.find(b'pssh', offset)) == -1: break
            size = int.from_bytes(content[offset-4: offset], byteorder='big'); pssh_offset = offset - 4
            offsets.append(content[pssh_offset: pssh_offset+size]); offset += size
        pssh_list = [base64.b64encode(wv_offset).decode() for wv_offset in offsets]
        for pssh in pssh_list:
            if 70 < len(pssh) < 190: return pssh
        return None
    '''getpsshfromdefaultkid'''
    @staticmethod
    def getpsshfromdefaultkid(manifest_content: str, xml_node: str = "cenc:default_KID", default_kid: str = None):
        try:
            if default_kid is None: default_kid = re.search(fr'{xml_node}="([a-fA-F0-9-]+)"', manifest_content).group(1).replace('-', '')
            pssh = f'000000387073736800000000edef8ba979d64acea3c827dcd51d21ed000000181210{default_kid}48e3dc959b06'
            return base64.b64encode(bytes.fromhex(pssh)).decode()
        except Exception:
            return None
    '''getpsshfromcencpssh'''
    @staticmethod
    def getpsshfromcencpssh(manifest_content: str, xml_node: str = "cenc:pssh"):
        try: return str(min(re.findall(fr'<[^<>]*{xml_node}[^<>]*>(.*?)</[^<>]*{xml_node}[^<>]*>', manifest_content), key=len))
        except Exception: return None
    '''getpsshfromplayready'''
    @staticmethod
    def getpsshfromplayready(manifest_content: str):
        try: return str(min(re.findall(fr'<ProtectionHeader[^<>"]*"[^<>"]*{SearchPsshValueUtils.PLAYREADY_SCHEME_ID}[^<>"]*"[^<>]*>(.*?)</ProtectionHeader>', manifest_content, re.DOTALL | re.IGNORECASE), key=len))
        except Exception: return None