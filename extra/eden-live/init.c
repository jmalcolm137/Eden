/* Eden live ISO init: mounts pseudo-filesystems, starts seatd, system D-Bus,
 * NetworkManager, then the user session (session bus, xfconfd, xfwl4 with
 * Xwayland + xfce4-session) as uid 1000, no login required. */

#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <ftw.h>
#include <unistd.h>

#define USER_UID 1000
#define USER_GID 1000
#define USER_NAME "action"
#define HOME_DIR "/home/action"
#define RUNTIME_DIR "/run/user/1000"

static int chown_cb(const char *path, const struct stat *st, int flag,
                    struct FTW *ftw) {
    (void)st;
    (void)flag;
    (void)ftw;
    lchown(path, USER_UID, USER_GID);
    return 0;
}

static void logmsg(const char *msg) {
    dprintf(1, "eden-init: %s\n", msg);
}

static void mkdir_p(const char *path, mode_t mode) {
    char tmp[256];
    size_t len;
    snprintf(tmp, sizeof(tmp), "%s", path);
    len = strlen(tmp);
    if (len == 0)
        return;
    for (char *p = tmp + 1; *p; p++) {
        if (*p == '/') {
            *p = 0;
            mkdir(tmp, mode);
            *p = '/';
        }
    }
    mkdir(tmp, mode);
}

static void try_mount(const char *src, const char *dst, const char *fstype,
                      unsigned long flags, const char *data) {
    if (mount(src, dst, fstype, flags, data) != 0)
        dprintf(1, "eden-init: mount %s -> %s (%s): %s\n", src, dst, fstype,
                strerror(errno));
}

static pid_t spawn(char *const argv[], uid_t uid, gid_t gid) {
    pid_t pid = fork();
    if (pid < 0) {
        dprintf(1, "eden-init: fork failed: %s\n", strerror(errno));
        return -1;
    }
    if (pid == 0) {
        if (gid != (gid_t)-1)
            setgid(gid);
        if (uid != (uid_t)-1)
            setuid(uid);
        execv(argv[0], argv);
        dprintf(1, "eden-init: exec %s failed: %s\n", argv[0], strerror(errno));
        _exit(127);
    }
    return pid;
}

