"""
Take data from salt and "return" it into a file formatted for Prometheus using
the `Text Exposition Format <https://prometheus.io/docs/instrumenting/exposition_formats/#text-format-example>`_
which rolls up state success and failure data.

.. versionadded:: 3005

The intended use case for this module is to have distributed success/failure
reporting from minions for unattended state or highstate runs.

Add the following to the minion or master configuration file to configure the
output location which Prometheus will monitor via Node Exporter.

.. code-block:: yaml

    prometheus_textfile.filename: <path_to_output_file>

Default is ``/var/cache/salt/minion/prometheus_textfile/salt.prom`` using the
``cachedir`` minion configuration.

The ``salt_procs`` metric will look for ``salt-minion`` processes by name. If
you have a custom installation of Salt, you might want to change the ``psutil``
process name to be matched or switch to matching the "exe" attribute of the
``Process.info`` dictionary.

.. code-block:: yaml

    prometheus_textfile.proc_name: custom-minion

.. code-block:: yaml

    prometheus_textfile.match_exe: True
    prometheus_textfile.exe: /opt/salt/bin/python3

The default operation of sending state metrics to a single file works well for
the use case of running distributed highstate or a single state run on minions.
However, there may be a use case for tracking multiple scheduled states in
separate files. To enable this behavior, set the following option in the
configuration file:

.. code-block:: yaml

    prometheus_textfile.add_state_name: True

This option will add the state name which was run as a filename suffix and also
inside the file as a metric parameter. Highstate runs will receive ``highstate``
as the state name, while running specific states will pass the first argument to
``state.apply`` or ``state.sls`` as the state name.

.. code-block:: bash

    # Filename is "salt-highstate.prom" and metrics get '{state="highstate"}'
    salt-call state.highstate

    # Filename is "salt-highstate.prom" and metrics get '{state="highstate"}'
    salt-call state.apply

    # Filename is "salt-test.prom" and metrics get '{state="test"}'
    salt-call state.apply test

    # Filename is "salt-test.prom" and metrics get '{state="test"}'
    salt-call state.sls test

Additionally, the inferred state name can be overridden on the command line by
passing the ``prom_textfile_state`` keyword argument to the state function.

.. code-block:: bash

    # Filename is "salt-hello.prom" and metrics get '{state="hello"}'
    salt-call state.highstate prom_textfile_state=hello

    # Filename is "salt-hello.prom" and metrics get '{state="hello"}'
    salt-call state.apply test prom_textfile_state=hello

Output file user, group, and mode can optionally be set through configuration
options:

.. code-block:: yaml

    prometheus_textfile.uid: 0
    prometheus_textfile.gid: 0
    prometheus_textfile.mode: "0644"

The metrics can include the names of failed states if necessary. This is
sometimes beneficial for monitoring purposes so engineers can see what in
particular caused a failure condition on a host and whether it is critical.

.. code-block:: yaml

    prometheus_textfile.show_failed_states: true

An additional way of viewing failure conditions is through the
``abort_state_ids`` option. If this option is used, a state ID or list of state
IDs can be provided to indicate an "abort" condition. This allows the user to
see that a failure was related to a "circuit breaker" condition which prevented
the state run to complete.

.. code-block:: yaml

    prometheus_textfile.abort_state_ids:
      - circuit_breaker_state
      - my_other_circuit_breaker

The state IDs in this configuration option can also be presented as a string in
the following manner:

.. code-block:: yaml

    # comma-separated states
    prometheus_textfile.abort_state_ids: circuit_breaker_state,my_other_circuit_breaker
    # single state
    prometheus_textfile.abort_state_ids: circuit_breaker_state

If you have systems running Salt versions which have a non-standard version scheme
(such as running from patched versions), the entire version string can be shown
by utilizing the ``raw_version`` parameter. Otherwise, only the portion of the
string before a plus sign (``+``) will be shown. So, a version string such as
"3004+12.g557e6cc0fc" will be shown as "3004" by default unless ``raw_version``
is enabled.

.. code-block:: yaml

    prometheus_textfile.raw_version: true

"""
import logging
import os
import time

import salt.modules.file
import salt.returners
import salt.utils.files
import salt.utils.platform
from prometheus_client import CollectorRegistry
from prometheus_client import Gauge
from prometheus_client import write_to_textfile

log = logging.getLogger(__name__)

HAS_PSUTIL = False
try:
    import psutil

    HAS_PSUTIL = True
