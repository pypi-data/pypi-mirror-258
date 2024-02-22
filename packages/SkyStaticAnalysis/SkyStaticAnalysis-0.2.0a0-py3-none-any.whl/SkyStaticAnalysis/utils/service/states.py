import json
from enum import Enum, auto
from typing import Any, List, Tuple, Type, TypeVar, Generic


class TransitionStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"


S = TypeVar("S", bound=Enum)
T = TypeVar("T", bound=Enum)


class Transition(Generic[S, T]):
    def __init__(
        self,
        trigger: T,
        source: S,
        dest: S,
        before_transition=None,
        after_transition=None,
    ):
        self.trigger = trigger
        self.source = source
        self.dest = dest
        self.before_transition = before_transition
        self.after_transition = after_transition


class StateMachine(Generic[S, T]):
    """
    状态机类，用于处理状态转换。

    参数：
        transitions (List[Transition[S, T]]): 状态转换列表，包含源状态、触发器和目标状态等信息。
        initial (S): 初始状态。

    属性：
        state (S): 当前状态。
        transitions (Dict[S, dict[T, Transition[S, T]]]): 状态转移字典，键为源状态，值为一个字典，其中键为触发器，值为对应的转换对象。
    """

    def __init__(self, transitions: List[Transition[S, T]], initial: S):
        """
        初始化状态机。

        参数：
            transitions (List[Transition[S, T]]): 状态转换列表，包含源状态、触发器和目标状态等信息。
            initial (S): 初始状态。
        """
        self.state = initial
        self.transitions = {
            outer_t.source: {
                t.trigger: t for t in transitions if t.source == outer_t.source
            }
            for outer_t in transitions
        }
        print(self.transitions)

    def process(self, trigger: T, data: Any) -> Tuple[TransitionStatus, str]:
        """
        处理状态转换。

        参数：
            trigger (T): 触发器。

        如果触发器不在当前状态的转移列表中，直接返回
        如果存在before_transition回调函数且返回False，则返回。
        打印状态转移信息，更新当前状态，如果存在after_transition回调函数，调用之。
        """
        if trigger not in self.transitions[self.state]:
            return TransitionStatus.FAILED, "Invalid trigger"

        transition = self.transitions[self.state][trigger]
        if transition.before_transition and not transition.before_transition():
            return TransitionStatus.FAILED, "Before transition callback returned False"

        self.state = transition.dest

        if transition.after_transition:
            transition.after_transition(data)
        return (
            TransitionStatus.SUCCEEDED,
            f"Transitioned from {transition.source} to {transition.dest}",
        )


# # Serialize the state machine to JSON
# sm_json = json.dumps(
#     {
#         "state": str(sm.state),
#         "transitions": [
#             {"trigger": str(t.trigger), "source": str(t.source), "dest": str(t.dest)}
#             for t in transitions
#         ],
#     }
# )
# print(sm_json)
