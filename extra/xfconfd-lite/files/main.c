/* xfconfd-lite: minimal org.xfce.Xfconf D-Bus daemon for the Eden live ISO.
 * Loads per-channel XML config from the XDG dirs, serves properties from
 * memory and keeps runtime changes in memory (no on-disk persistence). */

#include <gio/gio.h>
#include <glib/gstdio.h>
#include <string.h>
#include <stdlib.h>

#include "xbg.h"

#define CFG_SUBDIR "xfce4/xfconf/xfce-perchannel-xml"

typedef struct _Elem Elem;
struct _Elem {
    gchar *name;
    gchar *type;
    gchar *value;
    gboolean is_value;
    GPtrArray *children;
};

typedef struct {
    GPtrArray *stack;
    Elem *root;
} Parser;

typedef struct {
    GHashTable *channels; /* char* -> GHashTable(char* -> GVariant*) */
} Store;

static Store *store;
static XfconfExported *skeleton;

static void
elem_free(gpointer data)
{
    Elem *e = data;
    g_free(e->name);
    g_free(e->type);
    g_free(e->value);
    if (e->children)
        g_ptr_array_unref(e->children);
    g_free(e);
}

static Elem *
elem_new(gboolean is_value)
{
    Elem *e = g_new0(Elem, 1);
    e->is_value = is_value;
    e->children = g_ptr_array_new_with_free_func(elem_free);
    return e;
}

static const gchar *
attr(const gchar **names, const gchar **values, const gchar *name)
{
    for (guint i = 0; names[i]; i++)
        if (!strcmp(names[i], name))
            return values[i];
    return NULL;
}

static void
xml_start(GMarkupParseContext *ctx, const gchar *name, const gchar **attr_names,
          const gchar **attr_values, gpointer data, GError **error)
{
    Parser *p = data;
    (void)ctx;
    (void)error;

    Elem *e = elem_new(!strcmp(name, "value"));
    if (!e->is_value)
        e->name = g_strdup(attr(attr_names, attr_values, "name"));
    e->type = g_strdup(attr(attr_names, attr_values, "type"));
    e->value = g_strdup(attr(attr_names, attr_values, "value"));
    if (p->stack->len > 0) {
        Elem *parent = g_ptr_array_index(p->stack, p->stack->len - 1);
        g_ptr_array_add(parent->children, e);
    } else {
        p->root = e;
    }
    g_ptr_array_add(p->stack, e);
}

static void
xml_end(GMarkupParseContext *ctx, const gchar *name, gpointer data, GError **error)
{
    Parser *p = data;
    (void)ctx;
    (void)name;
    (void)error;
    if (p->stack->len > 0)
        g_ptr_array_remove_index(p->stack, p->stack->len - 1);
}

static void
xml_text(GMarkupParseContext *ctx, const gchar *text, gsize len, gpointer data,
         GError **error)
{
    (void)ctx;
    (void)text;
    (void)len;
    (void)data;
    (void)error;
}

static const GMarkupParser markup_parser = {
    xml_start, xml_end, xml_text, NULL, NULL
};

static GVariant *
scalar_to_variant(const gchar *type, const gchar *value)
{
    if (!value)
        value = "";
    if (!strcmp(type, "string"))
        return g_variant_new_string(value);
    if (!strcmp(type, "int"))
        return g_variant_new_int32((gint32) g_ascii_strtoll(value, NULL, 0));
    if (!strcmp(type, "uint"))
        return g_variant_new_uint32((guint32) g_ascii_strtoull(value, NULL, 0));
    if (!strcmp(type, "int64"))
        return g_variant_new_int64(g_ascii_strtoll(value, NULL, 0));
    if (!strcmp(type, "uint64"))
        return g_variant_new_uint64(g_ascii_strtoull(value, NULL, 0));
    if (!strcmp(type, "double") || !strcmp(type, "float"))
        return g_variant_new_double(g_ascii_strtod(value, NULL));
    if (!strcmp(type, "bool"))
        return g_variant_new_boolean(!strcmp(value, "true") || !strcmp(value, "1"));
    if (!strcmp(type, "char") || !strcmp(type, "uchar") ||
        !strcmp(type, "int16") || !strcmp(type, "uint16"))
        return g_variant_new_int32((gint32) g_ascii_strtoll(value, NULL, 0));
    return g_variant_new_string(value);
}

static GVariant *
elem_to_variant(Elem *e);

static void
flatten_prop(Elem *e, const gchar *prefix, GHashTable *props);

static GVariant *
elem_to_variant(Elem *e)
{
    if (e->is_value)
        return scalar_to_variant(e->type, e->value);
    if (e->type && !strcmp(e->type, "array")) {
        GVariantBuilder b;
        g_variant_builder_init(&b, G_VARIANT_TYPE("av"));
        for (guint i = 0; i < e->children->len; i++) {
            Elem *c = g_ptr_array_index(e->children, i);
            if (c->is_value)
                g_variant_builder_add(&b, "v", scalar_to_variant(c->type, c->value));
        }
        return g_variant_builder_end(&b);
    }
    if (!e->type || !strcmp(e->type, "empty"))
        return NULL;
    return scalar_to_variant(e->type, e->value);
}

