Inspect Extensions
==================

Extending Python `inspect` module to users and developers to get information
about packages, modules, classes and other members. Working on Python 3.8+.

Inspecting a package will recurse over all subpackages and modules, classes
and methods, functions and variables. Check out the examples in the end of
the README.

You can enter packages/module names. In the future it will be added classes
and functions as input too (example: pathlib.PurePath).


Installing, updating and uninstalling
#####################################


To install and/or update, do ::

    $ pip install -U inspect-extensions


To remove ::

    $ pip uninstall inspect-extensions


Running
#######


To get a minimalist output ::

    $ inspect-extensions


Examples
########


Help
----


.. code-block:: console

    $ inspect-extensions --help


.. code-block:: console

    usage: inspect_extensions.py [-h]
        [--colored COLORED] [--filter FILTER]
        [-p PACKAGES] [-m MODULES]
        [-c CLASSES] [-t METHODS] [-f FUNCTIONS] [-d DATA]
        [-a ALL_MEMBERS]
        [-b PUBLIC] [-o PROTECTED] [-i PRIVATE]
        [--encapsulation ENCAPSULATION] [-e ALL_ENCAPSULATION]
        [--count_members COUNT_MEMBERS] [--text_only TEXT_ONLY]
        [--special_classes SPECIAL_CLASSES]
        [--special_methods SPECIAL_METHODS]
        [--special_data SPECIAL_DATA]
        [--remove_special_classes REMOVE_SPECIAL_CLASSES]
        [--remove_special_methods REMOVE_SPECIAL_METHODS]
        [--remove_special_data REMOVE_SPECIAL_DATA]
        [--remove_special_members REMOVE_SPECIAL_MEMBERS]
        obj

    Inspect Extensions module.

    Python script that uses many modules from Python to exposes
    as many information that is possible to inspect packages.

    positional arguments:

    obj                   Input object (package, module, class)

    optional arguments:

    -h, --help            Show this help message and exit
    --count_members       Shows the number of members
    --colored             Print colored members
    --text_only           Print just text characters - not colorized

    --filter FILTER       [PACKAGE, MODULE, CLASS, METHOD, DATA, ALL]

    -p PACKAGES, --packages PACKAGES
        Show just packages
    -m MODULES, --modules MODULES
        Show just modules
    -c CLASSES, --classes CLASSES
        Show just classes
    -t METHODS, --methods METHODS
        Show just methods, must have 'self' as first arg
    -f FUNCTIONS, --functions FUNCTIONS
        Show just functions, not associated with any object
    -d DATA, --data DATA
        Show just data, variables
    -a ALL_MEMBERS, --all_members ALL_MEMBERS
        Show all members (DEFAULT)(packages, modules, classes, methods, functions, data)

    --encapsulation ENCAPSULATION [NONE, PUBLIC, PROTECTED, PRIVATE, ALL]

    -b PUBLIC, --public PUBLIC
        Show just public members (DEFAULT)
    -o PROTECTED, --protected PROTECTED
        Show just protected members
    -i PRIVATE, --private PRIVATE
        Show just private members
    -e ALL_ENCAPSULATION, --all_encapsulation ALL_ENCAPSULATION
        Show all encapsulation

    --special_classes SPECIAL_CLASSES
        Print special classes, '__' before and after name
    --special_methods SPECIAL_METHODS
        Print special methods, '__' before and after name
    --special_data SPECIAL_DATA
        Print special data, '__' before and after name

    --remove_special_classes REMOVE_SPECIAL_CLASSES
        Filter special classes, see special_classes
    --remove_special_methods REMOVE_SPECIAL_METHODS
        Filter special methods, see special_methods
    --remove_special_data REMOVE_SPECIAL_DATA
        Filter special data, see special_data
    --remove_special_members REMOVE_SPECIAL_MEMBERS
        Filter special members, see special_members

    --version
        Show program's version number and exit


Output for some packages
------------------------

The actual output has colored members (using `termcolor`)  listed for easy distinction.


.. code-block:: console

    $ inspect-extensions os.path


