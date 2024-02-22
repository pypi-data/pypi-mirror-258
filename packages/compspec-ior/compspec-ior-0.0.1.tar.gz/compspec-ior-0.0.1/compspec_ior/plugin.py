import argparse
import json
import logging
import os
import shlex

import compspec.utils as utils
from compspec.plugin import PluginBase

import compspec_ior.defaults as defaults

logger = logging.getLogger("compspec-ior")


class Plugin(PluginBase):
    """
    The IOR extractor plugin
    """

    # These metadata fields are required (and checked for)
    description = "IOR parallel I/O benchmarks"
    namespace = defaults.namespace
    version = defaults.spec_version
    schema = defaults.schema_url

    def add_arguments(self, subparser):
        """
        Add arguments for the plugin to show up in argparse
        """
        ior = subparser.add_parser(
            self.name,
            formatter_class=argparse.RawTextHelpFormatter,
            description=self.description,
        )
        # Ensure these are namespaced to your plugin
        ior.add_argument(
            "ior_args",
            help="Arguments for IOR (defaults to reasonable set if not defined)",
            nargs="*",
        )
        ior.add_argument(
            "--ior-load",
            dest="ior_load",
            help="Load metadata from this file instead of extraction from system directly.",
        )

    def run_ior(self, command):
        """
        Run IOR to generate json instead of loading from file.
        """
        if not isinstance(command, list):
            command = shlex.split(command)

        if "ior" not in command:
            command = ["ior"] + command

        # We must output to json
        if "summaryFormat" not in command:
            command += ["-O", "summaryFormat=JSON"]
        logger.debug(" ".join(command))

        result = utils.run_command(command)
        if result["return_code"] != 0:
            msg = " ".join(command)
            raise ValueError(f"Issue with running {msg}: {result['message']}")

        # Load the result
        return json.loads(result["message"])

    def extract(self, args, extra):
        """
        Run IOR and map metadata into compspec schema.

        Note that "extract" simply needs to return key value
        pairs of extraction metadata and values. Ideally, you can
        maintain things in lowercase, and if you have flattened
        groups represent them as <level1>.<level2>. Do not worry
        about adding a top level namespace for the plugin, this
        is handled by compspec.
        """
        if args.ior_load:
            data = utils.read_json(args.ior_load)
        else:
            data = self.run_ior(args.ior_args)

        # Prepare metadata, this is handled by another function for extended use
        return self.load_metadata(data)

    def load_metadata(self, data):
        """
        Load IOR metadata into a dictionary that can be given to compspec.
        """
        # Be forgiving if they provide a filepath
        if isinstance(data, str) and os.path.exists(data):
            data = utils.read_json(data)

        meta = {}

        # High level metadata
        for key in ["Version", "Began", "Machine", "Finished", "Command line"]:
            value = data.get(key)

            # This handles a single entry, lowercase and removes spaces
            key = utils.normalize_key(key)

            # Key needs to be lowercase and
            # Do not add empty values
            if value is not None:
                meta[key] = value

        # Add in summary - the operations (I think) should be unique
        for entry in data["summary"]:
            key = f"summary.{entry['operation']}"
            for k, v in entry.items():
                # This is more of the namespace
                if k == "operation":
                    continue
                meta[f"{key}.{k}"] = v

        # Now add in tests (note it's not clear yet which of these we should keep)
        for test in data["tests"]:
            key = f"test.{test['TestID']}"
            for a in [
                "StartTime",
                "Capacity",
                "Used Capacity",
                "Inodes",
                "Used Inodes",
            ]:
                subkey = utils.normalize_key(a)
                meta[f"{key}.{subkey}"] = test[a]

            # Add in Parameters for tests
            # These are in camel case, let's keep them as such
            for k, v in (test.get("Parameters") or {}).items():
                meta[f"{key}.parameters.{k}"] = v

            # Now add in options
            for k, v in (test.get("Options") or {}).items():
                subkey = utils.normalize_key(k)
                meta[f"{key}.options.{k}"] = v

            # Add results from list
            for i, result in enumerate(test.get("Results") or []):
                for k, v in result.items():
                    meta[f"{key}.results.{i}.{k}"] = v
        return meta