static void
flatten_prop(Elem *e, const gchar *prefix, GHashTable *props)
{
    gchar *path;
    GVariant *v;

    if (!e->name || !*e->name)
        return;

    path = g_strdup_printf("%s/%s", prefix, e->name);

    v = elem_to_variant(e);
    if (v != NULL)
        g_hash_table_insert(props, g_strdup(path), g_variant_ref_sink(v));

    for (guint i = 0; i < e->children->len; i++) {
        Elem *c = g_ptr_array_index(e->children, i);
        if (!c->is_value)
            flatten_prop(c, path, props);
    }

    g_free(path);
}

static GHashTable *
channel_table(const gchar *channel, gboolean create)
{
    GHashTable *t = g_hash_table_lookup(store->channels, channel);
    if (!t && create) {
        t = g_hash_table_new_full(g_str_hash, g_str_equal, g_free,
                                  (GDestroyNotify) g_variant_unref);
        g_hash_table_insert(store->channels, g_strdup(channel), t);
    }
    return t;
}

static void
load_file(const gchar *path, const gchar *channel)
{
    gchar *contents = NULL;
    gsize len = 0;
    GError *error = NULL;

    if (!g_file_get_contents(path, &contents, &len, &error)) {
        g_clear_error(&error);
        return;
    }

    Parser p = { g_ptr_array_new(), NULL };
    GMarkupParseContext *ctx = g_markup_parse_context_new(&markup_parser, 0, &p, NULL);
    if (!g_markup_parse_context_parse(ctx, contents, len, &error) ||
        !g_markup_parse_context_end_parse(ctx, &error)) {
        g_clear_error(&error);
    }
    g_markup_parse_context_free(ctx);
    g_ptr_array_unref(p.stack);

    if (p.root) {
        GHashTable *t = channel_table(channel, TRUE);
        for (guint i = 0; i < p.root->children->len; i++)
            flatten_prop(g_ptr_array_index(p.root->children, i), "", t);
        elem_free(p.root);
    }
    g_free(contents);
}

static void
load_dir(const gchar *base)
{
    gchar *dir = g_build_filename(base, CFG_SUBDIR, NULL);
    GDir *d = g_dir_open(dir, 0, NULL);
    if (d) {
        const gchar *name;
        while ((name = g_dir_read_name(d))) {
            if (!g_str_has_suffix(name, ".xml"))
                continue;
            gchar *channel = g_strndup(name, strlen(name) - 4);
            gchar *path = g_build_filename(dir, name, NULL);
            load_file(path, channel);
            g_free(path);
            g_free(channel);
        }
        g_dir_close(d);
    }
    g_free(dir);
}

static void
load_all(void)
{
    /* lowest priority first */
    load_dir("/usr/share");
    const gchar *const *dirs = g_get_system_config_dirs();
    for (gint i = (gint) g_strv_length((gchar **) dirs) - 1; i >= 0; i--)
        load_dir(dirs[i]);
    load_dir(g_get_user_config_dir());
}

/* ---- D-Bus methods ---- */

static GHashTable *
require_channel(const gchar *channel, GDBusMethodInvocation *inv)
{
    GHashTable *t = channel_table(channel, FALSE);
    if (!t) {
        t = channel_table(channel, TRUE);
    }
    (void)inv;
    return t;
}

static gboolean
on_list_channels(XfconfExported *sk, GDBusMethodInvocation *inv, gpointer data)
{
    (void)data;
    GList *names = g_hash_table_get_keys(store->channels);
    GPtrArray *arr = g_ptr_array_new();
    for (GList *l = names; l; l = l->next)
        g_ptr_array_add(arr, l->data);
    g_ptr_array_add(arr, NULL);
    xfconf_exported_complete_list_channels(sk, inv, (const gchar *const *) arr->pdata);
    g_ptr_array_unref(arr);
    g_list_free(names);
    return TRUE;
}

static gboolean
on_get_property(XfconfExported *sk, GDBusMethodInvocation *inv,
                const gchar *channel, const gchar *property, gpointer data)
{
    (void)data;
    GHashTable *t = require_channel(channel, inv);
    GVariant *v = g_hash_table_lookup(t, property);
    if (!v) {
        gchar *msg = g_strdup_printf("Property \"%s\" does not exist on channel \"%s\"",
                                     property, channel);
        g_dbus_method_invocation_return_dbus_error(inv,
            "org.xfce.Xfconf.Error.PropertyNotFound", msg);
        g_free(msg);
        return TRUE;
    }
    xfconf_exported_complete_get_property(sk, inv, g_variant_new_variant(v));
    return TRUE;
}