.. code-block:: console

    PREFIX........................ NAME.......................... TYPE...... ENCAPS.... EVINDECED...... type()......... inspect.............
    os.path....................... posixpath..................... MODULE.... PUBLIC.... ............... module......... ['ismodule']........
    os.path....................... _get_sep...................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... _joinrealpath................. METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... _varprog...................... DATA...... PROTECTED. ATTRIBUTE...... NoneType....... []..................
    os.path....................... _varprogb..................... DATA...... PROTECTED. ATTRIBUTE...... NoneType....... []..................
    os.path....................... abspath....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... altsep........................ DATA...... PUBLIC.... ATTRIBUTE...... NoneType....... []..................
    os.path....................... basename...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... commonpath.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... commonprefix.................. METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... curdir........................ DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... defpath....................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... devnull....................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... dirname....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... exists........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... expanduser.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... expandvars.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... extsep........................ DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... genericpath................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    os.path....................... getatime...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... getctime...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... getmtime...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... getsize....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... isabs......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... isdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... isfile........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... islink........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... ismount....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... join.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... lexists....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... normcase...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... normpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... os............................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    os.path....................... pardir........................ DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... pathsep....................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... realpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... relpath....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... samefile...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... sameopenfile.................. METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... samestat...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... sep........................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    os.path....................... split......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... splitdrive.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... splitext...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    os.path....................... stat.......................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    os.path....................... supports_unicode_filenames.... DATA...... PUBLIC.... ATTRIBUTE...... bool........... []..................
    os.path....................... sys........................... DATA...... PUBLIC.... ............... module......... ['ismodule']........


.. code-block:: console

    $ inspect-extensions termcolor


.. code-block:: console

    PREFIX........................ NAME.......................... TYPE...... ENCAPS.... EVINDECED...... type()......... inspect.............
    termcolor..................... __main__...................... MODULE.... PUBLIC.... ............... module......... ['ismodule']........
    termcolor.__main__............ annotations................... DATA...... PUBLIC.... ATTRIBUTE...... _Feature....... []..................
    termcolor.__main__............ cprint........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    termcolor.__main__............ os............................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    termcolor..................... termcolor..................... MODULE.... PUBLIC.... ............... module......... ['ismodule']........
    termcolor.termcolor........... ATTRIBUTES.................... DATA...... PUBLIC.... ATTRIBUTE...... dict........... []..................
    termcolor.termcolor........... Any........................... DATA...... PUBLIC.... ATTRIBUTE...... _SpecialForm... []..................
    termcolor.termcolor........... COLORS........................ DATA...... PUBLIC.... ATTRIBUTE...... dict........... []..................
    termcolor.termcolor........... HIGHLIGHTS.................... DATA...... PUBLIC.... ATTRIBUTE...... dict........... []..................
    termcolor.termcolor........... Iterable...................... DATA...... PUBLIC.... ATTRIBUTE...... _SpecialGenericAlias []..................
    termcolor.termcolor........... RESET......................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    termcolor.termcolor........... _can_do_colour................ METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    termcolor.termcolor........... annotations................... DATA...... PUBLIC.... ATTRIBUTE...... _Feature....... []..................
    termcolor.termcolor........... colored....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    termcolor.termcolor........... cprint........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    termcolor.termcolor........... os............................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    termcolor.termcolor........... sys........................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    termcolor.termcolor........... warnings...................... DATA...... PUBLIC.... ............... module......... ['ismodule']........


.. code-block:: console

    $ inspect-extensions pathlib