int main(void) {
    logmsg("start");

    mkdir_p("/dev", 0755);
    mkdir_p("/proc", 0555);
    mkdir_p("/sys", 0555);
    mkdir_p("/run", 0755);
    mkdir_p("/tmp", 01777);

    try_mount("devtmpfs", "/dev", "devtmpfs", 0, NULL);
    try_mount("proc", "/proc", "proc", 0, NULL);
    try_mount("sysfs", "/sys", "sysfs", 0, NULL);
    try_mount("tmpfs", "/run", "tmpfs", 0, "mode=0755");
    try_mount("tmpfs", "/tmp", "tmpfs", 0, "mode=1777");
    mkdir_p("/dev/pts", 0755);
    try_mount("devpts", "/dev/pts", "devpts", 0, "mode=0620,gid=5");
    mkdir_p("/dev/shm", 01777);
    try_mount("tmpfs", "/dev/shm", "tmpfs", 0, "mode=1777");

    sethostname("eden-live", 9);

    mkdir_p("/run/dbus", 0755);
    mkdir_p("/run/user", 0755);
    mkdir(RUNTIME_DIR, 0700);
    if (chown(RUNTIME_DIR, USER_UID, USER_GID) != 0)
        dprintf(1, "eden-init: chown %s failed: %s\n", RUNTIME_DIR,
                strerror(errno));
    mkdir_p("/var/lib/NetworkManager", 0755);
    mkdir_p("/var/lib/wpa_supplicant", 0755);
    mkdir_p("/var/run", 0755);

    /* home skeleton for the unprivileged session user */
    mkdir_p(HOME_DIR "/.config", 0700);
    mkdir_p(HOME_DIR "/.local/share", 0700);
    mkdir_p(HOME_DIR "/.local/state", 0700);
    mkdir_p(HOME_DIR "/.cache", 0700);
    mkdir_p(HOME_DIR "/Desktop", 0700);
    chown(HOME_DIR "/.config", USER_UID, USER_GID);
    chown(HOME_DIR "/.local", USER_UID, USER_GID);
    chown(HOME_DIR "/.local/share", USER_UID, USER_GID);
    chown(HOME_DIR "/.local/state", USER_UID, USER_GID);
    chown(HOME_DIR "/.cache", USER_UID, USER_GID);
    chown(HOME_DIR "/Desktop", USER_UID, USER_GID);
    chown(HOME_DIR, USER_UID, USER_GID);
    nftw(HOME_DIR, chown_cb, 32, FTW_PHYS);

    /* display/seat management */
    char *seatd_argv[] = {"/usr/bin/seatd", NULL};
    spawn(seatd_argv, 0, 0);
    logmsg("started seatd");

    /* seatd creates its socket asynchronously; wait for it, then open it up */
    for (int i = 0; i < 40; i++) {
        if (chmod("/run/seatd.sock", 0666) == 0)
            break;
        usleep(50000);
    }
    for (int i = 0; i < 8; i++) {
        char p[64];
        snprintf(p, sizeof(p), "/dev/dri/card%d", i);
        chmod(p, 0666);
        snprintf(p, sizeof(p), "/dev/dri/renderD%d", 128 + i);
        chmod(p, 0666);
        snprintf(p, sizeof(p), "/dev/input/event%d", i);
        chmod(p, 0666);
    }
    chmod("/dev/uinput", 0666);
    chmod("/dev/dri", 0755);
    chmod("/dev/input", 0755);

    /* system bus (NetworkManager etc.) */
    char *sysbus_argv[] = {"/usr/bin/dbus-daemon", "--system", "--nofork", NULL};
    spawn(sysbus_argv, 0, 0);
    logmsg("started system dbus");
    sleep(1);

    /* NetworkManager (brings up wired/wifi automatically) */
    char *nm_argv[] = {"/usr/bin/NetworkManager", "--no-daemon", NULL};
    spawn(nm_argv, 0, 0);
    logmsg("started NetworkManager");

    sleep(1);

    /* root debug console on the serial line */
    {
        pid_t dbg = fork();
        if (dbg == 0) {
            setsid();
            int tty = open("/dev/ttyS0", O_RDWR);
            if (tty >= 0) {
                dup2(tty, 0);
                dup2(tty, 1);
                dup2(tty, 2);
                if (tty > 2)
                    close(tty);
                char *dbg_argv[] = {"/bin/bash", "-i", NULL};
                execv(dbg_argv[0], dbg_argv);
            }
            _exit(0);
        }
    }

    /* user session: session bus, composer */
    pid_t sess = fork();
    if (sess == 0) {
        setgid(USER_GID);
        setuid(USER_UID);
        chdir(HOME_DIR);
        setenv("HOME", HOME_DIR, 1);
        setenv("USER", USER_NAME, 1);
        setenv("LOGNAME", USER_NAME, 1);
        setenv("SHELL", "/bin/bash", 1);
        setenv("PATH",
               "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin", 1);
        setenv("XDG_RUNTIME_DIR", RUNTIME_DIR, 1);
        setenv("XDG_SESSION_TYPE", "wayland", 1);
        setenv("XDG_CURRENT_DESKTOP", "XFCE", 1);
        setenv("XDG_SESSION_DESKTOP", "xfce", 1);
        setenv("XKB_CONFIG_ROOT", "/usr/share/X11/xkb", 1);
        setenv("RUST_LOG", "xfwl4=debug", 1);
        unsetenv("DISPLAY");
        unsetenv("WAYLAND_DISPLAY");

        /* session bus at a fixed address */
        char *sbus_argv[] = {"/usr/bin/dbus-daemon", "--session", "--nofork",
                             "--address=unix:path=" RUNTIME_DIR "/bus",
                             "--nopidfile", NULL};
        pid_t sbus = fork();
        if (sbus == 0) {
            execv(sbus_argv[0], sbus_argv);
            dprintf(1, "eden-init: session dbus failed: %s\n", strerror(errno));
            _exit(127);
        }
        setenv("DBUS_SESSION_BUS_ADDRESS", "unix:path=" RUNTIME_DIR "/bus", 1);
        sleep(2);

        /* minimal xfconf daemon on the session bus */
        char *xfconfd_argv[] = {"/usr/lib/xfce4/xfconf/xfconfd", NULL};
        spawn(xfconfd_argv, USER_UID, USER_GID);
        sleep(1);

        logmsg("starting xfwl4 with session");
        char *wl_argv[] = {"/usr/bin/xfwl4", "--backend", "tty",
                           "--session", "xfce4-session", NULL};
        execv(wl_argv[0], wl_argv);
        dprintf(1, "eden-init: xfwl4 failed: %s\n", strerror(errno));
        _exit(127);
    }
    logmsg("user session spawned");

    /* PID 1: reap children forever, restart the session if it dies */
    for (;;) {
        int st = 0;
        pid_t p = waitpid(-1, &st, 0);
        if (p < 0) {
            if (errno == EINTR)
                continue;
            pause();
            continue;
        }
        if (p == sess) {
            dprintf(1, "eden-init: user session exited (status %d); restarting in 5s\n", st);
            sleep(5);
            sess = -1;
        }
    }
}
