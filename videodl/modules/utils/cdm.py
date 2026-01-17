'''
Function:
    Implementation of CDM Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
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