except (ImportError, ModuleNotFoundError):
    log.warning("The psutil library is required for the salt_procs metric.")

# Define the module's virtual name
__virtualname__ = "prometheus_textfile"
# Loader workaround
try:
    __grains__  # pylint: disable=used-before-assignment
except NameError:
    import salt.version  # pylint: disable=ungrouped-imports

    __grains__ = {"saltversion": salt.version.__version__}


def __virtual__():
    return __virtualname__


def _get_options(ret):
    """
    Returns options used for the prometheus_textfile returner.
    """
    defaults = {
        "exe": None,
        "filename": os.path.join(__opts__["cachedir"], "prometheus_textfile", "salt.prom"),
        "uid": -1,  # fpopen default
        "gid": -1,  # fpopen default
        "mode": None,
        "match_exe": False,
        "proc_name": "salt-minion",
        "add_state_name": False,
        "abort_state_ids": None,
        "show_failed_states": False,
        "raw_version": False,
        "fail_comment_length": None,
    }
    attrs = {
        "exe": "exe",
        "filename": "filename",
        "uid": "uid",
        "gid": "gid",
        "mode": "mode",
        "match_exe": "match_exe",
        "proc_name": "proc_name",
        "add_state_name": "add_state_name",
        "abort_state_ids": "abort_state_ids",
        "show_failed_states": "show_failed_states",
        "raw_version": "raw_version",
        "fail_comment_length": "fail_comment_length",
    }
    _options = salt.returners.get_returner_options(
        __virtualname__,
        ret,
        attrs,
        __salt__=__salt__,
        __opts__=__opts__,
        defaults=defaults,
    )

    return _options


def _count_minion_procs(proc_name="salt-minion", match_exe=False, exe=None):
    """
    Return the count of processes with name matching "salt-minion"
    """
    proclist = []
    if HAS_PSUTIL:
        for proc in psutil.process_iter(["name", "exe"]):
            if match_exe and proc.info["exe"] == exe:
                proclist.append(proc)
            elif proc.info["name"] == proc_name:
                proclist.append(proc)
    return len(proclist)


