from code_generator_backend import DataclassGenerator
from unittest import TestCase
import json
class IntegrationTests(TestCase):
    """
    Some tests that tests big picture the code is working as expected
    """

    def test_ecs_cluster(self):
        """
        Tests non subclassed exampled for an ecs cluster data structure from AWS
        """
        test_data = json.load(open("../tests/test_data/single_cluster.json", 'r'))
        expected_output = """

@dataclass
class EcsCluster:
	clusterArn: str
	clusterName: str
	status: str
	registeredContainerInstancesCount: int
	runningTasksCount: int
	pendingTasksCount: int
	activeServicesCount: int
	statistics: List
	tags: List
	settings: List
	capacityProviders: List
	defaultCapacityProviderStrategy: List"""
        actual_output = DataclassGenerator(python_object=test_data, class_name="EcsCluster").generate_dataclass_str()
        self.assertEqual(expected_output, actual_output)


    def test_ecs_clusters(self):
        """
        Tests that it creates a parent class for a nested ecs clusters data
        """
        test_data_ecs_clusters = json.load(open("../tests/test_data/ecs_clusters.json", "r"))
        expected_output = """

@dataclass
class Failures:
	clusterArn: str
	clusterName: str
	status: str
	registeredContainerInstancesCount: int
	runningTasksCount: int
	pendingTasksCount: int
	activeServicesCount: int
	statistics: List

@dataclass
class Clusters:
	clusterArn: str
	clusterName: str
	status: str
	registeredContainerInstancesCount: int
	runningTasksCount: int
	pendingTasksCount: int
	activeServicesCount: int
	statistics: List
	tags: List
	settings: List
	capacityProviders: List
	defaultCapacityProviderStrategy: List

@dataclass
class EcsClusters:
	clusters: List[Clusters]
	failures: List[Failures]





"""
        actual_output = DataclassGenerator(python_object=test_data_ecs_clusters, class_name="EcsClusters").generate_parent_class_str()
        self.assertEqual(expected_output, actual_output)

    def test_algorand_block_structure(self):
        """
        Tests a more complex data structure - an Algorand Block structure. This is one of the first use cases I used
        this generator for. I wanted to create a fully typed Algorand Indexer API so that the complex data structure
        is a lot easier to work with.
        """
        test_data_algorand_block = json.load(open("../tests/test_data/algoblock.json"))
        expected_output = """

@dataclass
class UpgradeVote:
	upgrade_approve: bool
	upgrade_delay: int
	upgrade_propose: str

@dataclass
class UpgradeState:
	current_protocol: str
	next_protocol: str
	next_protocol_approvals: int
	next_protocol_switch_on: int
	next_protocol_vote_before: int

@dataclass
class Multisig:
	subsignature: List[Dict]
	threshold: int
	version: int

@dataclass
class MultisigSignature:
	subsignature: List[Dict]
	threshold: int
	version: int

@dataclass
class Logicsig:
	args: List[str]
	logic: str
	multisig_signature: MultisigSignature
	signature: str

@dataclass
class Signature:
	logicsig: Logicsig
	multisig: Multisig
	sig: str

@dataclass
class PaymentTransaction:
	amount: int
	close_amount: int
	close_remainder_to: str
	receiver: str

@dataclass
class KeyregTransaction:
	non_participation: bool
	selection_participation_key: str
	vote_first_valid: int
	vote_key_dilution: int
	vote_last_valid: int
	vote_participation_key: str

@dataclass
class AssetTransferTransaction:
	amount: int
	asset_id: int
	close_amount: int
	close_to: str
	receiver: str
	sender: str

@dataclass
class AssetFreezeTransaction:
	address: str
	asset_id: int
	new_freeze_status: bool

@dataclass
class Params:
	clawback: str
	creator: str
	decimals: int
	default_frozen: bool
	freeze: str
	manager: str
	metadata_hash: str
	name: str
	name_b64: str
	reserve: str
	total: int
	unit_name: str
	unit_name_b64: str
	url: str
	url_b64: str

@dataclass
class AssetConfigTransaction:
	asset_id: int
	params: Params

@dataclass
class GlobalStateSchema:
	num_uint: int
	num_byte_slice: int

@dataclass
class LocalStateSchema:
	num_uint: int
	num_byte_slice: int

@dataclass
class ApplicationTransaction:
	application_id: int
	on_completion: str
	application_args: List[str]
	accounts: List[str]
	foreign_apps: List[int]
	foreign_assets: List[int]
	local_state_schema: LocalStateSchema
	global_state_schema: GlobalStateSchema
	approval_program: str
	clear_state_program: str
	extra_program_pages: int

@dataclass
class Transactions:
	application_transaction: ApplicationTransaction
	asset_config_transaction: AssetConfigTransaction
	asset_freeze_transaction: AssetFreezeTransaction
	asset_transfer_transaction: AssetTransferTransaction
	auth_addr: str
	close_rewards: int
	closing_amount: int
	confirmed_round: int
	created_application_index: int
	created_asset_index: int
	fee: int
	first_valid: int
	genesis_hash: str
	genesis_id: str
	group: str
	id: str
	intra_round_offset: int
	keyreg_transaction: KeyregTransaction
	last_valid: int
	lease: str
	note: str
	payment_transaction: PaymentTransaction
	receiver_rewards: int
	rekey_to: str
	round_time: int
	sender: str
	sender_rewards: int
	signature: Signature
	tx_type: str
	local_state_delta: List[Dict]
	global_state_delta: List[Dict]
	logs: List[str]
	inner_txns: List[str]

@dataclass
class Rewards:
	fee_sink: str
	rewards_calculation_round: int
	rewards_level: int
	rewards_pool: str
	rewards_rate: int
	rewards_residue: int

@dataclass
class AlgorandBlock:
	genesis_hash: str
	genesis_id: str
	previous_block_hash: str
	rewards: Rewards
	round: int
	seed: str
	timestamp: int
	transactions: List[Transactions]
	transactions_root: str
	txn_counter: int
	upgrade_state: UpgradeState
	upgrade_vote: UpgradeVote









"""
        actual_output = DataclassGenerator(python_object=test_data_algorand_block, class_name="AlgorandBlock").generate_parent_class_str()
        self.assertEqual(expected_output, actual_output)


