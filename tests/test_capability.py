from src.capability.models import Action, Capability
from src.capability.recorder import CapabilityRecorder


def test_capability_save_and_load(tmp_path):
    recorder = CapabilityRecorder(output_dir=str(tmp_path))

    capability = Capability(
        name="test_balance",
        description="Test capability",
        parameters=["member_id"],
        actions=[
            Action(
                action_type="fill",
                selector='input[name="member_id"]',
                value="{{member_id}}",
            ),
            Action(
                action_type="click",
                selector='button[type="submit"]',
            ),
        ],
    )

    recorder.save(capability)

    loaded_capability = recorder.load("test_balance")

    assert loaded_capability.name == "test_balance"
    assert loaded_capability.parameters == ["member_id"]
    assert len(loaded_capability.actions) == 2
    assert loaded_capability.actions[0].value == "{{member_id}}"