pkgname = "thunar-volman"
pkgver = "4.20.0"
pkgrel = 0
build_style = "gnu_configure"
configure_gen = []
hostmakedepends = [
    "gettext",
    "pkgconf",
]
makedepends = [
    "exo-devel",
    "glib-devel",
    "gtk+3-devel",
    "libgudev-devel",
    "libnotify-devel",
    "libxfce4ui-devel",
    "libxfce4util-devel",
    "xfconf-devel",
]
pkgdesc = "Thunar volume manager extension"
license = "GPL-2.0-only"
url = "https://docs.xfce.org/xfce/thunar/thunar-volman"
source = f"https://archive.xfce.org/src/xfce/thunar-volman/4.20/thunar-volman-4.20.0.tar.bz2"
sha256 = "b0dad852959b515b8fbfd1ed552e362340347d26d5246e7f1b973027131eb1da"
# upstream tests need a display and a running session bus
options = ["!check"]


def post_patch(self):
    # socket embedding is X11-only; show the preferences dialog directly
    p = self.cwd / "thunar-volman-settings/main.c"
    text = p.read_text()
    text = text.replace("#include <gtk/gtkx.h>\n", "")
    text = text.replace(
        "  GtkWidget *dialog, *plug, *plug_child;\n"
        "  GError    *error = NULL;\n"
        "  GList     *list;\n",
        "  GtkWidget *dialog;\n  GError    *error = NULL;\n",
    )
    old = """  else
    {
      /* create plug widget */
      plug = gtk_plug_new (opt_socket_id);
      g_signal_connect (plug, "delete-event", G_CALLBACK (gtk_main_quit), NULL);
      gtk_widget_show (plug);

      list = gtk_container_get_children (GTK_CONTAINER (gtk_dialog_get_content_area (GTK_DIALOG (dialog))));
      plug_child = list->data;
      g_list_free (list);

      xfce_widget_reparent (plug_child, plug);
      gtk_widget_destroy (dialog);

      gtk_main ();
    }
"""
    new = """  else
    {
      /* Wayland has no X11 socket embedding; show the dialog normally */
      gtk_widget_show (dialog);
      gtk_main ();
    }
"""
    if old not in text:
        self.error("unexpected socket embedding code in thunar-volman settings")
    p.write_text(text.replace(old, new))
