/* Oasis pkg/cproc/config.h */
static const char target[]         = "x86_64-linux-musl";
static const char *const startfiles[]    = {"-l", ":crt1.o", "-l", ":crti.o"};
static const char *const endfiles[]      = {"-l", "c", "-l", ":crtn.o"};
static const char *const preprocesscmd[] = {
	/* Oasis uses cpp; the Chimera clang package provides clang-cpp */
	"clang-cpp",

	/* clear preprocessor GNU C version */
	"-U", "__GNUC__",
	"-U", "__GNUC_MINOR__",

	/* we don't yet support these optional features */
	"-D", "__STDC_NO_ATOMICS__",
	"-D", "__STDC_NO_COMPLEX__",
	"-D", "__STDC_NO_VLA__",
	"-U", "__SIZEOF_INT128__",

	/* we don't generate position-independent code */
	"-U", "__PIC__",

	/* ignore attributes and extension markers */
	"-D", "__attribute__(x)=",
	"-D", "__extension__=",
};
static const char *const codegencmd[]    = {"qbe"};
/* use clang's integrated assembler and lld instead of GNU binutils */
static const char *const assemblecmd[]   = {"clang", "-c", "-x", "assembler"};
static const char *const linkcmd[]       = {"ld.lld", "-L", "/usr/lib", "-L", "/lib", "--dynamic-linker", "/lib/ld-musl-x86_64.so.1"};
