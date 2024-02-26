from pyduinocli.commands.base import CommandBase
from pyduinocli.constants import commands
from pyduinocli.constants import flags


class CompileCommand(CommandBase):
    """
    This class wraps the call to the :code:`compile` command of :code:`arduino-cli`.
    """

    def __init__(self, base_args):
        CommandBase.__init__(self, base_args)
        self._base_args.append(commands.COMPILE)

    def __call__(self,
                 sketch, build_cache_path=None, build_path=None, build_properties=None, fqbn=None, output_dir=None,
                 port=None, preprocess=None, show_properties=None, upload=None, verify=None,
                 warnings=None, libraries=None, library=None, optimize_for_debug=None, export_binaries=None,
                 programmer=None, clean=None, only_compilation_database=None, discovery_timeout=None, protocol=None,
                 board_options=None, encrypt_key=None, keys_keychain=None, sign_key=None, dump_profile=None,
                 profile=None, verbose=None):
        """
        Calls the :code:`compile` command

        :param sketch: The sketch to compile, can also be a path to a sketch
        :type sketch: str
        :param build_cache_path: Builds of 'core.a' are saved into this path to be cached and reused.
        :type build_cache_path: str or NoneType
        :param build_path: Path where to save compiled files. If omitted, a directory will be created in the default temporary path of your OS.
        :type build_path: str or NoneType
        :param build_properties: Override build properties with custom values.
        :type build_properties: list or NoneType
        :param fqbn: Fully Qualified Board Name, e.g.: arduino:avr:uno
        :type fqbn: str or NoneType
        :param output_dir: Save build artifacts in this directory.
        :type output_dir: str or NoneType
        :param port: Upload port, e.g.: COM10 or /dev/ttyACM0
        :type port: str or NoneType
        :param preprocess: Print preprocessed code to stdout instead of compiling.
        :type preprocess: bool or NoneType
        :param show_properties: Show build properties. The properties are expanded, use show_properties="unexpanded" if you want them exactly as they are defined. (default "disabled")
        :type show_properties: str, bool or NoneType
        :param upload: Upload the binary after the compilation.
        :type upload: bool or NoneType
        :param verify: Verify uploaded binary after the upload.
        :type verify: bool or NoneType
        :param warnings: Optional, can be "none", "default", "more" and "all". Defaults to "none". Used to tell gcc which warning level to use (-W flag). (default "none")
        :type warnings: str or NoneType
        :param libraries: List of custom libraries dir paths separated by commas. Or can be used multiple times for multiple libraries dir paths.
        :type libraries: list or NoneType
        :param library: List of paths to libraries root folders. Libraries set this way have top priority in case of conflicts. Can be used multiple times for different libraries.
        :type library: list or NoneType
        :param optimize_for_debug: Optional, optimize compile output for debugging, rather than for release.
        :type optimize_for_debug: bool or NoneType
        :param export_binaries: If set built binaries will be exported to the sketch folder.
        :type export_binaries: bool or NoneType
        :param programmer: Optional, use the specified programmer to upload.
        :type programmer: str or NoneType
        :param clean: Optional, cleanup the build folder and do not use any cached build.
        :type clean: bool or NoneType
        :param only_compilation_database: Just produce the compilation database, without actually compiling.
        :type only_compilation_database: bool or NoneType
        :param discovery_timeout: Max time to wait for port discovery, e.g.: 30s, 1m (default 5s)
        :type discovery_timeout: str or NoneType
        :param protocol: Upload port protocol, e.g: serial
        :type protocol: str or NoneType
        :param board_options: Board options
        :type board_options: dict or NoneType
        :param encrypt_key: The name of the custom encryption key to use to encrypt a binary during the compile process. Used only by the platforms that support it.
        :type encrypt_key: str or NoneType
        :param keys_keychain: The path of the dir to search for the custom keys to sign and encrypt a binary. Used only by the platforms that support it.
        :type keys_keychain: str or NoneType
        :param sign_key: The name of the custom signing key to use to sign a binary during the compile process. Used only by the platforms that support it.
        :type sign_key: str or NoneType
        :param dump_profile: Create and print a profile configuration from the build.
        :type dump_profile: bool or NoneType
        :param profile: Sketch profile to use
        :type profile: str or NoneType
        :param verbose: Optional, turns on verbose mode
        :type verbose: bool or NoneType
        :return: The output of the related command
        :rtype: dict
        """
        args = []
        if build_cache_path:
            args.extend([flags.BUILD_CACHE_PATH, CommandBase._strip_arg(build_cache_path)])
        if build_path:
            args.extend([flags.BUILD_PATH, CommandBase._strip_arg(build_path)])
        if build_properties:
            for build_property in build_properties:
                args.extend([flags.BUILD_PROPERTY, CommandBase._strip_arg(build_property)])
        if fqbn:
            args.extend([flags.FQBN, CommandBase._strip_arg(fqbn)])
        if output_dir:
            args.extend([flags.OUTPUT_DIR, CommandBase._strip_arg(output_dir)])
        if port:
            args.extend([flags.PORT, CommandBase._strip_arg(port)])
        if preprocess is True:
            args.append(flags.PREPROCESS)
        if show_properties is True:
            args.append(flags.SHOW_PROPERTIES)
        elif show_properties:
            args.append("%s=%s" % (flags.SHOW_PROPERTIES, CommandBase._strip_arg(show_properties)))
        if upload is True:
            args.append(flags.UPLOAD)
        if verify is True:
            args.append(flags.VERIFY)
        if warnings:
            args.extend([flags.WARNINGS, CommandBase._strip_arg(warnings)])
        if libraries:
            for l in libraries:
                args.extend([flags.LIBRARIES, CommandBase._strip_arg(l)])
        if library:
            for l in library:
                args.extend([flags.LIBRARY, CommandBase._strip_arg(l)])
        if optimize_for_debug is True:
            args.append(flags.OPTIMIZE_FOR_DEBUG)
        if export_binaries is True:
            args.append(flags.EXPORT_BINARIES)
        if programmer:
            args.extend([flags.PROGRAMMER, CommandBase._strip_arg(programmer)])
        if clean is True:
            args.append(flags.CLEAN)
        if only_compilation_database is True:
            args.append(flags.ONLY_COMPILATION_DATABASE)
        if discovery_timeout:
            args.extend([flags.DISCOVERY_TIMEOUT, CommandBase._strip_arg(discovery_timeout)])
        if protocol:
            args.extend([flags.PROTOCOL, CommandBase._strip_arg(protocol)])
        if board_options:
            for option_name, option_value in board_options.items():
                option = "%s=%s" % (CommandBase._strip_arg(option_name), CommandBase._strip_arg(option_value))
                args.extend([flags.BOARD_OPTIONS, option])
        if encrypt_key:
            args.extend([flags.ENCRYPT_KEY, CommandBase._strip_arg(encrypt_key)])
        if keys_keychain:
            args.extend([flags.KEYS_KEYCHAIN, CommandBase._strip_arg(keys_keychain)])
        if sign_key:
            args.extend([flags.SIGN_KEY, CommandBase._strip_arg(sign_key)])
        if dump_profile is True:
            args.append(flags.DUMP_PROFILE)
        if profile:
            args.extend([flags.PROFILE, CommandBase._strip_arg(profile)])
        if verbose is True:
            args.append(flags.VERBOSE)
        args.append(CommandBase._strip_arg(sketch))
        return self._exec(args)
