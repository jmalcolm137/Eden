// Use the locale from the environment instead of the build locale.
pref("intl.locale.requested", "");

// Eden has no default-browser helper; do not prompt on every start.
pref("browser.shell.checkDefaultBrowser", false);

// Let the package manager install add-ons into the application and system
// scopes without Firefox disabling them.
pref("extensions.autoDisableScopes", 11);
pref("extensions.shownSelectionUI", true);

// No sponsored top sites.
pref("browser.topsites.contile.enabled", false);

// Widevine (DRM) is not available for musl; do not offer it.
pref("media.gmp-widevinecdm.visible", false);
pref("media.gmp-widevinecdm.enabled", false);

// Do not download GMP binaries; media is decoded with system or bundled
// libraries.
pref("media.gmp-manager.updateEnabled", false);

// The telemetry shutdown ping can delay exit.
pref("toolkit.telemetry.shutdownPingSender.enabled", false);

// Privacy-preserving ad measurement needs a service Eden does not use.
pref("dom.private-attribution.submission.enabled", false);