def returner(ret):
    """
    Write Prometheus metrics to a file on the minion.
    """
    state_functions = [
        "state.apply",
        "state.sls",
        "state.highstate",
    ]

    if ret["fun"] not in state_functions:
        log.info(
            "The prometheus_textfile returner is only intended to run on %s functions... not %s",
            ", ".join(state_functions),
            ret["fun"],
        )
        return

    opts = _get_options(ret)

    prom_state = ""

    if opts["add_state_name"]:
        if ret["fun"] == "state.highstate":
            prom_state = "highstate"
        elif ret["fun"] == "state.apply" and (not ret["fun_args"] or "=" in ret["fun_args"][0]):
            prom_state = "highstate"
        else:
            prom_state = ret["fun_args"][0]

    for fun_arg in ret["fun_args"]:
        if not isinstance(fun_arg, str):
            continue
        if fun_arg.lower() == "test=true":
            log.info("The prometheus_textfile returner is not enabled in Test mode.")
            return
        if opts["add_state_name"] and fun_arg.lower().startswith("prom_textfile_state="):
            prom_state = "".join(fun_arg.split("=")[1:])
            log.debug("Prometheus text file returner state name: %s", prom_state)

    out_dir = os.path.dirname(opts["filename"])

    if not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir)
        except OSError:
            log.error("Could not create directory for prometheus output: %s", out_dir)
            return

    success = 0
    failure = 0
    changed = 0
    total = 0
    duration = 0
    for data in ret.get("return", {}).values():
        total += 1
        duration += data.get("duration", 0)
        if data["result"] is False:
            failure += 1
        else:
            success += 1
        if data.get("changes"):
            changed += 1

    if not total:
        log.error("Total states run equals 0. There may be something wrong...")
        return

    salt_procs = _count_minion_procs(
        proc_name=opts["proc_name"],
        match_exe=opts["match_exe"],
        exe=opts["exe"],
    )

    now = int(time.time())

    output = {
        "salt_procs": {
            "help": "Number of salt minion processes running",
            "value": salt_procs,
        },
        "salt_states_succeeded": {
            "help": "Number of successful states in the run",
            "value": success,
        },
        "salt_states_failed": {
            "help": "Number of failed states in the run",
            "value": failure,
        },
        "salt_states_changed": {
            "help": "Number of changed states in the run",
            "value": changed,
        },
        "salt_states_total": {
            "help": "Total states in the run",
            "value": total,
        },
        "salt_states_success_pct": {
            "help": "Percent of successful states in the run",
            "value": round((success / total) * 100, 2),
        },
        "salt_states_failure_pct": {
            "help": "Percent of failed states in the run",
            "value": round((failure / total) * 100, 2),
        },
        "salt_states_changed_pct": {
            "help": "Percent of changed states in the run",
            "value": round((changed / total) * 100, 2),
        },
        "salt_elapsed_time": {
            "help": "Time spent for all operations during the state run",
            "value": round(duration, 3),
        },
        "salt_last_started": {
            "help": "Estimated time the state run started",
            "value": int(now - duration / 1000),
        },
        "salt_last_completed": {
            "help": "Time of last state run completion",
            "value": now,
        },
        "salt_version": {
            "help": "Version of installed Salt package",
            "value": __grains__["saltversion"].split("+", maxsplit=1)[0],
        },
        "salt_version_tagged": {
            "help": "Version of installed Salt package as a tag",
            "value": 1,
        },
    }

    registry = CollectorRegistry()

    if opts["show_failed_states"]:
        labels = ["state_id", "state_comment"]
        if opts["add_state_name"]:
            labels.append("state")
        gauge_show_failed_states = Gauge(
            "salt_failed",
            "Information regarding state with failure condition",
            labels,
            registry=registry,
        )
        for state_id, state_return in ret["return"].items():
            if state_return["result"] is False:
                failed_comment = state_return.get("comment", "").replace('"', "").replace("\n", " ")
                label_values = [
                    state_id.split("_|-")[1],
                    failed_comment[0 : opts["fail_comment_length"]],
                ]
                if opts["add_state_name"]:
                    label_values.append(prom_state)
                gauge_show_failed_states.labels(*label_values).set(1)

    if opts["abort_state_ids"]:
        labels = []
        label_values = []
        if opts["add_state_name"]:
            labels.append("state")
            label_values.append(prom_state)
        if not isinstance(opts["abort_state_ids"], list):
            opts["abort_state_ids"] = [item.strip() for item in opts["abort_state_ids"].split(",")]

        aborted_value = 0
        for state_id, state_return in ret["return"].items():
            if not state_return["result"] and state_return.get("__id__") in opts["abort_state_ids"]:
                aborted_value = 1
                labels.append("state_id")
                label_values.append(state_id.split("_|-")[1])

        gauge_salt_aborted = Gauge(
            "salt_aborted",
            "Flag to show that a specific abort state failed",
            labels,
            registry=registry,
        )
        if label_values:
            gauge_salt_aborted.labels(*label_values).set(aborted_value)
        else:
            gauge_salt_aborted.set(aborted_value)

    if opts["add_state_name"]:
        old_name, ext = os.path.splitext(opts["filename"])
        opts["filename"] = f"{old_name}-{prom_state}{ext}"
        log.debug(
            "Modified Prometheus filename from %s to %s",
            old_name + ext,
            opts["filename"],
        )

    for key in list(output.keys()):
        labels = []
        label_values = []
        if opts["add_state_name"]:
            labels.append("state")
            label_values.append(prom_state)
        if key == "salt_version_tagged":
            labels.append("salt_version")
            if opts["raw_version"]:
                label_values.append(__grains__["saltversion"])
            else:
                label_values.append(__grains__["saltversion"].split("+", maxsplit=1)[0])
        keys_dict = output.pop(key)
        gauge_keys = Gauge(key, keys_dict["help"], labels, registry=registry)
        try:
            if label_values:
                gauge_keys.labels(*label_values).set(keys_dict["value"])
            else:
                gauge_keys.set(keys_dict["value"])
        except ValueError:
            keys_dict["value"] = keys_dict["value"].split("rc", maxsplit=1)[0]
            if label_values:
                gauge_keys.labels(*label_values).set(keys_dict["value"])
            else:
                gauge_keys.set(keys_dict["value"])

    write_to_textfile(opts["filename"], registry)
    if not salt.utils.platform.is_windows():
        salt.modules.file.chown(opts["filename"], opts["uid"], opts["gid"])
        if opts["mode"]:
            try:
                salt.modules.file.set_mode(opts["filename"], opts["mode"])
            except ValueError:
                opts["mode"] = None
                log.exception("Unable to convert mode to octal. Using system default.")

    return True
