/* Eden live ISO hotplug helper: udev-less module autoloading.
 *
 *   eden-hotplug coldplug   one pass over devices already present
 *   eden-hotplug daemon     netlink uevent listener (foreground)
 */

#include <errno.h>
#include <fcntl.h>
#include <glob.h>
#include <linux/netlink.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static void
modprobe_alias(const char *alias)
{
    pid_t p;

    if (!alias || !*alias)
        return;
    p = fork();
    if (p == 0) {
        execl("/usr/bin/modprobe", "modprobe", "-q", alias, (char *)NULL);
        _exit(127);
    }
    if (p > 0)
        waitpid(p, NULL, 0);
}

static void
coldplug(void)
{
    glob_t g;

    if (glob("/sys/bus/*/devices/*/modalias", 0, NULL, &g) != 0)
        return;
    for (size_t i = 0; i < g.gl_pathc; i++) {
        char buf[256];
        int fd = open(g.gl_pathv[i], O_RDONLY);
        ssize_t n;

        if (fd < 0)
            continue;
        n = read(fd, buf, sizeof(buf) - 1);
        close(fd);
        if (n <= 0)
            continue;
        buf[n] = 0;
        char *nl = strchr(buf, '\n');
        if (nl)
            *nl = 0;
        modprobe_alias(buf);
    }
    globfree(&g);
}

static void
daemon_loop(void)
{
    int fd = socket(AF_NETLINK, SOCK_DGRAM, NETLINK_KOBJECT_UEVENT);
    struct sockaddr_nl sa;
    char buf[4096];

    if (fd < 0)
        return;
    memset(&sa, 0, sizeof(sa));
    sa.nl_family = AF_NETLINK;
    sa.nl_groups = 1;
    if (bind(fd, (struct sockaddr *)&sa, sizeof(sa)) != 0)
        return;
    for (;;) {
        ssize_t n = recv(fd, buf, sizeof(buf) - 1, 0);
        char *action = NULL, *modalias = NULL;

        if (n <= 0)
            continue;
        buf[n] = 0;
        for (char *p = buf; p < buf + n; p += strlen(p) + 1) {
            if (!strncmp(p, "ACTION=", 7))
                action = p + 7;
            else if (!strncmp(p, "MODALIAS=", 9))
                modalias = p + 9;
        }
        if (action && !strcmp(action, "add") && modalias)
            modprobe_alias(modalias);
    }
}

int
main(int argc, char **argv)
{
    if (argc > 1 && !strcmp(argv[1], "coldplug")) {
        coldplug();
        return 0;
    }
    daemon_loop();
    return 0;
}
