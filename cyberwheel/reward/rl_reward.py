from cyberwheel.network.network_base import Host, Network
from cyberwheel.reward.reward_base import Reward, RewardMap, RecurringAction
from cyberwheel.utils.hybrid_set_list import HybridSetList


class RLReward(Reward):
    def __init__(self, red_agent, blue_agent, args, network: Network) -> None:
        super().__init__(red_agent, blue_agent)
        # adapt to args signature used elsewhere
        self.valid_targets = getattr(args, 'valid_targets', 'all')
        self.network = network
        # internal last-call context (env will populate before reward retrieval)
        self._ctx = None

    def set_context(self, red_action: str, blue_action: str, red_success: bool, blue_success: bool,
                    target_host: Host, blue_id: str = "-1", blue_recurring: int = 0) -> None:
        self._ctx = (red_action, blue_action, red_success, blue_success, target_host, blue_id, blue_recurring)

    def _compute(
        self,
        red_action: str,
        blue_action: str,
        red_success: bool,
        blue_success: bool,
        target_host: Host,
        blue_id: str,
        blue_recurring: int,
    ) -> int | float:
        
        if self.valid_targets == "servers":
            valid_targets = self.network.server_hosts
        elif self.valid_targets == "users":
            valid_targets = self.network.user_hosts
        elif self.valid_targets == "all":
            valid_targets = valid_targets = HybridSetList(self.network.hosts.keys())
        elif type(self.valid_targets) is list:
            valid_targets = HybridSetList(self.valid_targets)
        elif type(self.valid_targets) is str:
            valid_targets = HybridSetList(self.valid_targets)
        else:
            valid_targets = HybridSetList(self.network.hosts.keys())

        target_host_name = target_host.name
        decoy = target_host.decoy

        if red_success and not decoy and target_host_name in valid_targets:  # If red action succeeded on a real Host
            r = self.red_rewards[red_action][0] * -1
            r_recurring = self.red_rewards[red_action][1] * -1
        elif red_success and decoy and target_host_name in valid_targets:
            r = self.red_rewards[red_action][0] * 10
            r_recurring = self.red_rewards[red_action][1] * 10
        else:
            r = 0
            r_recurring = 0

        if blue_success:
            b = self.blue_rewards[blue_action][0]
        else:
            b = 0
        
        if r_recurring != 0:
            self.add_recurring_red_action('0', red_action, decoy)

        if blue_recurring == -1:
            self.remove_recurring_blue_action(blue_id)
        elif blue_recurring == 1:
            self.add_recurring_blue_action(blue_id, blue_action)

        return r + b + self.sum_recurring()

    def calculate_reward(self) -> int | float:
        # Base class interface: use stored context
        if self._ctx is None:
            return 0
        return self._compute(*self._ctx)
    
    def sum_recurring(self) -> int | float:
        sum = 0
        for ra in self.blue_recurring_actions:
            sum += self.blue_rewards[ra.action][1]
        for ra in self.red_recurring_actions:
            sum += self.red_rewards[ra[0].action][1]
        return sum

    def add_recurring_blue_action(self, id: str, action: str) -> None:
        self.blue_recurring_actions.append(RecurringAction(id, action))

    def remove_recurring_blue_action(self, id: str) -> None:
        for i in range(len(self.blue_recurring_actions)):
            if self.blue_recurring_actions[i].id == id:
                self.blue_recurring_actions.pop(i)
                break

    def add_recurring_red_action(self, id: str, red_action: str, is_decoy: bool) -> None:
        self.red_recurring_actions.append((RecurringAction(id, red_action), is_decoy))

    def reset(self) -> None:
        self.blue_recurring_actions = []
        self.red_recurring_actions = []
