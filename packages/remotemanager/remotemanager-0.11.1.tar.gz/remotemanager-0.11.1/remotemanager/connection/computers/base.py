import copy
import json
import typing
import importlib
import warnings

import yaml

from typing import Union

from remotemanager.connection.url import URL
from remotemanager.connection.computers.resource import Resource, Resources
from remotemanager.storage.function import Function
from remotemanager.storage.sendablemixin import get_class_storage, INTERNAL_STORAGE_KEYS


class BaseComputer(URL):
    """
    Base computer module for HPC connection management.

    Extend this class for connecting to your machine
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._extra = ""
        self._internal_extra = ""

    def __setattr__(self, key, value):
        """
        If the set `key` attribute is a Resource, and `value` is not a Resource,
        instead set the `value` of that attribute

        Args:
            key:
                attribute name to set
            value:
                value to set to

        Returns:
            None
        """
        # if this resource already exists, and we're _not_ trying to set a new resource,
        # set the value of the Resource to value
        if key in self.__dict__ and not isinstance(value, Resource):
            if isinstance(getattr(self, key), Resource):
                # need to get before we can set
                getattr(self, key).value = value
                return

        object.__setattr__(self, key, value)

    def get_parser(self):
        parser = getattr(self, "parser", None)

        if parser is None:
            # legacy _parser
            parser = getattr(self, "_parser", None)

        return parser

    @classmethod
    def from_dict(cls, spec: dict, **url_args):
        """
        Create a Computer class from a `spec` dictionary. The required values are:

        - resources:
            a dict of required resources for the machine (mpi, nodes, queue, etc.)
        - resource_parser:
            a function which takes a dictionary of {resource: Option}, returning a list
            of valid jobscript lines

        You can also provide some optional arguments:

        - required_or:
            list of resources, ONE of which is required. Note that this must be a
            _list_ of dicts, one for each or "block"
        - optional_resources:
            as with `resources`, but these will not be stored as required values
        - optional_defaults:
            provide defaults for the names given in optional_resources. When adding the
            optional arg, the optional_defaults will be checked to see if a default is
            provided
        - host:
            machine hostname. Note that this _must_ be available for a job run, but if
            not provided within the spec, can be added later with
            ``url.host = 'hostname'``
        - submitter:
            override the default submitter
        - python:
            override the default python
        - extra:
            any extra lines that should be appended after the resource specification.
            Note that this includes module loads/swaps, but this can be specified on a
            per-job basis, rather than locking it into the `Computer`

        The `resources` specification is in `notebook`:`machine` order. That is to say
        that the `key` is what will be required in the _notebook_, and the `value` is
        what is placed in the jobscript:

        >>> spec = {'resources': {'mpi': 'ntasks'}, ...}
        >>> url = BaseComputer.from_dict(spec)
        >>> url.mpi = 12
        >>> url.script()
        >>> "--ntasks=12"

        Args:
            spec (dict):
                input dictionary
            url_args:
                any arguments to be passed directly to the created `url`

        Returns:
            Computer class as per input spec
        """
        from remotemanager import Logger

        payload = copy.deepcopy(spec)
        # check if we have a stored Computer Class
        class_store_key = INTERNAL_STORAGE_KEYS["CLASS_STORAGE_KEY"]
        if class_store_key in payload:
            class_storage = payload[class_store_key]
            Logger.debug(f"using class storage {class_storage}")
            # first, try grab the module
            try:
                mod = importlib.import_module(class_storage["mod"])
                # then try import from that module
                try:
                    cls = getattr(mod, class_storage["name"])
                except AttributeError:  # inner import error, no class
                    warnings.warn(f"Could not import class {class_storage['name']}")
            except ModuleNotFoundError:  # outer import error, no module
                warnings.warn(f"Could not import module {class_storage['mod']}")

        Logger.debug(f"from_dict called on {cls}")

        # convert the parser back into a function
        def unpack(parser_data) -> Function:
            """
            Parser data can be either a string, dict or callable.
            Handle all and return the Function

            Args:
                parser_data:
                    stored parser
            Returns:
                Function
            """
            if callable(parser_data):
                return Function(parser_data, force_self=True)
            if isinstance(parser_data, str):
                return Function(parser_data, force_self=True)
            if isinstance(parser_data, dict):
                return Function.unpack(parser_data, force_self=True)
            if isinstance(parser_data, Function):
                return parser_data

            Logger.warning(
                f"no string found, setting {type(parser_source)} "
                f"{parser_source} as parser"
            )
            return parser_data

        parser = None
        parser_source = payload.pop("resource_parser_source", None)
        if parser_source is not None:
            Logger.debug("generating parser from source code")
            parser = unpack(parser_source)
        else:  # legacy unpack method
            Logger.debug("parser source code not found at resource_parser_source")
            parser_source = payload.pop("resource_parser", None)
            parser = unpack(parser_source)

        # parser object must be assigned (monkey patched) at class level, or it will
        # not be a bound-method, which is required for `self` and inspect to work
        if parser is not None:
            Logger.debug("assigning parser object at parser")
            cls.parser = parser.object
            cls._parser_source = parser.raw_source
        else:
            Logger.debug("parser NOT assigned")

        # create a new class
        computer = cls()
        if parser is not None:
            computer._parser_source = parser.raw_source

        # add the resource storing objects to the class
        required_resources = payload.pop("resources")
        oldstyle = False
        for field, resource_args in required_resources.items():
            if isinstance(resource_args, str):
                # this is a consequence of an older style "name": "flag" spec
                # cast to new type by setting it to "flag"
                # other args can be set later
                oldstyle = True
                resource_args = {"flag": resource_args, "optional": False}

            resource = Resource(name=field, **resource_args)
            setattr(computer, field, resource)

        if oldstyle:
            optional = payload.pop("optional_resources", {})
            for name, flag in optional.items():
                resource = Resource(name=name, flag=flag)
                setattr(computer, name, resource)

            required_or = payload.pop("required_or", [])
            for group in required_or:
                for name, flag in group.items():
                    replaces = [n for n in group if n != name]
                    resource = Resource(
                        name=name, flag=flag, optional=False, replaces=replaces
                    )
                    setattr(computer, name, resource)

            defaults = payload.pop("optional_defaults")
            for name, default in defaults.items():
                computer.resource_dict[name].default = default

        if oldstyle:
            print(
                "WARNING! Old style import detected. "
                "You should check the validity of the "
                "resulting Computer then re-dump to yaml."
            )

        # add any extra content
        for key, val in payload.items():
            setattr(computer, key, val)

        for key, val in url_args.items():
            setattr(computer, key, val)

        return computer

    def to_dict(self, include_extra: bool = True) -> dict:
        """
        Generate a spec dict from this Computer

        Args:
            include_extra:
                includes the `extra` property if True (default True)

        Returns:
            dict
        """
        self._logger.debug(f"to_dict called on {self}")

        def create_entry(obj):
            data = {"flag": obj.flag}

            if obj.min is not None:
                data["min"] = obj.min
            if obj.max is not None:
                data["max"] = obj.max
            if getattr(obj, "default", None) is not None:
                data["default"] = obj.default
            if not obj.optional:
                data["optional"] = False
            if len(obj.requires) != 0:
                data["requires"] = obj.requires
            if len(obj.replaces) != 0:
                data["replaces"] = obj.replaces
            if obj.format is not None:
                data["format"] = obj.format

            return data

        # gather all non resource objects
        spec = {
            k: getattr(self, k)
            for k in self.__dict__
            if k not in self.resources and not k.startswith("_")
        }

        spec["resources"] = {n: create_entry(r) for n, r in self.resource_dict.items()}

        if getattr(self, "_parser_source", None) is not None:
            parser = Function(self._parser_source, force_self=True).raw_source
        else:
            parser = self.get_parser()
            try:
                # avoids a strange error where the parser source cant be found.
                # likely loads it into memory where `inspect` can access it
                # noinspection PyStatementEffect
                parser
            except AttributeError:
                pass

        if isinstance(parser, Function):
            spec["resource_parser_source"] = parser.raw_source
        elif parser is not None:
            spec["resource_parser_source"] = Function(
                parser, force_self=True
            ).raw_source
        # grab `extra` if requested
        if include_extra and self.extra is not None:
            spec["extra"] = self.extra
        # round up missing package inclusions
        collect = ["submitter", "shebang", "pragma"]
        for name in collect:
            try:
                spec[name] = getattr(self, name)
            except AttributeError:
                pass
        # parser object is not required, and looks ugly
        if "parser" in spec:
            del spec["parser"]
        cls_store_key = INTERNAL_STORAGE_KEYS["CLASS_STORAGE_KEY"]
        spec[cls_store_key] = get_class_storage(self)
        return spec

    @classmethod
    def from_yaml(cls, filepath: str, **url_args):
        """
        Create a Computer from `filepath`.

        Args:
            filepath:
                path containing yaml computer spec
            **url_args:
                extra args to be passed to the internal URL

        Returns:
            BaseComputer
        """
        if isinstance(filepath, str):
            try:
                with open(filepath, "r") as o:
                    data = yaml.safe_load(o)
            except OSError:
                data = yaml.safe_load(filepath)
        else:
            data = yaml.safe_load(filepath)

        return cls.from_dict(data, **url_args)

    def to_yaml(
        self, filepath: Union[str, typing.IO, None] = None, include_extra: bool = True
    ) -> Union[str, None]:
        """
        Dump a computer to yaml `filepath`.

        Args:
            filepath:
                path containing yaml computer spec
            include_extra:
                includes the `extra` property if True (default True)
        """
        data = self.to_dict(include_extra)
        # source will simply not print correctly with base yaml
        # extract it and do it manually, if it exists
        if "resource_parser_source" in data:
            parser_string = ["resource_parser_source: |"] + [
                f"    {line}" for line in data.pop("resource_parser_source").split("\n")
            ]
            # dump the remaining content to string
            prepared = yaml.dump(data)
            # append the cleaned string
            prepared += "\n".join(parser_string)
        else:
            prepared = yaml.dump(data)

        if filepath is None:  # "dump" to string
            return prepared
        elif isinstance(filepath, str):  # dump to path
            with open(filepath, "w+") as o:
                o.write(prepared)
        else:  # assume file handler and dump there
            filepath.write(prepared)

    @classmethod
    def from_repo(
        cls,
        name: str,
        branch: str = "main",
        repo: str = "https://gitlab.com/l_sim/remotemanager-computers/",
        **url_args,
    ):
        """
        Attempt to access the remote-computers repo, and pull the computer with name
        `name`

        Args:
            name (str):
                computer name to target
            branch (str):
                repo branch (defaults to main)
            repo (str):
                repo web address (defaults to main l_sim repo)

        Returns:
            BaseComputer instance
        """
        import requests
        from remotemanager.utils import ensure_filetype

        def download_file(file_url, filename):
            response = requests.get(file_url)

            if response.status_code == requests.codes.ok:
                # Save the file
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"Grabbed file '{filename}'")
            else:
                raise RuntimeError(f"Could not find a file at: {file_url}")

        filename = ensure_filetype(name, "yaml").lower()
        url = f"{repo}-/raw/{branch}/storage/{filename}"

        print(f"polling url {url}")

        download_file(url, filename)

        return cls.from_yaml(filename, **url_args)

    def generate_cell(
        self, name: Union[str, None] = None, return_string: bool = False
    ) -> Union[None, str]:
        """
        Prints out copyable source which regenerates this Computer

        Args:
            name (str, None):
                Optional name for new computer. Defaults to `new`
            return_string (bool):
                Also returns the string if True. Defaults to False

        Returns:
            (None, str)
        """
        if name is None:
            name = "new"
        output = [
            "# Copy the following into a jupyter cell or python script "
            "to generate a modifiable source",
            "\n# Parser source code",
        ]
        source = self.to_dict()

        try:
            parser = self.get_parser()
            if not isinstance(parser, Function):
                parser = Function(parser)

            output.append(parser.raw_source)

            source.pop("resource_parser_source")
            # use json.dumps with indent=4 to format dict
            output.append(
                f"\n# JSON compatibility\n"
                f"true = True\n"
                f"false = False\n\n"
                f"# spec dict\n\nspec = {json.dumps(source, indent=4)}"
            )
            output.append(f'spec["resource_parser"] = {parser.name}')

            output.append(f"\n{name} = BaseComputer.from_dict(spec)")

        except TypeError:
            output.append(
                f"# JSON compatibility\n"
                f"true = True\n"
                f"false = False\n\n"
                f"# spec dict\n\nspec = {json.dumps(source, indent=4)}"
            )
            output.append(f"\n{name} = BaseComputer.from_dict(spec)")

        output = "\n".join(output)

        print(output)

        if return_string:
            return output

    @property
    def resources(self) -> list:
        return sorted([k for k, v in self.__dict__.items() if isinstance(v, Resource)])

    @property
    def resource_objects(self) -> list:
        return [v for k, v in self.__dict__.items() if isinstance(v, Resource)]

    @property
    def resource_dict(self) -> dict:
        return {k.strip(): getattr(self, k) for k in self.resources}

    @property
    def required(self) -> list:
        """
        Returns a list of required arguments
        """
        required = []

        def append_if(item):
            if item not in required:
                required.append(item)

        for name, resource in self.resource_dict.items():
            if not resource.optional:
                append_if(name)
            for name in resource.requires:
                append_if(name)

        return required

    @property
    def missing(self) -> list:
        """
        Returns the currently missing arguments
        """
        missing = []
        covered = []
        for resource in self.resource_objects:
            # this resource has a value, so is not missing, and can replace others
            if resource:
                covered.append(resource.name)
                for name in resource.replaces:
                    if name in missing:
                        missing.remove(name)
                    covered.append(name)
            # resource is missing a value and is non optional
            elif not resource and not resource.optional:
                if resource.name not in covered:
                    missing.append(resource.name)

            for name in resource.requires:
                if name not in covered and not self.resource_dict[name]:
                    missing.append(name)

        return missing

    @property
    def valid(self):
        return len(self.missing) == 0

    def update_resources(self, **kwargs):
        """
        Set any arguments passed to the script call

        Args:
            **kwargs:
                kwarg updates e.g. mpi=128
        Returns:
            None
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    def parser(self, resources) -> list:
        """
        Default parser for use on basic "SLURM style" machines.

        Will iterate over resource objects, creating a script of the format:

        {pragma} --{flag}={value}

        ..note::
            This method can (and should) be overidden for a custom parser.

        Args:
            resources:
                Resources object, to be created by BaseComputer

        Returns:
            list of resource lines
        """
        output = []
        for r in resources:
            if r:
                output.append(r.resource_line)

        return output

    @property
    def extra(self):
        return self._internal_extra + self._extra

    @extra.setter
    def extra(self, external):
        self._extra = external

    def script(self, **kwargs) -> str:
        """
        Takes job arguments and produces a valid jobscript

        Returns:
            (str):
                script
        """
        self.update_resources(**kwargs)
        if not self.valid:
            raise RuntimeError(f"missing required arguments: {self.missing}")

        pragma = getattr(self, "pragma", None)
        tag = getattr(self, "resource_tag", None)
        sep = getattr(self, "resource_separator", None)
        submit_args = Resources(
            resources=self.resource_objects,
            pragma=pragma,
            tag=tag,
            separator=sep,
            run_args=kwargs,
        )

        script = [self.shebang]

        script += self.parser(submit_args)

        if self.extra is not None:
            script += [self.extra]

        return "\n".join(script)

    def pack(self, file=None):
        if file is not None:
            self.to_yaml(filepath=file)
            return
        return self.to_dict()

    @classmethod
    def unpack(cls, data: dict = None, file: str = None, limit: bool = True):
        if file is not None:
            return cls.from_yaml(file)
        return cls.from_dict(data)
