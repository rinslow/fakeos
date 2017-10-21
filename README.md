# fakeos
[![codebeat badge](https://codebeat.co/badges/d247bedf-d202-48ea-8aae-feeb3d4deb1f)](https://codebeat.co/projects/github-com-rinslow-fakeos-master)

Mock the os module. 
## What is fakeos
fakeos lets you run blazing fast unit-tests without using your operating systems for I/O-bound operations.

## Supported
* mkdir
* getcwd
* chdir
* listdir
* environ
* getenv
* putenv
* makedirs
* chown
* chmod
* rmdir
* remove
* unlink
* major
* minor
* makedev
* rename
* access
* getegid
* setegid
* geteuid
* seteuid
* getgid
* setgid
* getuid
* setuid
* cpu_count

## Not supported yet
* walk, fwalk
* stat, stat_float_times, statvfs, 
* scandir
* replace
* renames
* removedirs
* sync
* link, readlink, unlink
* symlink
* mkfifo
* mknod
* truncate
* utime
* uname
* abort
* _exit
* execl, execle, execlp, execlpe, execv, execve, execvp, execvpe
* pathconf
* chflags
* chroot
* ctermid
* confstr
* cpu_count
* fsencode, fsdecode
* fspath
* get_exec_path
* getgrouplist
* getgroups, setgroups
* getlogin
* getpgid, setpgid
* getpgrp, setpgrp
* getpid
* getppid
* getpriority, setpriority
* getresuid, setresuid
* getresgid, setresgid
* getsid, setsid
* initgroups
* setregid
* setreuid
* strerror
* umask
* unsetenv
* open
* pipe
* pipe2
* read
* write
* sendfile 
* get_terminal_size
* getxattr, listxattr, removexattr, setxattr
* fork
* forkpty
* kill
* killpg
* nice
* plock
* popen
* spawnl, spawnle, spawnlp, spawnlpe, spawnv, spawnve, spawnvp, spawnvpe
* startfile
* system
* times
* getrandom, urandom
* wait, waitid, waitpid, wait3, wait4
* sched_getparam, sched_setparam
* sched_yield, sched_rr_get_interval
* sched_getscheduler, sched_setscheduler
* sched_get_priority_min, sched_get_priority_max
* sched_setaffinity, sched_getaffinity
* getloadavg
* sysconf
* sysconf

## Nice to have 
* environb
* fchdir
* getenvb
* getcwdb
* lchflags
* lchmod
* lchown
* lstat
* fdopen
* close
* closerange
* device_encoding
* dup
* dup2
* fchmod
* fchown
* fdatasync
* fpathconf
* fstat
* fstatvfs
* fsync
* ftruncate
* get_blocking, set_blocking
* is_atty
* lockf
* lseek
* openpty
* posix_fallocate
* posix_fadvise
* pread
* pwrite
* readv, writev
* tcgetpgrp, tcsetpgrp
* ttyname
* get_inheritable, set_inheritable
* get_handle_inheritable, set_handle_inheritable

## Properties
* supports_bytes_environ
* sysconf_names
* pardir
* devnull
* curdir
* sep
* defsep
* linesep
* altsep
* extsep
* os.pathsep
* pathconf_names
* confstr_names
* supports_dir_fd
* supports_effective_ids
* supports_fd
* supports_follow_symlinks
