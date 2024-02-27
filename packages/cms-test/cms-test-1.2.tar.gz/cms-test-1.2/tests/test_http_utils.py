from cms import http_utils

decrypted_cred = http_utils.get_cred_from_uuid(
    'ae899373-8d60-4360-a2d6-045027fdb5ef',
    'https://sit.hcmp.jio.com/openapi/credential-management/cms/v1/getcredential',
    'Basic Y21zX3VzZXI6ejJmOSNROT1WZjwoM2k=',
    'encryptionIntVec',
    'aesEncryptionKey'
)

print(decrypted_cred)