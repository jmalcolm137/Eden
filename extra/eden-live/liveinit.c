/* Eden live ISO early init (PID 1 inside the initramfs).
 *
 * Loads the storage/filesystem modules, finds the ISO image on an attached
 * block device, mounts the squashfs root through a loop device, builds a
 * tmpfs-backed overlay for writes and hands over to sinit in the new root.
 */

#include <errno.h>
#include <fcntl.h>
#include <linux/loop.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/sysmacros.h>
#include <sys/types.h>
#include <unistd.h>
#include <dirent.h>

#define ISO_DIR "/mnt/iso"
#define ROOT_DIR "/mnt/root"
#define OVER_DIR "/mnt/overlay"
#define SQUASH_PATH ISO_DIR "/eden/rootfs.squashfs"

static void
msg(const char *s)
{
    dprintf(1, "eden-liveinit: %s\n", s);
}

static void
try_mount(const char *src, const char *dst, const char *fs, unsigned long fl,
          const char *data)
{
    if (mount(src, dst, fs, fl, data) != 0)
        dprintf(1, "eden-liveinit: mount %s -> %s: %s\n", src, dst,
                strerror(errno));
}

static void
load_modules(void)
{
    FILE *f = fopen("/modules.order", "r");
    char line[512];

    if (!f) {
        msg("no /modules.order");
        return;
    }
    while (fgets(line, sizeof(line), f)) {
        char *nl = strchr(line, '\n');
        int fd;
        if (nl)
            *nl = 0;
        if (!line[0])
            continue;
        fd = open(line, O_RDONLY | O_CLOEXEC);
        if (fd < 0) {
            dprintf(1, "eden-liveinit: cannot open module %s: %s\n", line,
                    strerror(errno));
            continue;
        }
        if (syscall(SYS_finit_module, fd, "", 0) != 0 && errno != EEXIST)
            dprintf(1, "eden-liveinit: module %s: %s\n", line,
                    strerror(errno));
        close(fd);
    }
    fclose(f);
    msg("modules loaded");
}

static int
find_iso(void)
{
    DIR *d = opendir("/sys/class/block");
    struct dirent *de;

    if (!d)
        return -1;
    while ((de = readdir(d)) != NULL) {
        char dev[128];
        struct stat st;

        if (de->d_name[0] == '.')
            continue;
        if (!strncmp(de->d_name, "loop", 4) ||
            !strncmp(de->d_name, "ram", 3) ||
            !strncmp(de->d_name, "zram", 4) ||
            !strncmp(de->d_name, "dm-", 3) ||
            !strncmp(de->d_name, "md", 2))
            continue;
        snprintf(dev, sizeof(dev), "/dev/%s", de->d_name);
        if (stat(dev, &st) != 0 || !S_ISBLK(st.st_mode))
            continue;
        if (mount(dev, ISO_DIR, "iso9660", MS_RDONLY, NULL) != 0)
            continue;
        if (access(SQUASH_PATH, R_OK) == 0) {
            dprintf(1, "eden-liveinit: ISO on %s\n", dev);
            closedir(d);
            return 0;
        }
        umount2(ISO_DIR, MNT_DETACH);
    }
    closedir(d);
    return -1;
}