.. code-block:: console

    PREFIX........................ NAME.......................... TYPE...... ENCAPS.... EVINDECED...... type()......... inspect.............
    pathlib....................... pathlib....................... MODULE.... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... EBADF......................... DATA...... PUBLIC.... ATTRIBUTE...... int............ []..................
    pathlib....................... EINVAL........................ DATA...... PUBLIC.... ATTRIBUTE...... int............ []..................
    pathlib....................... ELOOP......................... DATA...... PUBLIC.... ATTRIBUTE...... int............ []..................
    pathlib....................... ENOENT........................ DATA...... PUBLIC.... ATTRIBUTE...... int............ []..................
    pathlib....................... ENOTDIR....................... DATA...... PUBLIC.... ATTRIBUTE...... int............ []..................
    pathlib....................... Path.......................... CLASS..... PUBLIC.... TYPE........... type........... ['isclass'].........
    pathlib.Path.................. _accessor..................... DATA...... PROTECTED. ATTRIBUTE...... _NormalAccessor []..................
    pathlib.Path.................. _cached_cparts................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. _cparts....................... DATA...... PROTECTED. PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. _format_parsed_parts.......... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.Path.................. _from_parsed_parts............ METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.Path.................. _from_parts................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.Path.................. _hash......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. _make_child................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. _make_child_relpath........... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. _parse_args................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.Path.................. _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. _pparts....................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. _str.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.Path.................. absolute...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. anchor........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. as_posix...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. as_uri........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. chmod......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. cwd........................... METHOD.... PUBLIC.... ............... method......... ['ismethod', 'isroutine']
    pathlib.Path.................. drive......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. exists........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. expanduser.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. glob.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.Path.................. group......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. hardlink_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. home.......................... METHOD.... PUBLIC.... ............... method......... ['ismethod', 'isroutine']
    pathlib.Path.................. is_absolute................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_block_device............... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_char_device................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_dir........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_fifo....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_file....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_mount...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_relative_to................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_socket..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. is_symlink.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. iterdir....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.Path.................. joinpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. lchmod........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. link_to....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. lstat......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. match......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. mkdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. name.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. open.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. owner......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. parent........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. parents....................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. parts......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. read_bytes.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. read_text..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. readlink...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. relative_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. rename........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. replace....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. resolve....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. rglob......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.Path.................. rmdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. root.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. samefile...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. stat.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. stem.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. suffix........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. suffixes...................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.Path.................. symlink_to.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. touch......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. unlink........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. with_name..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. with_stem..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. with_suffix................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. write_bytes................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.Path.................. write_text.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... PosixPath..................... CLASS..... PUBLIC.... TYPE........... type........... ['isclass'].........
    pathlib.PosixPath............. _accessor..................... DATA...... PROTECTED. ATTRIBUTE...... _NormalAccessor []..................
    pathlib.PosixPath............. _cached_cparts................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. _cparts....................... DATA...... PROTECTED. PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. _flavour...................... DATA...... PROTECTED. ATTRIBUTE...... _PosixFlavour.. []..................
    pathlib.PosixPath............. _format_parsed_parts.......... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PosixPath............. _from_parsed_parts............ METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PosixPath............. _from_parts................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PosixPath............. _hash......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. _make_child................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. _make_child_relpath........... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. _parse_args................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PosixPath............. _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. _pparts....................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. _str.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PosixPath............. absolute...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. anchor........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. as_posix...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. as_uri........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. chmod......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. cwd........................... METHOD.... PUBLIC.... ............... method......... ['ismethod', 'isroutine']
    pathlib.PosixPath............. drive......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. exists........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. expanduser.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. glob.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.PosixPath............. group......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. hardlink_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. home.......................... METHOD.... PUBLIC.... ............... method......... ['ismethod', 'isroutine']
    pathlib.PosixPath............. is_absolute................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_block_device............... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_char_device................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_dir........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_fifo....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_file....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_mount...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_relative_to................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_socket..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. is_symlink.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. iterdir....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.PosixPath............. joinpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. lchmod........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. link_to....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. lstat......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. match......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. mkdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. name.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. open.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. owner......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. parent........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. parents....................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. parts......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. read_bytes.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. read_text..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. readlink...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. relative_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. rename........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. replace....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. resolve....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. rglob......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.PosixPath............. rmdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. root.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. samefile...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. stat.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. stem.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. suffix........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. suffixes...................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PosixPath............. symlink_to.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. touch......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. unlink........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. with_name..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. with_stem..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. with_suffix................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. write_bytes................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PosixPath............. write_text.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... PurePath...................... CLASS..... PUBLIC.... TYPE........... type........... ['isclass'].........
    pathlib.PurePath.............. _cached_cparts................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. _cparts....................... DATA...... PROTECTED. PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. _format_parsed_parts.......... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePath.............. _from_parsed_parts............ METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePath.............. _from_parts................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePath.............. _hash......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. _make_child................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. _parse_args................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePath.............. _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. _pparts....................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. _str.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePath.............. anchor........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. as_posix...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. as_uri........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. drive......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. is_absolute................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. is_relative_to................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. joinpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. match......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. name.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. parent........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. parents....................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. parts......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. relative_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. root.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. stem.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. suffix........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. suffixes...................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePath.............. with_name..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. with_stem..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePath.............. with_suffix................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... PurePosixPath................. CLASS..... PUBLIC.... TYPE........... type........... ['isclass'].........
    pathlib.PurePosixPath......... _cached_cparts................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... _cparts....................... DATA...... PROTECTED. PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... _flavour...................... DATA...... PROTECTED. ATTRIBUTE...... _PosixFlavour.. []..................
    pathlib.PurePosixPath......... _format_parsed_parts.......... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePosixPath......... _from_parsed_parts............ METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePosixPath......... _from_parts................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePosixPath......... _hash......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... _make_child................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... _parse_args................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PurePosixPath......... _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... _pparts....................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... _str.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PurePosixPath......... anchor........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... as_posix...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... as_uri........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... drive......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... is_absolute................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... is_relative_to................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... joinpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... match......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... name.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... parent........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... parents....................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... parts......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... relative_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... root.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... stem.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... suffix........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... suffixes...................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PurePosixPath......... with_name..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... with_stem..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PurePosixPath......... with_suffix................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... PureWindowsPath............... CLASS..... PUBLIC.... TYPE........... type........... ['isclass'].........
    pathlib.PureWindowsPath....... _cached_cparts................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... _cparts....................... DATA...... PROTECTED. PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... _flavour...................... DATA...... PROTECTED. ATTRIBUTE...... _WindowsFlavour []..................
    pathlib.PureWindowsPath....... _format_parsed_parts.......... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PureWindowsPath....... _from_parsed_parts............ METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PureWindowsPath....... _from_parts................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PureWindowsPath....... _hash......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... _make_child................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... _parse_args................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.PureWindowsPath....... _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... _pparts....................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... _str.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.PureWindowsPath....... anchor........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... as_posix...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... as_uri........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... drive......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... is_absolute................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... is_relative_to................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... joinpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... match......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... name.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... parent........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... parents....................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... parts......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... relative_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... root.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... stem.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... suffix........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... suffixes...................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.PureWindowsPath....... with_name..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... with_stem..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.PureWindowsPath....... with_suffix................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... WindowsPath................... CLASS..... PUBLIC.... TYPE........... type........... ['isclass'].........
    pathlib.WindowsPath........... _accessor..................... DATA...... PROTECTED. ATTRIBUTE...... _NormalAccessor []..................
    pathlib.WindowsPath........... _cached_cparts................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... _cparts....................... DATA...... PROTECTED. PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... _flavour...................... DATA...... PROTECTED. ATTRIBUTE...... _WindowsFlavour []..................
    pathlib.WindowsPath........... _format_parsed_parts.......... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.WindowsPath........... _from_parsed_parts............ METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.WindowsPath........... _from_parts................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.WindowsPath........... _hash......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... _make_child................... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... _make_child_relpath........... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... _parse_args................... METHOD.... PROTECTED. ............... method......... ['ismethod', 'isroutine']
    pathlib.WindowsPath........... _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... _pparts....................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... _str.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib.WindowsPath........... absolute...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... anchor........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... as_posix...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... as_uri........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... chmod......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... cwd........................... METHOD.... PUBLIC.... ............... method......... ['ismethod', 'isroutine']
    pathlib.WindowsPath........... drive......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... exists........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... expanduser.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... glob.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.WindowsPath........... group......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... hardlink_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... home.......................... METHOD.... PUBLIC.... ............... method......... ['ismethod', 'isroutine']
    pathlib.WindowsPath........... is_absolute................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_block_device............... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_char_device................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_dir........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_fifo....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_file....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_mount...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_relative_to................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_socket..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... is_symlink.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... iterdir....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.WindowsPath........... joinpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... lchmod........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... link_to....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... lstat......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... match......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... mkdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... name.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... open.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... owner......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... parent........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... parents....................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... parts......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... read_bytes.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... read_text..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... readlink...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... relative_to................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... rename........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... replace....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... resolve....................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... rglob......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib.WindowsPath........... rmdir......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... root.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... samefile...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... stat.......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... stem.......................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... suffix........................ DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... suffixes...................... DATA...... PUBLIC.... PROPERTY....... property....... ['isdatadescriptor']
    pathlib.WindowsPath........... symlink_to.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... touch......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... unlink........................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... with_name..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... with_stem..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... with_suffix................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... write_bytes................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib.WindowsPath........... write_text.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _Accessor..................... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib....................... _Flavour...................... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._Flavour.............. join_parsed_parts............. METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._Flavour.............. parse_parts................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _IGNORED_ERROS................ DATA...... PROTECTED. ATTRIBUTE...... tuple.......... []..................
    pathlib....................... _IGNORED_WINERRORS............ DATA...... PROTECTED. ATTRIBUTE...... tuple.......... []..................
    pathlib....................... _NormalAccessor............... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._NormalAccessor....... expanduser.................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._NormalAccessor....... group......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._NormalAccessor....... owner......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._NormalAccessor....... realpath...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._NormalAccessor....... touch......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _PathParents.................. CLASS..... PROTECTED. TYPE........... ABCMeta........ ['isclass'].........
    pathlib._PathParents.......... _abc_impl..................... DATA...... PROTECTED. ATTRIBUTE...... _abc_data...... []..................
    pathlib._PathParents.......... _drv.......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib._PathParents.......... _parts........................ DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib._PathParents.......... _pathcls...................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib._PathParents.......... _root......................... DATA...... PROTECTED. PROPERTY....... member_descriptor ['isdatadescriptor', 'ismemberdescriptor']
    pathlib._PathParents.......... count......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PathParents.......... index......................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _PosixFlavour................. CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._PosixFlavour......... altsep........................ DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    pathlib._PosixFlavour......... casefold...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... casefold_parts................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... compile_pattern............... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... has_drv....................... DATA...... PUBLIC.... ATTRIBUTE...... bool........... []..................
    pathlib._PosixFlavour......... is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... is_supported.................. DATA...... PUBLIC.... ATTRIBUTE...... bool........... []..................
    pathlib._PosixFlavour......... join_parsed_parts............. METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... make_uri...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... parse_parts................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._PosixFlavour......... pathmod....................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib._PosixFlavour......... sep........................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    pathlib._PosixFlavour......... splitroot..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _PreciseSelector.............. CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._PreciseSelector...... _select_from.................. METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib._PreciseSelector...... select_from................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _RecursiveWildcardSelector.... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._RecursiveWildcardSele _iterate_directories.......... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib._RecursiveWildcardSele _select_from.................. METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib._RecursiveWildcardSele select_from................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _Selector..................... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._Selector............. select_from................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _TerminatingSelector.......... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._TerminatingSelector.. _select_from.................. METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib....................... _WINERROR_CANT_RESOLVE_FILENAME DATA...... PROTECTED. ATTRIBUTE...... int............ []..................
    pathlib....................... _WINERROR_INVALID_NAME........ DATA...... PROTECTED. ATTRIBUTE...... int............ []..................
    pathlib....................... _WINERROR_NOT_READY........... DATA...... PROTECTED. ATTRIBUTE...... int............ []..................
    pathlib....................... _WildcardSelector............. CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._WildcardSelector..... _select_from.................. METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isgeneratorfunction', 'isroutine']
    pathlib._WildcardSelector..... select_from................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _WindowsFlavour............... CLASS..... PROTECTED. TYPE........... type........... ['isclass'].........
    pathlib._WindowsFlavour....... _split_extended_path.......... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... altsep........................ DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    pathlib._WindowsFlavour....... casefold...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... casefold_parts................ METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... compile_pattern............... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... drive_letters................. DATA...... PUBLIC.... ATTRIBUTE...... set............ []..................
    pathlib._WindowsFlavour....... ext_namespace_prefix.......... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    pathlib._WindowsFlavour....... has_drv....................... DATA...... PUBLIC.... ATTRIBUTE...... bool........... []..................
    pathlib._WindowsFlavour....... is_reserved................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... is_supported.................. DATA...... PUBLIC.... ATTRIBUTE...... bool........... []..................
    pathlib._WindowsFlavour....... join_parsed_parts............. METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... make_uri...................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... parse_parts................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib._WindowsFlavour....... pathmod....................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib._WindowsFlavour....... reserved_names................ DATA...... PUBLIC.... ATTRIBUTE...... set............ []..................
    pathlib._WindowsFlavour....... sep........................... DATA...... PUBLIC.... ATTRIBUTE...... str............ []..................
    pathlib._WindowsFlavour....... splitroot..................... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _ignore_error................. METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _is_wildcard_pattern.......... METHOD.... PROTECTED. FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... _make_selector................ DATA...... PROTECTED. ............... _lru_cache_wrapper ['ismethoddescriptor', 'isroutine']
    pathlib....................... _normal_accessor.............. DATA...... PROTECTED. ATTRIBUTE...... _NormalAccessor []..................
    pathlib....................... _posix_flavour................ DATA...... PROTECTED. ATTRIBUTE...... _PosixFlavour.. []..................
    pathlib....................... _windows_flavour.............. DATA...... PROTECTED. ATTRIBUTE...... _WindowsFlavour []..................
    pathlib....................... fnmatch....................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... functools..................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... io............................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... ntpath........................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... os............................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... posixpath..................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... re............................ DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... sys........................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
    pathlib....................... urlquote_from_bytes........... METHOD.... PUBLIC.... FUNCTION....... function....... ['isfunction', 'isroutine']
    pathlib....................... warnings...................... DATA...... PUBLIC.... ............... module......... ['ismodule']........
