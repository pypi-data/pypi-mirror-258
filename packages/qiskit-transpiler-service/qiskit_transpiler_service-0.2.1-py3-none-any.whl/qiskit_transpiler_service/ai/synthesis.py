import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from qiskit.circuit.exceptions import CircuitError
from qiskit.converters import circuit_to_dag
from qiskit.dagcircuit.dagcircuit import DAGCircuit
from qiskit.quantum_info import Clifford
from qiskit.transpiler.basepasses import TransformationPass

from .service_wrapper import TranspilerError
from .synthesis_service_wrappers import (
    CliffordAIService,
    LinearFunctionAIService,
    PermutationAIService,
)

logging.getLogger().setLevel(logging.INFO)

MAX_THREADS = os.environ.get("AI_TRANSPILER_MAX_THREADS", None)


class AISynthesis(TransformationPass):
    """AI Synthesis base class"""

    def __init__(
        self, backend_name, synth_service, replace_only_if_better=True, max_threads=None
    ) -> None:
        self.backend_name = backend_name
        self.replace_only_if_better = replace_only_if_better
        self.synth_service = synth_service
        self.max_threads = max_threads if max_threads else MAX_THREADS
        super().__init__()

    def _should_keep_original(self, synth, original):
        if synth is None:
            return True
        return (
            original is not None
            and self.replace_only_if_better
            and self._is_original_a_better_circuit(synth, original)
        )

    def synth_node(self, node):
        try:
            synth_input, original = self._get_synth_input_and_original(node)
        except CircuitError:
            logging.warning(
                f"Error getting  synth input from node. Skipping ai transpilation."
            )
            return None, None
        try:
            qargs = [q._index for q in node.qargs]
            logging.warning(f"Attempting synthesis over qubits {qargs}")
            synth = self.synth_service.transpile(
                synth_input, backend=self.backend_name, qargs=qargs
            )
        except TranspilerError as e:
            logging.warning(
                f"{self.synth_service.__class__.__name__} couldn't synthesize the circuit: {e}"
            )
            synth = None

        if synth is None and original is None:
            logging.warning("Keeping original circuit")
            return None, None
        elif self._should_keep_original(synth, original):
            logging.warning("Keeping original circuit")
            output = original
        else:
            logging.warning("Using synthesized circuit")
            output = synth
        return (output, node)

    def run(self, dag: DAGCircuit):
        logging.info(f"Requesting synthesis to the service")
        future_list = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for node in self._get_nodes(dag):
                future_list.append(executor.submit(self.synth_node, node))
            for future in as_completed(future_list):
                output, node = future.result()
                if output:
                    dag.substitute_node_with_dag(node, circuit_to_dag(output))

        return dag


class AICliffordSynthesis(AISynthesis):
    """AI Clifford Synthesis"""

    def __init__(
        self, backend_name, replace_only_if_better=True, max_threads=None
    ) -> None:
        super().__init__(
            backend_name, CliffordAIService(), replace_only_if_better, max_threads
        )

    def _get_synth_input_and_original(self, node):
        if type(node.op) is Clifford:
            cliff, original = node.op, None
        else:
            cliff, original = node.op.params
        return cliff, original

    def _get_nodes(self, dag):
        return dag.named_nodes("clifford", "Clifford")

    def _is_original_a_better_circuit(self, synth, original):
        return (
            original.decompose("swap").num_nonlocal_gates()
            <= synth.num_nonlocal_gates()
        )


class AILinearFunctionSynthesis(AISynthesis):
    """AI Linear Function"""

    def __init__(
        self, backend_name, replace_only_if_better=True, max_threads=None
    ) -> None:
        super().__init__(
            backend_name, LinearFunctionAIService(), replace_only_if_better, max_threads
        )

    def _get_synth_input_and_original(self, node):
        return node.op, node.op.params[1]

    def _get_nodes(self, dag):
        return dag.named_nodes("linear_function", "Linear_function")

    def _is_original_a_better_circuit(self, synth, original):
        return (
            original.decompose("swap").num_nonlocal_gates()
            <= synth.num_nonlocal_gates()
        )


class AIPermutationSynthesis(AISynthesis):
    """AI Linear Function"""

    def __init__(
        self, backend_name, replace_only_if_better=True, max_threads=None
    ) -> None:
        super().__init__(
            backend_name, PermutationAIService(), replace_only_if_better, max_threads
        )

    def _get_synth_input_and_original(self, node):
        return node.op.params[0].tolist(), None

    def _get_nodes(self, dag):
        return dag.named_nodes("permutation", "Permutation")

    def _is_original_a_better_circuit(self, synth, original):
        return original.num_nonlocal_gates() <= synth.num_nonlocal_gates()