static int
setup_squash(void)
{
    int lc, num, lfd, ffd;
    char ldev[64];

    lc = open("/dev/loop-control", O_RDWR);
    if (lc < 0) {
        msg("no loop-control");
        return -1;
    }
    num = ioctl(lc, LOOP_CTL_GET_FREE);
    close(lc);
    if (num < 0) {
        msg("no free loop device");
        return -1;
    }
    snprintf(ldev, sizeof(ldev), "/dev/loop%d", num);
    if (access(ldev, F_OK) != 0) {
        if (mknod(ldev, S_IFBLK | 0600, makedev(7, num)) != 0) {
            dprintf(1, "eden-liveinit: mknod %s: %s\n", ldev,
                    strerror(errno));
            return -1;
        }
    }
    lfd = open(ldev, O_RDWR);
    if (lfd < 0) {
        dprintf(1, "eden-liveinit: open %s: %s\n", ldev, strerror(errno));
        return -1;
    }
    ffd = open(SQUASH_PATH, O_RDONLY);
    if (ffd < 0) {
        dprintf(1, "eden-liveinit: open squashfs: %s\n", strerror(errno));
        close(lfd);
        return -1;
    }
    if (ioctl(lfd, LOOP_SET_FD, ffd) != 0) {
        dprintf(1, "eden-liveinit: LOOP_SET_FD: %s\n", strerror(errno));
        close(ffd);
        close(lfd);
        return -1;
    }
    close(ffd);
    if (mount(ldev, ROOT_DIR, "squashfs", MS_RDONLY, NULL) != 0) {
        dprintf(1, "eden-liveinit: mount squashfs: %s\n", strerror(errno));
        close(lfd);
        return -1;
    }
    close(lfd);
    msg("squashfs mounted");
    return 0;
}

static int
setup_overlay(void)
{
    char opts[512];

    mkdir("/run/overlay", 0755);
    mkdir("/run/overlay/upper", 0755);
    mkdir("/run/overlay/work", 0755);
    snprintf(opts, sizeof(opts),
             "lowerdir=%s,upperdir=/run/overlay/upper,"
             "workdir=/run/overlay/work", ROOT_DIR);
    if (mount("overlay", OVER_DIR, "overlay", 0, opts) != 0) {
        dprintf(1, "eden-liveinit: overlay: %s\n", strerror(errno));
        return -1;
    }
    msg("overlay mounted");
    return 0;
}

static void
switch_to_root(void)
{
    mkdir(OVER_DIR "/.oldroot", 0755);
    mount("/dev", OVER_DIR "/dev", NULL, MS_MOVE, NULL);
    mount("/proc", OVER_DIR "/proc", NULL, MS_MOVE, NULL);
    mount("/sys", OVER_DIR "/sys", NULL, MS_MOVE, NULL);
    mount("/run", OVER_DIR "/run", NULL, MS_MOVE, NULL);
    if (chdir(OVER_DIR) != 0) {
        dprintf(1, "eden-liveinit: chdir: %s\n", strerror(errno));
        return;
    }
    if (syscall(SYS_pivot_root, ".", ".oldroot") == 0) {
        /* Keep the old root mounted: it holds the ISO and squashfs mounts
         * that back the live root, so detaching it can break later reads. */
    } else {
        dprintf(1, "eden-liveinit: pivot_root: %s (using chroot)\n",
                strerror(errno));
        if (chroot(".") != 0) {
            dprintf(1, "eden-liveinit: chroot: %s\n", strerror(errno));
            return;
        }
    }
    chdir("/");
    execl("/usr/bin/sinit", "sinit", (char *)NULL);
    dprintf(1, "eden-liveinit: exec sinit: %s\n", strerror(errno));
}

int
main(void)
{
    msg("start");

    mkdir("/dev", 0755);
    mkdir("/proc", 0555);
    mkdir("/sys", 0555);
    mkdir("/run", 0755);
    mkdir("/tmp", 0777);
    mkdir("/mnt", 0755);
    mkdir(ISO_DIR, 0755);
    mkdir(ROOT_DIR, 0755);
    mkdir(OVER_DIR, 0755);

    try_mount("devtmpfs", "/dev", "devtmpfs", 0, "mode=0755");
    try_mount("proc", "/proc", "proc", 0, NULL);
    try_mount("sysfs", "/sys", "sysfs", 0, NULL);
    try_mount("tmpfs", "/run", "tmpfs", 0, "mode=0755");

    load_modules();

    if (find_iso() != 0) {
        msg("no Eden ISO found");
        for (;;)
            pause();
    }
    if (setup_squash() != 0) {
        msg("cannot mount squashfs");
        for (;;)
            pause();
    }
    if (setup_overlay() != 0) {
        msg("cannot mount overlay");
        for (;;)
            pause();
    }

    switch_to_root();
    for (;;)
        pause();
    return 0;
}