static gboolean
on_get_all_properties(XfconfExported *sk, GDBusMethodInvocation *inv,
                      const gchar *channel, const gchar *property_base,
                      gpointer data)
{
    (void)data;
    GHashTable *t = require_channel(channel, inv);
    GVariantBuilder b;
    gboolean all = !property_base || !*property_base || !strcmp(property_base, "/");
    gsize blen = all ? 0 : strlen(property_base);

    g_variant_builder_init(&b, G_VARIANT_TYPE("a{sv}"));
    GHashTableIter it;
    gpointer k, v;
    g_hash_table_iter_init(&it, t);
    while (g_hash_table_iter_next(&it, &k, &v)) {
        const gchar *key = k;
        if (!all) {
            if (strncmp(key, property_base, blen) != 0)
                continue;
            if (key[blen] != '/' && key[blen] != '\0')
                continue;
        }
        g_variant_builder_add(&b, "{sv}", key, g_variant_ref(v));
    }
    xfconf_exported_complete_get_all_properties(sk, inv, g_variant_builder_end(&b));
    return TRUE;
}

static gboolean
on_property_exists(XfconfExported *sk, GDBusMethodInvocation *inv,
                   const gchar *channel, const gchar *property, gpointer data)
{
    (void)data;
    GHashTable *t = require_channel(channel, inv);
    xfconf_exported_complete_property_exists(sk, inv,
                                             g_hash_table_contains(t, property));
    return TRUE;
}

static gboolean
on_is_property_locked(XfconfExported *sk, GDBusMethodInvocation *inv,
                      const gchar *channel, const gchar *property, gpointer data)
{
    (void)channel;
    (void)property;
    (void)data;
    xfconf_exported_complete_is_property_locked(sk, inv, FALSE);
    return TRUE;
}

static gboolean
on_set_property(XfconfExported *sk, GDBusMethodInvocation *inv,
                const gchar *channel, const gchar *property, GVariant *value,
                gpointer data)
{
    (void)data;
    GHashTable *t = require_channel(channel, inv);
    g_hash_table_insert(t, g_strdup(property), g_variant_ref_sink(value));
    xfconf_exported_emit_property_changed(sk, channel, property,
                                          g_variant_new_variant(value));
    xfconf_exported_complete_set_property(sk, inv);
    return TRUE;
}

static gboolean
on_reset_property(XfconfExported *sk, GDBusMethodInvocation *inv,
                  const gchar *channel, const gchar *property,
                  gboolean recursive, gpointer data)
{
    (void)data;
    GHashTable *t = require_channel(channel, inv);
    g_hash_table_remove(t, property);
    if (recursive) {
        GList *keys = g_hash_table_get_keys(t);
        GList *drop = NULL;
        gsize plen = strlen(property);
        for (GList *l = keys; l; l = l->next) {
            const gchar *k = l->data;
            if (!strncmp(k, property, plen) && k[plen] == '/')
                drop = g_list_prepend(drop, l->data);
        }
        for (GList *l = drop; l; l = l->next) {
            gchar *k = l->data;
            xfconf_exported_emit_property_removed(sk, channel, k);
            g_hash_table_remove(t, k);
        }
        g_list_free(drop);
        g_list_free(keys);
    } else {
        xfconf_exported_emit_property_removed(sk, channel, property);
    }
    xfconf_exported_complete_reset_property(sk, inv);
    return TRUE;
}



int
main(void)
{
    GError *error = NULL;
    GMainLoop *loop;

    store = g_new0(Store, 1);
    store->channels = g_hash_table_new_full(g_str_hash, g_str_equal, g_free,
                                            (GDestroyNotify) g_hash_table_unref);
    load_all();

    loop = g_main_loop_new(NULL, FALSE);
    GDBusConnection *conn = g_bus_get_sync(G_BUS_TYPE_SESSION, NULL, &error);
    if (!conn) {
        g_printerr("xfconfd-lite: cannot connect to session bus: %s\n",
                   error->message);
        return 1;
    }

    skeleton = g_object_new(XFCONF_TYPE_EXPORTED_SKELETON, NULL);
    g_signal_connect(skeleton, "handle-list-channels", G_CALLBACK(on_list_channels), NULL);
    g_signal_connect(skeleton, "handle-get-property", G_CALLBACK(on_get_property), NULL);
    g_signal_connect(skeleton, "handle-get-all-properties", G_CALLBACK(on_get_all_properties), NULL);
    g_signal_connect(skeleton, "handle-property-exists", G_CALLBACK(on_property_exists), NULL);
    g_signal_connect(skeleton, "handle-is-property-locked", G_CALLBACK(on_is_property_locked), NULL);
    g_signal_connect(skeleton, "handle-set-property", G_CALLBACK(on_set_property), NULL);
    g_signal_connect(skeleton, "handle-reset-property", G_CALLBACK(on_reset_property), NULL);

    if (!g_dbus_interface_skeleton_export(G_DBUS_INTERFACE_SKELETON(skeleton), conn,
                                          "/org/xfce/Xfconf", &error)) {
        g_printerr("xfconfd-lite: export failed: %s\n", error->message);
        return 1;
    }

    g_bus_own_name_on_connection(conn, "org.xfce.Xfconf",
                                 G_BUS_NAME_OWNER_FLAGS_NONE,
                                 NULL, NULL, NULL, NULL);
    g_printerr("xfconfd-lite: serving %u channel(s)\n",
               g_hash_table_size(store->channels));
    g_main_loop_run(loop);
    return 0;
}
