from __future__ import annotations

from .. import Backend, BackendNotAvailable, PasswordInfo, register_backend

try:
    import pywintypes
    import win32cred
except ImportError:
    win32cred = None


@register_backend(priority=50)
class WincredBackend(Backend):
    """
    Backend for `Windows Credential Manager <https://support.microsoft.com/en-us/windows/accessing-credential-manager-1b5c916a-6a16-889f-8581-fc16e8165ac0>`_, the password manager integrated in Windows.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not win32cred:
            raise BackendNotAvailable(self, "package win32cred missing")

    def get_password(self, name: str, warn_if_notfound=False) -> str|None:
        try:
            cred = win32cred.CredRead(Type=win32cred.CRED_TYPE_GENERIC, TargetName=name)
            self.logger.info("Password %s retrieved from backend %s", name, self.name)
            return self._decode_blob(cred['CredentialBlob'])
        except pywintypes.error as e:
            if e.winerror == 1168 and e.funcname == 'CredRead': # not found
                if warn_if_notfound:
                    self.logger.warning("Password %s not found in backend %s", name, self.name)
                return None
            else:
                raise

    def set_password(self, name: str, password: str, enterprise = False, username: str = None, **options) -> bool:
        # Determine username of existing credential, if any
        try:
            _existing_cred = win32cred.CredRead(Type=win32cred.CRED_TYPE_GENERIC, TargetName=name)
            existing_username = _existing_cred['UserName']
            created = False
        except pywintypes.error as e:
            if e.winerror == 1168 and e.funcname == 'CredRead': # not found
                created = True
                existing_username = None
            else:
                raise
            
        # Reuse exising username, if any
        if not username:
            username = existing_username
        
        cred = dict(
            Type=win32cred.CRED_TYPE_GENERIC,
            TargetName=name,
            UserName=username,
            CredentialBlob=password,
            Persist=win32cred.CRED_PERSIST_ENTERPRISE if enterprise else win32cred.CRED_PERSIST_LOCAL_MACHINE,
        )
        win32cred.CredWrite(cred, 0)
        self.logger.info("Password %s %s in backend %s", name, 'created' if created else 'updated', self.name)
        return created

    def delete_password(self, name: str, warn_if_notfound=False) -> bool:
        try:
            win32cred.CredDelete(Type=win32cred.CRED_TYPE_GENERIC, TargetName=name)
            self.logger.info("Password %s deleted from backend %s", name, self.name)
            return True
        except pywintypes.error as e:
            if e.winerror == 1168 and e.funcname == 'CredDelete': # not found
                if warn_if_notfound:
                    self.logger.warning("Password %s not found in backend %s", name, self.name)
                return False
            else:
                raise

    def list_passwords(self) -> list[PasswordInfo]:
        passwords: list[PasswordInfo] = []
        for cred in win32cred.CredEnumerate():
            password_name = cred.pop('TargetName')
            password = PasswordInfo(password_name)

            credtype = cred.pop('Type')
            if credtype == win32cred.CRED_TYPE_GENERIC: # The credential is a generic credential. The credential will not be used by any particular authentication package. The credential will be stored securely but has no other significant characteristics.
                credtype = 'Generic'
            elif credtype == 2: # The credential is a password credential and is specific to Microsoft's authentication packages. The NTLM, Kerberos, and Negotiate authentication packages will automatically use this credential when connecting to the named target.
                credtype = 'Domain'
            elif credtype== 3: # The credential is a certificate credential and is specific to Microsoft's authentication packages. The Kerberos, Negotiate, and Schannel authentication packages automatically use this credential when connecting to the named target.
                credtype = 'DomainCertificate'

            persist = cred.pop('Persist')
            if persist == win32cred.CRED_PERSIST_NONE:
                persist = 'None'
            elif persist == win32cred.CRED_PERSIST_SESSION:
                persist = 'Session'
            elif persist == win32cred.CRED_PERSIST_LOCAL_MACHINE:
                persist = 'Local'
            elif persist == win32cred.CRED_PERSIST_ENTERPRISE:
                persist = 'Enterprise'

            info = {
                'mtime': cred.pop('LastWritten'),
                'username': cred.pop('UserName'),
                'type': credtype,
                'persist': persist,
            }

            for key, value in cred.items():
                if value is None or value == '':
                    continue
                if key == 'CredentialBlob':
                    continue
                if key == 'Flags' and value == 0:
                    continue
                if key == 'Attributes' and not value:
                    continue
                info[key] = value
                
            password._add_backend_info(self, info)
            passwords.append(password)

        return sorted(passwords, key=lambda password: password.name)

    def _decode_blob(self, blob: bytes):
        """
        Attempt to decode password blob as UTF-16 then UTF-8.
        """
        try:
            return blob.decode('utf-16')
        except UnicodeDecodeError:
            decoded_cred_utf8 = blob.decode('utf-8')
            return decoded_cred_utf8
