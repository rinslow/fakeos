"""Everything related to configuring a virtual user."""
from typing import Tuple


class FakeUser(object):
    """A user in the system"""
    def __init__(self, is_sudoer: bool = False, gid: int = -1, uid: int = -1):
        self.is_sudoer = is_sudoer
        self.gid = gid
        self.uid = uid

    def can_read(self, file_object: 'FakeFileLikeObject') -> bool:
        """Whether or not the user can read the file"""
        return self.can_access(file_object, action_mask=0b100)

    def can_write(self, file_object: 'FakeFileLikeObject') -> bool:
        """Whether or not the user can write to the file"""
        return self.can_access(file_object, action_mask=0b010)

    def can_execute(self, file_object: 'FakeFileLikeObject') -> bool:
        """Whether or not the user can execute the file"""
        return self.can_access(file_object, action_mask=0b001)

    def can_access(self, file_object: 'FakeFileLikeObject', action_mask: int) -> bool:
        """Whether or not user can access the file using an action mask."""
        return self._can_access(mode=file_object.mode,
                                file_gid=file_object.gid,
                                file_uid=file_object.uid,
                                action_mask=action_mask)

    def _can_access(self, mode: int, file_gid: int, action_mask: int,
                    file_uid: int) -> bool:
        """Whether or not the user can perform an action on the file"""
        owner, group, everyone = self._parse_mode(mode)
        return any([self.is_sudoer,
                    owner & action_mask == action_mask and file_uid == self.uid,
                    group & action_mask == action_mask and file_gid == self.gid,
                    everyone & action_mask == action_mask])

    @staticmethod
    def _parse_mode(mode: int) -> Tuple[int, int, int]:
        """Return the root byte, group byte and everyone byte of a mode"""
        octal = "{:o}".format(mode).zfill(3)

        if len(octal) != 3:
            raise ValueError("Illegal mode %d" % mode)

        owner, group, everyone = octal
        return int(owner), int(group), int(everyone)


class Root(FakeUser):
    """A root user"""
    def __init__(self, uid: int = -1, gid: int = -1):
        super().__init__(uid=uid, gid=gid, is_sudoer=True)
