"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import cirq_google.api.v1.operations_pb2
import cirq_google.api.v1.params_pb2
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Program(google.protobuf.message.Message):
    """A quantum program. This includes a quantum circuit and also a set of circuit
    parameters over which the circuit should be run.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    OPERATIONS_FIELD_NUMBER: builtins.int
    PARAMETER_SWEEPS_FIELD_NUMBER: builtins.int
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cirq_google.api.v1.operations_pb2.Operation]:
        """Gates and measurements that make up the circuit."""
    @property
    def parameter_sweeps(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cirq_google.api.v1.params_pb2.ParameterSweep]:
        """The circuit parameters for the operations above will be evaluated for
        each parameter in parameter sweeps.
        """
    def __init__(
        self,
        *,
        operations: collections.abc.Iterable[cirq_google.api.v1.operations_pb2.Operation] | None = ...,
        parameter_sweeps: collections.abc.Iterable[cirq_google.api.v1.params_pb2.ParameterSweep] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["operations", b"operations", "parameter_sweeps", b"parameter_sweeps"]) -> None: ...

global___Program = Program

@typing_extensions.final
class RunContext(google.protobuf.message.Message):
    """The context for running a quantum program."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PARAMETER_SWEEPS_FIELD_NUMBER: builtins.int
    @property
    def parameter_sweeps(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cirq_google.api.v1.params_pb2.ParameterSweep]:
        """The parameters for operations in a program."""
    def __init__(
        self,
        *,
        parameter_sweeps: collections.abc.Iterable[cirq_google.api.v1.params_pb2.ParameterSweep] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["parameter_sweeps", b"parameter_sweeps"]) -> None: ...

global___RunContext = RunContext

@typing_extensions.final
class ParameterizedResult(google.protobuf.message.Message):
    """The parameters used to generate result along with the results for this
    set of parameters.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PARAMS_FIELD_NUMBER: builtins.int
    MEASUREMENT_RESULTS_FIELD_NUMBER: builtins.int
    @property
    def params(self) -> cirq_google.api.v1.params_pb2.ParameterDict:
        """The parameter dict that was used when generating these results."""
    measurement_results: builtins.bytes
    """The measurement results. This is a packed representation of all of the
    measurements for fixed set of parameters (specified by params above)
    across all of the repetitions for the set of parameters given the
    params field.

    The result of a measurement gate is a list of bits, one for each qubit
    that has been measured. Every Program has a fixed set of measurement gates.
    These gates are labeled by a key (this key is unique across the Program).
    The results of a single run of the program should consist of bits for
    each of the measurement gates. To order these bits we use the
    measurement_keys field of the SweepResult. This is an ordered list of
    measurement keys, each of which includes a list of qubits that the
    measurement acts on. We use the ordering of the measurement_keys and then
    the ordering of the qubits to define the order of the bit string for a
    single run of the measurement.

    If the keys are (k_i), for i \\in {0, 1, ..., m-1}, and the measurement
    acts on qubits q_{i,0}, q_{i,1}, ..., q_{i,n_i-1} (so that ith key
    corresponds to n_i qubits), then the measurements bit results are
    defined as
     r_0[0] r_0[1] ... r_0[n_i-1] r_1[0] r_1[1] ... r_1[n_1-1] ...
      ... r_{m-1}[0] r_{m-1}[1] ... r_{m-1}[n_{m-1}-1]
    Here r_i are the measurement result for the ith key (order defined by
    measurement keys).  Since the ith key has n_i qubits, r_i is a length
    n_i bit string, and r_i[j] is the jth bit in this string (order
    following the list order of the qubits).

    The above describes a bit string for a single run of a program with
    fixed parameters. This program however may be repeated, the number
    of times the program was run for these parameters is defined by the
    num_repetitions field of the SweepResult. If R_l is the bit string
    for the lth repetition of the program (defined by the r_0[0]... bit
    string above), then the full results is the concatenation of these
    bit strings
      R_0 R_1 ... R_{num_repetitions - 1}

    Finally this entire bit string is encoded into the bytes of this field
    using little endian notation. That is, the least significant bit of the
    bytes is the first bit of the bit string, the second-least significant
    bit of the bytes is the second bit of the bit string, etc.
    """
    def __init__(
        self,
        *,
        params: cirq_google.api.v1.params_pb2.ParameterDict | None = ...,
        measurement_results: builtins.bytes = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["params", b"params"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["measurement_results", b"measurement_results", "params", b"params"]) -> None: ...

global___ParameterizedResult = ParameterizedResult

@typing_extensions.final
class MeasurementKey(google.protobuf.message.Message):
    """A message which represents a measurement key, along with the qubits
    upon which the measurement acts. This measurement is in the computational
    basis.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_FIELD_NUMBER: builtins.int
    QUBITS_FIELD_NUMBER: builtins.int
    key: builtins.str
    """The measurement key."""
    @property
    def qubits(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[cirq_google.api.v1.operations_pb2.Qubit]:
        """The qubits upon which this measurement is performed."""
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        qubits: collections.abc.Iterable[cirq_google.api.v1.operations_pb2.Qubit] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "qubits", b"qubits"]) -> None: ...

global___MeasurementKey = MeasurementKey

@typing_extensions.final
class SweepResult(google.protobuf.message.Message):
    """The measurement results for a particular ParameterSweep."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    REPETITIONS_FIELD_NUMBER: builtins.int
    MEASUREMENT_KEYS_FIELD_NUMBER: builtins.int
    PARAMETERIZED_RESULTS_FIELD_NUMBER: builtins.int
    repetitions: builtins.int
    """The total number of repetitions that were performed for this sweep.
    This is reported in order to make it possible to decode the bytes
    in the measurement results.
    """
    @property
    def measurement_keys(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MeasurementKey]:
        """A list of measurement keys (string) along with the qubits that have been
        measured. The size of the measurement key is the total number of
        measurements in the list of operations for the Program. The measurement
        keys are all unique.
        """
    @property
    def parameterized_results(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ParameterizedResult]:
        """The results along with the parameters that generated these results.
        These represent the expanded parameters defined int he ParameterSweep
        which this SweepResult corresponds to.
        """
    def __init__(
        self,
        *,
        repetitions: builtins.int = ...,
        measurement_keys: collections.abc.Iterable[global___MeasurementKey] | None = ...,
        parameterized_results: collections.abc.Iterable[global___ParameterizedResult] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["measurement_keys", b"measurement_keys", "parameterized_results", b"parameterized_results", "repetitions", b"repetitions"]) -> None: ...

global___SweepResult = SweepResult

@typing_extensions.final
class Result(google.protobuf.message.Message):
    """The overall results of running a Program."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SWEEP_RESULTS_FIELD_NUMBER: builtins.int
    @property
    def sweep_results(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SweepResult]:
        """The results for each ParameterSweep. These will be in the same order
        as the parameter_sweeps repeated field in the Program that generated
        these results.
        """
    def __init__(
        self,
        *,
        sweep_results: collections.abc.Iterable[global___SweepResult] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["sweep_results", b"sweep_results"]) -> None: ...

global___Result = Result
